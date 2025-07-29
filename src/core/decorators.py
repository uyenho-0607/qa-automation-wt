import functools
import inspect
import json
import time

import requests
from selenium.common import StaleElementReferenceException, ElementNotInteractableException, \
    ElementClickInterceptedException

from src.data.project_info import StepLogs
from src.utils.allure_utils import attach_verify_table, log_verification_result, attach_screenshot
from src.utils.format_utils import format_request_log
from src.utils.logging_utils import logger


def attach_table_details(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        __tracebackhide__ = True
        actual, expected, *_ = args
        
        # Store the comparison result if it's returned by the function
        comparison_result = None
        
        # Call the function and capture any returned comparison result
        result = func(*args, **kwargs)
        
        # Check if the function returned a comparison result (for soft_assert)
        if isinstance(result, dict) and "res" in result and "diff" in result:
            comparison_result = result

        if all([isinstance(actual, dict), isinstance(expected, dict)]):
            title = "Verify Table Details"
            if StepLogs.test_steps:
                title += f" - {StepLogs.test_steps[-1]}"

            attach_verify_table(
                actual, expected, 
                tolerance_percent=kwargs.get("tolerance"), 
                tolerance_fields=kwargs.get("tolerance_fields"), 
                title=title,
                comparison_result=comparison_result
            )

        elif kwargs.get("log_details"):
            name = "Verification Details"
            if StepLogs.test_steps:
                name += f" - {StepLogs.test_steps[-1]}"
            log_verification_result(
                actual, expected, result, desc=kwargs.get("desc", "") + kwargs.get("err_msg", "") if not result else "", name=name
            )

    return _wrapper


def handle_stale_element(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        __tradebackhide__ = True

        # Use inspect to get all function parameters including defaults
        sig = inspect.signature(func)
        bound_args = sig.bind(self, *args, **kwargs)
        bound_args.apply_defaults()  # This applies default values
        all_args = bound_args.arguments
        
        max_retries = 3
        raise_exception = all_args.get("raise_exception")

        for attempt in range(max_retries + 1):  # +1 for initial attempt
            try:
                return func(self, *args, **kwargs)

            except (StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException) as e:
                # Clear any broken steps that might have been added from the previous attempt
                if StepLogs.broken_steps and attempt < max_retries + 1:
                    StepLogs.broken_steps.pop()

                if attempt < max_retries:
                    logger.warning(f"{type(e).__name__} for locator {args[0]} (attempt {attempt + 1}/{max_retries + 1}), retrying...")
                    time.sleep(1)
                    continue

                else:
                    # Final attempt failed, re-raise the exception
                    logger.error(f"{type(e).__name__} for locator {args[0]} after {max_retries + 1} attempts")
                    # logger.debug(f"raise exception: {raise_exception}")
                    if raise_exception and StepLogs.test_steps:
                        logger.debug("- Capture broken info")
                        StepLogs.all_failed_logs.append((StepLogs.test_steps[-1], ""))
                        attach_screenshot(self._driver, name="broken")  # Capture broken screenshot

                    raise e

        return None

    return wrapper


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
