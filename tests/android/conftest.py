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


@pytest.fixture
def cancel_delete_order(android):
    yield
    android.trade_screen.modals.cancel_delete_order()


@pytest.fixture
def cancel_bulk_delete(android):
    yield
    android.trade_screen.modals.cancel_bulk_delete()


@pytest.fixture
def cancel_bulk_close(android):
    yield
    android.trade_screen.modals.cancel_bulk_close()


@pytest.fixture
def cancel_edit_order(android):
    yield
    android.trade_screen.modals.cancel_edit_order()
