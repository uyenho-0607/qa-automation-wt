import pytest

from src.core.actions.mobile_actions import MobileActions
from src.core.driver.appium_driver import AppiumDriver
from src.core.driver.driver_manager import DriverManager
from src.core.page_container.android_container import AndroidContainer
from src.utils.logging_utils import logger


@pytest.fixture(scope="package")
def android():

    logger.info("- Init Android driver")
    DriverManager.get_driver()
    actions = MobileActions()

    yield AndroidContainer(actions)

    logger.info("- Clean up Android driver")
    DriverManager.quit_driver()
    
    logger.info("- Stop Appium service")
    AppiumDriver.stop_appium_service()


@pytest.fixture(scope="package", autouse=True)
def setup_markets_test(android):

    logger.info(f"- Perform Login")
    android.login_screen.login()
