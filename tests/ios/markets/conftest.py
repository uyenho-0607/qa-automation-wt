import pytest

from src.core.driver.appium_driver import AppiumDriver
from src.core.driver.driver_manager import DriverManager
from src.core.page_container.ios_container import iOSContainer
from src.utils.logging_utils import logger


@pytest.fixture(scope="package")
def ios():
    """
    Fixture to initialize and provide page objects for login tests.
    Handles driver setup and cleanup.
    """
    logger.info("Initializing ios driver")
    DriverManager.get_driver()

    yield iOSContainer()

    logger.info("Cleaning up ios driver")
    DriverManager.quit_driver()

    logger.info("- Stop Appium service")
    AppiumDriver.stop_appium_service()


@pytest.fixture(scope="package", autouse=True)
def setup_markets_test(ios):
    logger.info(f"- Perform Login")
    ios.login_screen.login()
