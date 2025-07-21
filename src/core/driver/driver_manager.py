from typing import Any
from src.core.config_manager import Config
from src.core.driver.appium_driver import AppiumDriver
from src.core.driver.web_driver import WebDriver
from src.utils.logging_utils import logger


class DriverManager:

    @classmethod
    def get_driver(cls, platform=None, **kwargs) -> Any:
        """
        Get a driver instance for the specified platform.
        """
        platform = platform or Config.config.get("platform", "web")
        match platform.lower():
            case "web":
                _driver = WebDriver.init_driver(
                    browser=kwargs.get("browser", Config.config.browser),
                    headless=kwargs.get("headless", Config.config.headless),
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
        platform = platform or Config.config.get("platform")
        match platform.lower():
            case "web":
                WebDriver.quit()

            case "ios":
                logger.warning("iOS driver quit not implemented yet")

            case "android":
                AppiumDriver.quit_android_driver()

            case _:
                raise ValueError(f"Invalid platform: {platform}")
