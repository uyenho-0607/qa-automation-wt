import pytest

from src.core.driver.appium_driver import AppiumDriver
from src.core.driver.driver_manager import DriverManager
from src.core.page_container.android_container import AndroidContainer
from src.utils.logging_utils import logger


@pytest.fixture
def android():
    """
    Fixture to initialize and provide page objects for login tests.
    Handles driver setup and cleanup.
    """
    logger.info("Initializing Android driver")
    DriverManager.get_driver()
    # actions = MobileActions()

    yield AndroidContainer()

    logger.info("Cleaning up Android driver")
    DriverManager.quit_driver()


@pytest.fixture(scope="package", autouse=True)
def stop_appium_service():
    yield
    AppiumDriver.stop_appium_service()
