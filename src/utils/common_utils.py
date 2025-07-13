import subprocess
import xml.dom.minidom
from datetime import datetime, timedelta

from src.core.config_manager import Config
from src.data.consts import ROOTDIR
from src.data.enums import Language
from src.data.project_info import DriverList


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


