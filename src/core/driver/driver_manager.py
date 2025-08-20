from typing import Any

from src.core.driver.appium_driver import AppiumDriver
from src.core.driver.web_driver import WebDriver
from src.data.project_info import RuntimeConfig
from src.utils.logging_utils import logger


class DriverManager:

    @classmethod
    def get_driver(cls, platform=None, **kwargs) -> Any:
        """
        Get a driver instance for the specified platform.
        """
        platform = platform or RuntimeConfig.platform
        match platform.lower():
            case "web" | "web-app":
                _driver = WebDriver.init_driver(
                    browser=kwargs.get("browser", RuntimeConfig.browser),
                    headless=kwargs.get("headless", RuntimeConfig.headless),
                    enable_cdp=True
                )
                logger.debug(f"- Driver session id: {_driver.session_id!r}")
                return _driver

            case "ios":
                _driver = AppiumDriver.init_ios_driver()
                logger.debug(f"- Driver session id: {_driver.session_id!r}")
                return _driver

            case "android":
                _driver = AppiumDriver.init_android_driver()
                logger.debug(f"- Driver session id: {_driver.session_id!r}")
                return _driver

            case _:
                raise ValueError(f"Invalid platform: {platform}")

    @classmethod
    def quit_driver(cls, platform=None):
        platform = platform or RuntimeConfig.platform
        match platform.lower():
            case "web" | "web-app":
                WebDriver.quit()

            case "ios":
                AppiumDriver.quit_mobile_driver("ios")

            case "android":
                AppiumDriver.quit_mobile_driver("android")

            case _:
                raise ValueError(f"Invalid platform: {platform}")
