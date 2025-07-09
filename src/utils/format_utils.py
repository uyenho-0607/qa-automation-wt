import json
import re
from enum import Enum
from typing import Dict, Any

from requests import Response

from src.utils.logging_utils import logger


def locator_format(value: str):
    """return the string as locator format: EX: Good Till Cancelled -> good-till-cancel"""
    return value.lower().replace(" ", "-").lower()


def is_integer(s):
    try:
        int(s)
        return True
    except (ValueError, TypeError):
        return False


def is_float(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False


def get_asset_tab_number(text: str) -> int | None:
    """Extract number from text, Example: "Open Position (13)" 13"""
    match = re.search(r"\((\d+)\)", text)
    return int(match.group(1)) if match else 0


def get_decimal_places(number):
    """ Return the decimal places: EX: 123 >> 0, 123.10 >> 2, 123.123 >> 3"""
    decimal_places = 0

    if "." in str(number):
        decimal_places = len(str(number).split(".")[-1])

    return decimal_places


def remove_commas(input_str: str, to_float: bool = False) -> float | int | str:
    """Remove commas from a string and return a float or int if possible."""
    # Remove commas from string
    res = str(input_str).replace(",", "")
    if to_float:
        try:
            res = float(res)

        except (ValueError, TypeError):
            res = input_str

    return res


def format_with_decimal(num_to_convert: int | float, decimal_places: float | str) -> str:
    """Add specific decimal places based on decimal_places: number = 123.1, decimal_places = 1.12 >> number = 123.10"""
    if isinstance(num_to_convert, str):
        return num_to_convert

    decimal_places = len(str(decimal_places).split(".")[-1])
    return f"{num_to_convert:.{decimal_places}f}"


def add_commas(number: float | int | str, decimal_places: int = None) -> str:
    """
    Format a number with commas as thousand separators and specified decimal places.
    """
    if is_float(number) or is_integer(number):
        decimal_places = decimal_places or get_decimal_places(number)
        number = remove_commas(number, to_float=True)
        format_str = "{:,.%df}" % decimal_places
        return format_str.format(number)

    return number


def format_prices(prices, decimal: int = None):
    """
    Format all prices value back to one general format for more stable
    Sample: 1,234.10
    """
    # decimal = decimal or ObjectTrade.DECIMAL
    prices = prices if isinstance(prices, list) else [prices]
    res = []
    logger.debug(f"Formating number: {prices}")
    # Add comas if not yet - convert to float
    for price in prices:
        price = add_commas(price)
        if not price or price == "--":
            price = price

        else:
            # add missing zero if any
            cur_decimal_places = get_decimal_places(price)
            if decimal != cur_decimal_places:
                # Format the value to match the decimal places
                if "." not in str(price):
                    price = str(price) + "."

                price = str(price) + "0" * (decimal - cur_decimal_places)

        res.append(price)

    return res if len(prices) > 1 else res[0]


def format_acc_balance(value: str, to_float=True):
    res = value.replace("$", "").replace(",", "").replace("+", "").replace("%", "")
    if to_float:
        res = float(res)
    return res


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
