import re
from typing import Any

import pytest_check as check

from src.core.decorators import attach_table_details
from src.data.objects.trade_object import ObjectTrade
from src.data.project_info import DriverList, StepLogs
from src.utils import DotDict
from src.utils.allure_utils import attach_screenshot
from src.utils.format_utils import format_dict_to_string, remove_comma, format_str_price
from src.utils.logging_utils import logger

"""Utilities"""


def compare_dict_with_keymap(actual, expected, key: str, tolerance=None):
    actual_map = {item[key]: item for item in actual}
    expected_map = {item[key]: item for item in expected}

    all_keys = set(actual_map) | set(expected_map)
    mismatches = []
    missing = []
    redundant = []

    for k in all_keys:
        a_item = actual_map.get(k)
        e_item = expected_map.get(k)

        if a_item and e_item:
            a_filtered = {ka: va for ka, va in a_item.items() if ka != key}
            e_filtered = {ke: ve for ke, ve in e_item.items() if ke != key}

            actual_diff = {}
            expected_diff = {}

            for subkey in e_filtered:
                va = a_filtered.get(subkey)
                ve = e_filtered.get(subkey)

                if tolerance is not None:
                    delta = round(abs(va - ve), ndigits=4)
                    if delta <= tolerance:
                        if delta:
                            logger.debug(f"- Acceptable tolerance: {delta!r}")
                        continue

                if va != ve:
                    actual_diff[subkey] = va
                    expected_diff[subkey] = ve

            if actual_diff:
                mismatches.append({
                    key: k,
                    'actual': actual_diff,
                    'expected': expected_diff
                })

        elif e_item and not a_item:
            missing.append(k)

        elif a_item and not e_item:
            redundant.append(k)

    return {
        'result': not mismatches and not missing and not redundant,
        'mismatches': mismatches,
        'missing': missing,  # expected but not in actual
        'redundant': redundant  # in actual but not in expected
    }


def compare_with_tolerance(
        actual: str | float,
        expected: str | float,
        tolerance_percent: float = 0.01,
        get_diff: bool = False
) -> bool | dict:
    """
    Compare actual and expected values with percentage-based tolerance.
    Args:
        actual: Actual value as string (will be converted to float)
        expected: Expected value as float
        tolerance_percent: Tolerance as percentage (default 1%)
        get_diff: Get full dict result of different information
    """

    actual = remove_comma(actual)
    expected = remove_comma(expected)
    tolerance = tolerance_percent * expected

    diff = abs(actual - expected)
    diff_percent = diff / expected if expected else 0

    if diff:
        logger.debug(f"Expected: {expected}, Actual: {actual}, Tolerance: ±{tolerance:.2f} ({tolerance_percent:.2f}%), Diff: {diff:.4f}, Diff Percent: {diff_percent:.4f}")

    else:
        logger.debug(f"Actual {actual!r} and expected {expected!r} are the same")

    res = diff_percent <= tolerance_percent

    return res if not get_diff else dict(res=res, diff=f"{diff:.4f}", diff_percent=f"{diff_percent:.4f}", tolerance=f"±{tolerance:.2f} ({tolerance_percent:.2f}%)")


def compare_dict(
        actual: dict | DotDict,
        expected: dict | DotDict,
        tolerance_percent: float = None,
        tolerance_fields: list[str] = None
):
    """
    Compare two dictionaries with optional tolerance for specified fields.
    Args:
        actual: Actual dictionary
        expected: Expected dictionary
        tolerance_percent: Tolerance percent value for comparing numbers
        tolerance_fields: List of field names to apply tolerance to
    """

    all_res = []
    diff_keys = []
    tolerance_info = {}

    # compare if length of two dicts are the same
    all_res.append(set(actual.keys()) == set(expected.keys()))

    for key in expected:
        act, exp = actual.get(key, "MISSING"), expected[key]

        if tolerance_percent is not None and key in tolerance_fields:
            res_tolerance = compare_with_tolerance(act, exp, tolerance_percent, get_diff=True)
            res = res_tolerance["res"]
            tolerance_info[key] = dict(diff_percent=res_tolerance["diff_percent"], tolerance=res_tolerance["tolerance"])

        else:
            res = act == exp

        all_res.append(res)
        if not res:
            diff_keys.append(key)

    # Find missing and redundant keys
    missing = [key for key in expected.keys() if key not in actual.keys()]
    redundant = [key for key in actual.keys() if key not in expected.keys()]

    res_dict = dict(
        res=all(all_res) and not missing and not redundant,
        missing=missing,
        redundant=redundant,
        diff=[item for item in diff_keys if item not in missing + redundant]
    )

    if tolerance_percent and tolerance_fields:
        res_dict |= {"tolerance_info": tolerance_info}

    return res_dict


def extract_diff_list(actual: dict, expected: dict, diff_keys: list):
    res = [
        {k: item.get(k, "") for k in diff_keys} for item in [actual, expected]
    ]
    return res


def extract_diff_key(actual: dict, expected: dict):
    res = {}
    all_keys = set(actual.keys()) | set(expected.keys())

    for key in all_keys:
        if actual[key] != expected[key]:
            diff = {key: dict(actual=actual[key], expected=expected[key])}
            res |= diff

    return res


"""Notification
----------------------------
Notification Sample
1. Banner
- XRPUSD.std - BUY ORDER placed, Size: 1 / Units: 1,000. Stop Loss: 2.5649. Take Profit: 2.5895.
- XRPUSD.std - BUY LIMIT ORDER placed, Size: 1 / Units: 1,000. Price: 2.2000. Stop Loss: 2.1877. Take Profit: 2.2123.
- ETH.USD - BUY STOP LIMIT ORDER placed, Volume: 0.1 / Units: 0.1. Stop Limit Price: 2,993.22. Price: 2,994.18. Stop Loss: 2,991.99. Take Profit: 2,994.45.
- ETH.USD - BUY ORDER updated, Volume: 9 / Units: 9. Entry Price: 2,520.70. Stop Loss: 2,994.23. Take Profit: 2,996.69.

2. Details
- Open Position: Open Position: #8526920 AUDNZD.std: Size 0.02 / Units 2,000 @ 1.07698 
- Position Closed: #7592152 DASHUSD.std: Size 0.02 / Units 0.2 @ 19.92, Loss of -1.82
"""

def extract_noti_prices(noti_content: str) -> dict:
    """Extract price value from notification text."""
    # Pattern to match price after @ symbol (most common case)
    price_patterns = [
        r'@\s*([\d,]+\.?\d*)',  # Price after @ symbol (handles commas)
        r'Price:\s*([\d,]+\.?\d*)',  # Price after "Price:" (handles commas)
        r'Entry Price:\s*([\d,]+\.?\d*)',  # Entry Price (handles commas)
        r'Stop Loss:\s*([\d,]+\.?\d*)',  # Stop Loss (handles commas)
        r'Take Profit:\s*([\d,]+\.?\d*)',  # Take Profit (handles commas)
        r'Stop Limit Price:\s*([\d,]+\.?\d*)',  # Stop Limit Price (handles commas)
    ]

    res = {}

    for pattern in price_patterns:
        match = re.search(pattern, noti_content)
        if match:
            try:
                # Remove commas before converting to float
                price_str = match.group(1).replace(',', '')

                key = "entry_price" if "@" in match.group(0) else match.group(0).split(": ")[0].lower().replace(" ", "_")
                res[key] = float(price_str)


            except ValueError:
                continue
    return res


def compare_noti_with_tolerance(
        actual: str,
        expected: str,
        tolerance_percent: float = 0.5,
        is_banner=True
):
    """Compare notification messages with tolerance for price values."""
    # Extract prices from both messages
    actual_price = extract_noti_prices(actual)
    expected_price = extract_noti_prices(expected)
    desc = ""
    decimal = ObjectTrade.DECIMAL if is_banner else None

    if actual_price and expected_price:
        res = compare_dict(actual_price, expected_price, tolerance_percent=tolerance_percent, tolerance_fields=["stop_loss", "take_profit", "entry_price"])["res"]
        if res:
            desc += f"Tolerance: {tolerance_percent}% - \n"
            # Replace price in expected with actual price for string comparison
            pattern_key_mapping = {
                r'@\s*[\d,]+\.?\d*': 'entry_price',
                r'Entry Price:\s*[\d,]+\.?\d*': 'entry_price',
                r'Stop Loss:\s*[\d,]+\.?\d*': 'stop_loss',
                r'Take Profit:\s*[\d,]+\.?\d*': 'take_profit'
            }

            processed_keys = set()  # Track which keys have been processed

            for pattern, key in pattern_key_mapping.items():
                if key in expected_price and key in actual_price and key not in processed_keys:
                    # Only update if prices are different (within tolerance but not exactly the same)
                    if abs(actual_price[key] - expected_price[key]) > 0:

                        logger.debug(f"- Updating {key}: {expected_price[key]} -> {actual_price[key]}")
                        expected = re.sub(pattern, lambda m: m.group(0).replace(
                            re.search(r'[\d,]+\.?\d*', m.group(0)).group(0),
                            format_str_price(actual_price[key], decimal)
                        ), expected)
                    else:
                        logger.debug(f"- Skipping {key}: values are identical ({actual_price[key]})")
                    
                    processed_keys.add(key)  # Mark this key as processed

                    desc += f"Update price: {key}, from {expected_price[key]} -> {actual_price[key]}\n"

            logger.debug(f"- Expected noti after adjust prices: {expected!r}")

    soft_assert(actual, expected, log_details=True, desc=desc)


"""Assertion"""


def check_contain(actual: Any, expected: Any, error_message: str) -> bool:
    """Check if actual contains expected value."""
    __tracebackhide__ = True

    if isinstance(actual, dict) and isinstance(expected, dict):
        res = check.is_true(expected.items() <= actual.items(), error_message)
        return res

    res = check.is_in(expected, actual, error_message)
    return res


def check_equal(actual: Any, expected: Any, error_message: str) -> bool:
    """Check if actual equals expected value."""
    __tracebackhide__ = True

    res = check.equal(actual, expected, error_message)
    return res


@attach_table_details
def soft_assert(
        actual: Any,
        expected: Any,
        check_contains: bool = False,
        error_message: str = "",
        **kwargs
) -> bool:
    """
    Perform a soft assertion that doesn't stop test execution on failure.
    Captures screenshots and logs failures for reporting.
    Args:
        actual: The actual value to check
        expected: The expected value to compare against
        check_contains: If True, uses contains() instead of equal()
        error_message: Custom error message to display if check fails
    Returns:
        bool: True if assertion passes, False otherwise
    Raises:
        TypeError: If actual or expected are None
    """
    __tracebackhide__ = True

    check_func = check_contain if check_contains else check_equal
    validation_err_msg = f"\nValidation Failed ! {check_func.__name__.replace('_', ' ').upper()} "

    if isinstance(actual, dict) and isinstance(expected, dict):
        logger.debug(f"Compare values: {format_dict_to_string(expected=expected, actual=actual)}")

        tolerance = kwargs.get("tolerance")
        tolerance_fields = kwargs.get("tolerance_fields", [])

        if tolerance is not None and tolerance_fields:
            logger.debug(f"Tolerance: {tolerance}%, apply for fields: {tolerance_fields}")

        res = compare_dict(actual, expected, tolerance_percent=tolerance, tolerance_fields=tolerance_fields)

        if res["missing"]:
            validation_err_msg += f"\n>>> Missing Fields: {res['missing']}"

        if res["redundant"]:
            validation_err_msg += f"\n>>> Redundant Fields: {res['redundant']}"

        if res["diff"]:
            diff_list = extract_diff_list(actual, expected, res["diff"])
            validation_err_msg += (
                f"\n>>> Different Fields: "
                f"\nActual: {format_dict_to_string(diff_list[0])} "
                f"\nExpected: {format_dict_to_string(diff_list[-1])}"
            )

        assertion_result = check_equal(res["res"], True, validation_err_msg)

        # Handle error logging and screenshot capture
        if not assertion_result:
            logger.error(validation_err_msg)
            for driver in DriverList.all_drivers.values():
                attach_screenshot(driver)

            # save failed verify step
            if StepLogs.test_steps:
                failed_step = [item.lower() for item in StepLogs.test_steps if "verify" in item.lower()][-1]
                StepLogs.all_failed_logs.append((failed_step, validation_err_msg))

        # Return the comparison result for the decorator to use
        return res

    else:
        validation_err_msg += (error_message or f"\n>>> Actual:   {actual!r} \n>>> Expected: {expected!r}")
        res = check_func(actual, expected, validation_err_msg)

        if not res:
            logger.error(validation_err_msg)
            for driver in DriverList.all_drivers.values():
                attach_screenshot(driver)

            # save failed verify step
            if StepLogs.test_steps:
                failed_step = [item.lower() for item in StepLogs.test_steps if "verify" in item.lower()][-1]
                StepLogs.all_failed_logs.append((failed_step, validation_err_msg))

        return res
