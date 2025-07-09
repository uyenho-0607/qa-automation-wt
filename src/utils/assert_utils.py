from typing import Any

import pytest_check as check

from src.core.decorators import attach_table_details
from src.data.project_info import DriverList, StepLogs
from src.utils.allure_utils import attach_screenshot
from src.utils.common_utils import compare_dict, extract_diff_list
from src.utils.format_utils import format_dict_to_string
from src.utils.logging_utils import logger


def check_contain(actual: Any, expected: Any, error_message: str) -> bool:
    """
    Check if actual contains expected value.
    
    Args:
        actual: The actual value to check
        expected: The expected value to find in actual
        error_message: Message to display if check fails
        
    Returns:
        bool: True if check passes, False otherwise
        
    """
    __tracebackhide__ = True

    if isinstance(actual, dict) and isinstance(expected, dict):
        res = check.is_true(expected.items() <= actual.items(), error_message)
        return res

    res = check.is_in(expected, actual, error_message)
    return res


def check_equal(actual: Any, expected: Any, error_message: str) -> bool:
    """
    Check if actual equals expected value.
    
    Args:
        actual: The actual value to check
        expected: The expected value to compare against
        error_message: Message to display if check fails
        
    Returns:
        bool: True if check passes, False otherwise
        
    """
    __tracebackhide__ = True

    res = check.equal(actual, expected, error_message)
    return res


# @attach_table_details
# def soft_assert(
#         actual: Any,
#         expected: Any,
#         check_contains: bool = False,
#         error_message: str = ""
# ) -> bool:
#     """
#     Perform a soft assertion that doesn't stop test execution on failure.
#     Captures screenshots and logs failures for reporting.
#     Args:
#         actual: The actual value to check
#         expected: The expected value to compare against
#         check_contains: If True, uses contains() instead of equal()
#         error_message: Custom error message to display if check fails
#
#     Returns:
#         bool: True if assertion passes, False otherwise
#
#     Raises:
#         TypeError: If actual or expected are None
#     """
#     __tracebackhide__ = True
#
#     if isinstance(actual, dict) and isinstance(expected, dict):
#         logger.debug(f"Compare values: {format_dict_to_string(expected=expected, actual=actual)}")
#         failed_vals: List[str] = []
#
#         # handle log error in case check failed
#         if len(actual) == len(expected):
#             for key in expected:
#                 actual_val = actual.get(key, "")
#                 expected_val = expected.get(key, "")
#                 if actual_val != expected_val:
#                     failed_vals.append(key)
#
#             if failed_vals:
#                 diff_list = [
#                     {key: item.get(key, "") for key in failed_vals}
#                     for item in [actual, expected]
#                 ]
#
#                 error_message = (
#                     f"\n>>> Actual: {format_dict_to_string(diff_list[0])} "
#                     f"\n>>> Expected: {format_dict_to_string(diff_list[-1])}"
#                 )
#         else:
#             error_message = ""
#
#             missing_keys = [k for k in expected if k not in actual]
#             redundant_keys = [k for k in actual if k not in expected]
#
#             missing_message = f"\nMissing keys: {format_dict_to_string({k: expected[k] for k in missing_keys})}"
#             redundant_message = f"\nRedundant keys: {format_dict_to_string({k: actual[k] for k in redundant_keys})}"
#
#             error_message += missing_message if missing_keys else ""
#             error_message += redundant_message if redundant_keys else ""
#
#     else:
#         error_message = error_message or f"\n>>> Actual:   {actual!r} \n>>> Expected: {expected!r}"
#
#     check_func = check_contain if check_contains else check_equal
#     error_message = f"\nValidation Failed ! {check_func.__name__} " + error_message
#
#     res = check_func(actual, expected, error_message)
#     if not res:
#         logger.error(error_message)
#         for driver in DriverList.all_drivers.values():
#             attach_screenshot(driver)
#
#         # save failed verify step
#         if StepLogs.test_steps:
#             failed_step = [item.lower() for item in StepLogs.test_steps if "verify" in item.lower()][-1]
#             StepLogs.all_failed_logs.append((failed_step, error_message))
#
#     return res


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
        tolerance_fields=kwargs.get("tolerance_fields", [])

        if tolerance is not None:
            logger.debug(f"Tolerance: {tolerance * 100}%, apply for fields: {tolerance_fields}")

        res = compare_dict(actual, expected, tolerance=tolerance, tolerance_fields=tolerance_fields)

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

        res = check_equal(res["res"], True, validation_err_msg)

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
            StepLogs.all_failed_logs.append((failed_step, error_message))

    return res
