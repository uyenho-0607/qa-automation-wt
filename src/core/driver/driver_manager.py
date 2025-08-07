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
            case "web" | "web_app":
                _driver = WebDriver.init_driver(
                    browser=kwargs.get("browser", RuntimeConfig.browser),
                    headless=kwargs.get("headless", RuntimeConfig.headless),
                )
                logger.debug(f"- Driver session id: {_driver.session_id!r}")
                return _driver

            case "ios":
                logger.warning("iOS driver initialization not implemented yet")
                return None

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
            case "web" | "web_app":
                WebDriver.quit()

            case "ios":
                logger.warning("iOS driver quit not implemented yet")

            case "android":
                AppiumDriver.quit_android_driver()

            case _:
                raise ValueError(f"Invalid platform: {platform}")
