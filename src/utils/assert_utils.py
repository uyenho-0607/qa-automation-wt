from typing import Any

import pytest_check as check

from src.data.project_info import StepLogs
from src.utils import DotDict
from src.utils.logging_utils import logger

"""Utilities"""


def compare_dict_with_keymap(actual, expected, key: str = 'chart_time', tolerance_percent=0.1):
    act_chart_time = [item['chartTime'] for item in actual]
    exp_chart_time = [item['chartTime'] for item in expected]

    # 1. Check missing dataset
    missing = [item for item in exp_chart_time if item not in act_chart_time]
    # 2. Check redundant dataset
    redundant = [item for item in act_chart_time if item not in exp_chart_time]

    # 3. Compare values between 2 dataset
    actual_map = {item[key]: item for item in actual}
    expected_map = {item[key]: item for item in expected}
    all_keys = set(actual_map) | set(expected_map)

    mismatches = []

    for k in all_keys:
        a_item = actual_map.get(k)
        e_item = expected_map.get(k)

        if a_item and e_item:
            # filter out the actual and expected value without chart_time
            a_filtered = {k: v for k, v in a_item.items() if k != key}
            e_filtered = {k: v for k, v in e_item.items() if k != key}

            actual_diff = {}
            expected_diff = {}

            res_dict = compare_dict(a_filtered, e_filtered, tolerance_percent=tolerance_percent, tolerance_fields=["close", "high", "low", "open"])

            if not res_dict['res']:
                for diff in res_dict['diff']:
                    actual_diff[diff] = a_filtered.get(diff)
                    expected_diff[diff] = e_filtered.get(diff)

            if actual_diff:
                mismatches.append({
                    key: k,
                    'actual': actual_diff,
                    'expected': expected_diff
                })

    return dict(
        # res=not missing and not mismatches and not redundant,
        res=not missing and not mismatches,  # skip checking redundant data for now
        mismatches=mismatches,
        missing=missing,
        redundant=redundant
    )


def compare_with_tolerance(
        actual: str | float,
        expected: str | float,
        tolerance_percent: float = 0.1,
) -> dict:
    """
    Compare actual and expected values with percentage-based tolerance.
    Args:
        actual: Actual value as string (will be converted to float)
        expected: Expected value as string or float
        tolerance_percent: Tolerance as percentage (e.g., 0.5 means 0.5%)
    """
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
    # if diff:
    #     logger.debug(f"Expected: {expected}, Actual: {actual}, Tolerance: ±{tolerance_value:.6f} ({tolerance_percent}%), Diff: {diff:.6f}, Diff Percent: {diff_percent:.6f}%")

    res = abs(diff) <= abs(tolerance_value)

    return dict(
        res=res,
        diff=f"{diff:.4f}",
        diff_percent=f"{diff_percent:.4f}",
        tolerance=f"±{tolerance_value:.2f} ({tolerance_percent:.2f}%)"
    )


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
            res_tolerance = compare_with_tolerance(act, exp, tolerance_percent)
            res = res_tolerance["res"]
            tolerance_info[key] = dict(diff_percent=res_tolerance["diff_percent"], tolerance=res_tolerance["tolerance"])

        else:
            res = act == exp

        all_res.append(res)
        if not res:
            diff_keys.append(key)

    res_dict = dict(
        res=all(all_res),
        diff=[item for item in diff_keys]
    )

    if tolerance_percent and tolerance_fields:
        res_dict |= {"tolerance_info": tolerance_info}

    return res_dict


def soft_assert(
        actual: Any,
        expected: Any,
        error_message: str = "",
) -> bool:
    """
    Perform a soft assertion that doesn't stop test execution on failure.
    Args:
        actual: The actual value to check
        expected: The expected value to compare against
        error_message: Custom error message to display if check fails
    Returns:
        bool: True if assertion passes, False otherwise
    """
    __tracebackhide__ = True

    validation_err_msg = f"\nValidation Failed ! " + (error_message or f"\n>>> Actual:   {actual!r} \n>>> Expected: {expected!r}")
    res = check.equal(actual, expected, validation_err_msg)

    if not res:
        logger.error(validation_err_msg)
        # save failed verify step
        if StepLogs.test_steps:
            # save failed verify step
            if StepLogs.test_steps:
                failed_step = [item.lower() for item in StepLogs.test_steps if "verify" in item.lower()][-1]
                failed_step in StepLogs.all_failed_logs or StepLogs.add_failed_log(failed_step, "")

    return res
