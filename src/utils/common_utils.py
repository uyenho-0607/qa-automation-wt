import json
import subprocess
import xml.dom.minidom
from collections import Counter
from datetime import datetime, timedelta

from src.core.config_manager import Config
from src.data.consts import ROOTDIR
from src.data.enums import Language
from src.data.project_info import DriverList
from src.utils import DotDict
from src.utils.format_utils import remove_commas
from src.utils.logging_utils import logger


def log_page_source(name="page_source"):
    driver = DriverList.all_drivers[Config.config.platform]
    output_path = ROOTDIR / f'{name}.xml'
    dom = xml.dom.minidom.parseString(driver.page_source)
    pretty_xml = '\n'.join([line for line in dom.toprettyxml(indent="  ").split('\n') if line.strip()])

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)


def get_connected_device(platform=Config.config.get("platform", "android")):
    if platform == "android":
        result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        lines = result.stdout.strip().split('\n')[1:]  # Skip the first line
        for line in lines:
            if line.strip() and 'device' in line:
                return line.split()[0]  # Return the device ID
    else:
        # Not Implement for IOS yet
        pass

    return None


def cook_element(element: tuple, *custom):
    by, ele = element
    # Count the number of {} placeholders in the string
    placeholder_count = ele.count('{}')
    # Create a list of custom values, filling remaining with '{}'
    formatted_custom = list(custom) + ['{}'] * (placeholder_count - len(custom))
    return by, ele.format(*formatted_custom)


def data_testid(testid, tag='*'):
    pattern = f"{tag}[data-testid='{testid}']"
    return pattern


def resource_id(testid, tag='*'):
    pattern = f"//{tag}[@resource-id='{testid}']"
    return pattern


def translate_sign_in(language: Language) -> str:
    translations = {
        "English": "Sign in",
        "简体中文": "登录",
        "繁体中文": "登入",
        "ภาษาไทย": "ลงชื่อเข้าใช้",
        "Tiếng Việt": "Đăng nhập",
        "Melayu": "Log masuk",
        "Bahasa Indonesia": "Masuk",
        "Japanese": "ログイン",
        "Korean": "로그인",
        "Arabic": "تسجيل الدخول.",
    }

    return translations.get(str(language), "Translation not available")


def translate_trade(language: Language) -> str:
    translations = {
        "English": "Logout",
        "简体中文": "登出",
        "繁体中文": "登出",
        "ภาษาไทย": "ออกจากระบบ",
        "Tiếng Việt": "Đăng xuất",
        "Melayu": "Log keluar",
        "Bahasa Indonesia": "Keluar",
        "Japanese": "ログアウト",
        "Korean": "로그아웃",
        "Arabic": "تسجيل الخروج",
    }

    return translations.get(str(language), "Translation not available")


def move_days_from_now(days: int, backward: bool = True, milli_sec: bool = True) -> int:
    """
    Move forward or backward a specific number of days from the current date
    and return a rounded timestamp.
    Args:
        days (int): Number of days to move. Should be positive.
        backward: True to move backward in time, False to move forward
        milli_sec: True if convert the result from sec >> milli_sec
    Returns:
        int: Rounded timestamp in seconds since epoch
    """
    current_time = datetime.now()

    if backward:
        target_date = current_time - timedelta(days=days)
    else:
        target_date = current_time + timedelta(days=days)

    # Convert to timestamp and round to nearest second
    timestamp = int(target_date.timestamp())

    return timestamp * 1000 if milli_sec else timestamp


def compare_dict(
        actual: dict | DotDict,
        expected: dict | DotDict,
        tolerance: float = None,
        tolerance_fields: list[str] = None
):
    """
    Compare two dictionaries with optional tolerance for specified fields.
    
    Args:
        actual: Actual dictionary
        expected: Expected dictionary  
        tolerance: Tolerance value for comparing numbers
        tolerance_fields: List of field names to apply tolerance to
    """
    def _compare_values(actual_val, expected_val, field_name=None):
        """Compare two values with tolerance if applicable"""
        if actual_val == expected_val:
            return True
        
        # Apply tolerance only if specified and field is in tolerance_fields
        if (tolerance is not None and 
            tolerance_fields is not None and
            field_name in tolerance_fields):
            try:
                actual_float = remove_commas(actual_val, to_float=True)
                expected_float = remove_commas(expected_val, to_float=True)
                if abs(actual_float - expected_float) >0:
                    print("different: ", abs(actual_float - expected_float))

                return abs(actual_float - expected_float) <= tolerance
            except (ValueError, TypeError):
                pass
        
        return False
    
    def _dicts_equal(act, exp):
        """Compare two dictionaries with tolerance support"""
        all_res = []
        diff_key = []

        if set(act.keys()) != set(exp.keys()):
            all_res.append(False)
        
        for key in exp:
            val1, val2 = act.get(key, "MISSING"), exp[key]
            res = _compare_values(val1, val2, key)
            all_res.append(res)

            if not res:
                diff_key.append(key)

        return all(all_res), diff_key

    # Find missing and redundant keys
    missing = [key for key in expected.keys() if key not in actual.keys()]
    redundant = [key for key in actual.keys() if key not in expected.keys()]

    # Compare dictionaries with tolerance
    res, diff_key = _dicts_equal(actual, expected)
    return dict(
        res=res and not missing and not redundant,
        missing=missing,
        redundant=redundant,
        diff=[item for item in diff_key if item not in missing + redundant]
    )


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
        actual: str,
        expected: float,
        tolerance_percent: float = 0.01
) -> bool:
    """
    Compare actual and expected values with percentage-based tolerance.
    Args:
        actual: Actual value as string (will be converted to float)
        expected: Expected value as float
        tolerance_percent: Tolerance as percentage (default 1%)
    """
    try:
        actual = float(actual)
        expected = float(expected)
        tolerance = abs(expected) * tolerance_percent if tolerance_percent else 0

        is_within_tolerance = abs(expected - actual) <= tolerance

        logger.debug(f"Expected: {expected}, Actual: {actual}")
        if tolerance_percent:
            logger.debug(f"Tolerance: ±{tolerance:.2f} ({tolerance_percent * 100:.2f}%)")

        return is_within_tolerance

    except ValueError as e:
        logger.error(f"Failed to convert actual value '{actual}' to float: {e}")
        return False


def extract_diff_list(actual: dict, expected: dict, diff_keys: list):
    res = [
        {k: item.get(k, "") for k in diff_keys}  for item in [actual, expected]
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
