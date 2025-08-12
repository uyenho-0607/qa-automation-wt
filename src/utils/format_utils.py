import json
from enum import Enum
from typing import Dict, Any

from requests import Response


def format_dict_to_string(
        data: Dict[str, Any] = None,
        expected: Dict[str, Any] = None,
        actual: Dict[str, Any] = None
) -> str:
    """
    Format a dictionary or compare two dictionaries into a readable string.
    
    Args:
        data: Single dictionary to format (used when not comparing)
        expected: Expected dictionary for comparison
        actual: Actual dictionary for comparison
    
    Examples:
        Single dictionary:
            data = {'name': 'John', 'age': 30}
            print(format_dict_to_string(data))
            ==================================================
            name         : John
            age          : 30
            ==================================================
            
        Dictionary comparison:
            expected = {'name': 'John', 'age': 30}
            actual = {'name': 'John', 'status': 'active'}
            print(format_dict_to_string(None, expected, actual))
            =================================================================================
            Field               | Expected                | Actual
            ---------------------------------------------------------------------------------
            name                | John                    | John
            age                | 30                      | MISSING
            status             | MISSING                 | active
            =================================================================================
    """
    if expected is not None and actual is not None:
        # Comparison mode
        all_keys = sorted(set(list(expected.keys()) + list(actual.keys())))

        # Column widths
        field_width = 20
        value_width = 25

        # Format header
        formatted_lines = [
            f"{'Field':<{field_width}} | {'Expected':<{value_width}} | {'Actual':<{value_width}}",
            "-" * (field_width + value_width * 2 + 5)  # 5 is for the separators and spacing
        ]

        # Format each field
        for key in all_keys:
            expected_value = expected.get(key, "MISSING")
            actual_value = actual.get(key, "MISSING")

            # Convert enum values to their string representation
            if isinstance(expected_value, Enum):
                expected_value = expected_value.value
            if isinstance(actual_value, Enum):
                actual_value = actual_value.value

            formatted_lines.append(
                f"{str(key):<{field_width}} | {str(expected_value):<{value_width}} | {str(actual_value)}"
            )

    else:
        # Single dictionary mode
        field_names = {}
        fields = list(data.keys())
        formatted_lines = []

        for key in fields:
            if key in data:
                display_name = field_names.get(key, key)
                value = data[key]

                if isinstance(value, Enum):
                    value = value.value

                indent_str = " " * 0
                formatted_lines.append(f"{indent_str}{display_name:<15}: {value}")

    # Create border and format output
    border = "=" * (field_width + value_width * 2 + 5 if expected is not None and actual is not None else 50)
    indent_str = " " * 0

    return f"\n{indent_str}{border}\n" + "\n".join(formatted_lines) + f"\n{indent_str}{border}"


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
        return f"\n{curl_command}\n\n{response_text}"
    return f"\n{curl_command}"
