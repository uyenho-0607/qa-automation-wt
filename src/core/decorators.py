import functools
import json
import time

import requests
from requests import Response

from src.utils.logging_utils import logger

def format_request_log(resp: Response, log_resp=False) -> str:
    # Format request content
    method = resp.request.method.upper()
    lines = [f"curl --location --request {method} '{resp.request.url}'"]

    for key, value in resp.request.headers.items():
        lines.append(f"--header '{key}: {value}'")

    if resp.request.body and isinstance(resp.request.body, (str, bytes)):
        try:
            data = json.loads(resp.request.body)
            json_data = json.dumps(data)  # compact form
        except Exception:
            json_data = resp.request.body.decode() if isinstance(resp.request.body, bytes) else resp.request.body

        lines.append(f"--data-raw '{json_data}'")

    curl_command = " \n".join(lines)

    # Format response content
    try:
        content = resp.json()
        response_text = json.dumps(content, indent=4)
    except ValueError:
        response_text = resp.text.strip()

    if log_resp:
        return f"⮕ Request Sent: \n\n{curl_command}\n\n⬅ Response Received: \n\n{response_text}\n\n"
    return f"⮕ Request Sent: \n\n{curl_command}\n\n"


def after_request(max_retries=3, base_delay=1.0, max_delay=10.0):
    """
    Enhanced decorator for handling API requests with retry logic and proper error handling.
    
    Args:
        max_retries (int): Maximum number of retry attempts
        base_delay (float): Base delay in seconds for exponential backoff
        max_delay (float): Maximum delay in seconds
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            __tracebackhide__ = True

            last_exception = None

            for attempt in range(max_retries + 1):  # +1 for initial attempt
                try:
                    # Execute the API request
                    response = func(self, *args, **kwargs)
                    logger.info(f"- Response time: {response.elapsed.total_seconds()} sec")

                    # Handle successful response
                    if response.ok:
                        logger.debug(f"{format_request_log(response, log_resp=True)}")

                        # Parse JSON response safely
                        try:
                            result = response.json()
                            return result.get("result", result) if response.text.strip() else []

                        except json.JSONDecodeError as e:
                            logger.warning(f"Failed to parse JSON response: {e}")
                            return response.text if response.text else []

                    # Handle server errors (5xx) - always retry
                    elif response.status_code >= 400:
                        logger.warning(f"Server error (attempt {attempt + 1}/{max_retries + 1}): "
                                       f"{format_request_log(response, log_resp=True)}")

                        if attempt < max_retries:
                            delay = min(base_delay * (2 ** attempt), max_delay)
                            logger.debug(f"Retrying in {delay:.2f} seconds...")
                            time.sleep(delay)
                            continue
                        else:
                            raise requests.RequestException(f"Server error after {max_retries + 1} attempts: {response.status_code}")

                    # Handle client errors (4xx) - don't retry
                    else:
                        logger.error(f"Client error: {format_request_log(response, log_resp=True)}")
                        raise Exception(f"API request failed with status {response.status_code}: {response.text}")

                except (requests.RequestException, Exception) as e:
                    last_exception = e

                    # Only retry on server errors or network issues
                    if isinstance(e, requests.RequestException) and attempt < max_retries:
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        logger.debug(f"Request failed (attempt {attempt + 1}/{max_retries + 1}), "
                                     f"retrying in {delay:.2f} seconds... Error: {str(e)}")
                        time.sleep(delay)
                        continue
                    else:
                        # Don't retry on client errors or after max retries
                        break

            # If we get here, all retries failed
            if last_exception:
                raise last_exception

            # This should never be reached, but just in case
            raise Exception("Unexpected error in after_request decorator")

        return wrapper

    return decorator
