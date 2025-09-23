import pytest

from src.data.project_info import RuntimeConfig
from src.core.driver.driver_manager import DriverManager
from src.core.driver.appium_driver import AppiumDriver
from src.core.page_container.ios_container import iOSContainer
from src.utils.logging_utils import logger


@pytest.fixture(scope="package")
def ios():
    logger.info("- Init ios driver")
    DriverManager.get_driver()

    yield iOSContainer()

    logger.info("- Clean up ios driver")
    DriverManager.quit_driver()

    logger.info("- Stop Appium service")
    AppiumDriver.stop_appium_service()

@pytest.fixture(scope="package", autouse=True)
def setup_login_test(ios):
    if not RuntimeConfig.argo_cd:
        # currently, cannot reset login state of app -> temporarily check if app is logged in -> perform logout
        if ios.home_screen.on_home_screen():
            logger.info("- App is logged in, logout first", setup=True)
            ios.home_screen.settings.logout()