import operator
import re
from typing import Any

import pytest_check as check

from src.core.decorators import attach_table_details
from src.data.consts import FAILED_ICON_COLOR
from src.data.objects.trade_obj import ObjTrade
from src.data.project_info import DriverList, StepLogs
from src.utils import DotDict
from src.utils.allure_utils import attach_screenshot
from src.utils.format_utils import format_dict_to_string, remove_comma, format_str_price, is_float
from src.utils.logging_utils import logger

"""Utilities"""


def compare_with_tolerance(
        actual: str | float,
        expected: str | float,
        tolerance_percent: float = 0.1,
        get_diff: bool = False
) -> bool | dict:
    """
    Compare actual and expected values with percentage-based tolerance.
    Args:
        actual: Actual value as string (will be converted to float)
        expected: Expected value as string or float
        tolerance_percent: Tolerance as percentage (e.g., 0.5 means 0.5%)
        get_diff: Get full dict result of different information
    """
    actual = remove_comma(actual)
    expected = remove_comma(expected)

    if not is_float(expected) or not is_float(actual):
        logger.debug(f"- Expected/ Actual value is not in correct type, expected: {expected} - type: {type(expected)}, actual: {actual} - type: {type(actual)}")
        return False if not get_diff else dict(res=False, diff="", diff_percent="", tolerance="")

    actual = float(actual)
    expected = float(expected)

    diff = abs(actual - expected)
    tol_frac = tolerance_percent / 100.0  # convert percent to fraction

    if expected != 0:
        baseline = abs(expected)
        diff_percent = diff / baseline  # fraction (e.g., 0.005 = 0.5%)
        tolerance_value = tol_frac * baseline

    else:
        # expected is zero: only allow exact match
        if diff == 0:
            diff_percent = 0.0
        else:
            diff_percent = float("inf")
        tolerance_value = 0.0

    # convert to percent for human-readable
    diff_percent = diff_percent * 100
    res = abs(diff) <= abs(tolerance_value)

    if diff and not res:
        logger.warning(f"Expected: {expected}, Actual: {actual}, Tolerance: ±{tolerance_value:.6f} ({tolerance_percent}%), Diff: {diff:.6f}, Diff Percent: {diff_percent:.6f}%")

    return res if not get_diff else dict(
        res=res,
        diff=f"{diff:.4f}",
        diff_percent=f"{diff_percent:.4f}",
        tolerance=f"±{tolerance_value:.2f} ({tolerance_percent:.2f}%)"
    )


def compare_dict(
        actual: dict | DotDict,
        expected: dict | DotDict,
        tolerance_percent: float = None,
        tolerance_fields: list[str] = None,
        field_tolerances: dict[str, float] = None,
        cus_operator = None
):
    """
    Compare two dictionaries with optional tolerance for specified fields.
    Args:
        actual: Actual dictionary
        expected: Expected dictionary
        tolerance_percent: Global tolerance percent value for comparing numbers
        tolerance_fields: List of field names to apply global tolerance to
        field_tolerances: Dictionary mapping field names to specific tolerance percentages
                         e.g., {'price': 0.1, 'volume': 0.5} - overrides global tolerance
        cus_operator: custom compare operator
    """

    all_res = []
    diff_keys = []
    tolerance_info = {}

    logger.debug(f"- Compare dict: {format_dict_to_string(expected=expected, actual=actual)}")
    # compare if length of two dicts are the same
    all_res.append(set(actual.keys()) == set(expected.keys()))

    for key in expected:
        act, exp = actual.get(key, "MISSING"), expected[key]

        # Check if field has specific tolerance
        if field_tolerances and key in field_tolerances:
            field_tolerance = field_tolerances[key]
            res_tolerance = compare_with_tolerance(act, exp, field_tolerance, get_diff=True)
            res = res_tolerance["res"]
            tolerance_info[key] = dict(diff_percent=res_tolerance["diff_percent"], tolerance=res_tolerance["tolerance"])

        # Check if field should use global tolerance
        elif tolerance_percent is not None and tolerance_fields and key in tolerance_fields:
            res_tolerance = compare_with_tolerance(act, exp, tolerance_percent, get_diff=True)
            res = res_tolerance["res"]
            tolerance_info[key] = dict(diff_percent=res_tolerance["diff_percent"], tolerance=res_tolerance["tolerance"])

        else:
            res = act == exp if not cus_operator else cus_operator(act, exp)

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

    if (tolerance_percent and tolerance_fields) or field_tolerances:
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
    price_patterns = [
        r'@\s*([\d,]+\.?\d*)',  # Price after @ symbol
        r'\.\s+Price:\s*([\d,]+\.?\d*)',  # Exact ". Price:"
        r'Entry Price:\s*([\d,]+\.?\d*)',
        r'Stop Loss:\s*([\d,]+\.?\d*)',
        r'Take Profit:\s*([\d,]+\.?\d*)',
        r'Stop Limit Price:\s*([\d,]+\.?\d*)',
    ]

    res = {}

    for pattern in price_patterns:
        match = re.search(pattern, noti_content)
        if match:
            try:
                price_str = match.group(1).replace(',', '')

                raw_key = match.group(0).split(":")[0]
                raw_key = raw_key.strip().lstrip(".").strip()  # remove leading period if present
                key = "entry_price" if "@" in match.group(0) else raw_key.lower().replace(" ", "_")

                res[key] = float(price_str)
            except ValueError:
                continue

        # Remove duplicate "price" if "entry_price" exists
        if "price" in res and "entry_price" in res:
            res.pop("price", None)

    return res


def compare_noti_with_tolerance(
        actual: str,
        expected: str,
        tolerance_percent: float = 1,
        is_banner=True
):
    """Compare notification messages with tolerance for price values."""
    # Extract prices from both messages
    actual_price = extract_noti_prices(actual)
    expected_price = extract_noti_prices(expected)
    decimal = ObjTrade.DECIMAL if is_banner else None

    if actual_price and expected_price:
        compare_result = compare_dict(actual_price, expected_price, tolerance_percent=tolerance_percent, tolerance_fields=["stop_loss", "take_profit", "entry_price", "price"])
        res = compare_result["res"]

        if res:
            # Replace price in expected with actual price for string comparison
            pattern_key_mapping = {
                r'@\s*[\d,]+\.?\d*': 'entry_price',
                r'Entry Price:\s*[\d,]+\.?\d*': 'entry_price',
                r'\.\s+Price:\s*([\d,]+\.?\d*)': 'price',
                r'Stop Loss:\s*[\d,]+\.?\d*': 'stop_loss',
                r'Take Profit:\s*[\d,]+\.?\d*': 'take_profit'
            }

            for pattern, key in pattern_key_mapping.items():
                if key in expected_price and key in actual_price:
                    # Only update if prices are different (within tolerance but not exactly the same)
                    if abs(actual_price[key] - expected_price[key]) > 0:
                        logger.debug(f"- Updating {key}: {expected_price[key]} -> {actual_price[key]}")
                        expected = re.sub(pattern, lambda m: m.group(0).replace(
                            re.search(r'[\d,]+\.?\d*', m.group(0)).group(0),
                            format_str_price(actual_price[key], decimal)
                        ), expected)

    soft_assert(actual, expected, log_details=True)


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
) -> dict[str, bool | list[Any]] | bool:
    """
    Perform a soft assertion that doesn't stop test execution on failure.
    Captures screenshots and logs failures for reporting.
    Args:
        actual: The actual value to check
        expected: The expected value to compare against
        check_contains: If True, uses contains() instead of equal()
        error_message: Custom error message to display if check fails
        **kwargs: Additional parameters including:
            - tolerance: Global tolerance percentage for numeric fields
            - tolerance_fields: List of field names to apply global tolerance to
            - field_tolerances: Dict mapping field names to specific tolerance percentages
    Returns:
        bool: True if assertion passes, False otherwise
    Raises:
        TypeError: If actual or expected are None
    """
    __tracebackhide__ = True

    check_func = check_contain if check_contains else check_equal
    validation_err_msg = f"\n {FAILED_ICON_COLOR} Validation Failed ! "
    tolerance = kwargs.get("tolerance")
    tolerance_fields = kwargs.get("tolerance_fields", [])
    field_tolerances = kwargs.get("field_tolerances")
    cus_operator = kwargs.get("cus_operator")

    if isinstance(actual, dict) and isinstance(expected, dict):
        if check_contains:
            actual = {k: v for k, v in actual.items() if k in expected}

        if tolerance is not None and tolerance_fields:
            logger.debug(f"Global tolerance: {tolerance}%, apply for fields: {tolerance_fields}")

        if field_tolerances:
            logger.debug(f"Field-specific tolerances: {field_tolerances}")

        res = compare_dict(actual, expected, cus_operator=cus_operator, tolerance_percent=tolerance, tolerance_fields=tolerance_fields, field_tolerances=field_tolerances)

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
                StepLogs.add_failed_log(failed_step, validation_err_msg)

        # Return the comparison result for the decorator to use
        return res

    else:
        validation_err_msg += (error_message or f"\n>>> Actual:   {actual!r} \n>>> Expected: {expected!r}")
        res = check_func(actual, expected, validation_err_msg) if not tolerance else compare_with_tolerance(actual, expected, tolerance)

        if not res:
            logger.error(validation_err_msg)
            for driver in DriverList.all_drivers.values():
                attach_screenshot(driver)

            # save failed verify step
            if StepLogs.test_steps:
                failed_step = [item.lower() for item in StepLogs.test_steps if "verify" in item.lower()][-1]
                StepLogs.add_failed_log(failed_step, validation_err_msg)

        return res
