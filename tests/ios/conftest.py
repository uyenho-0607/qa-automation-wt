import pytest

from src.core.actions.mobile_actions import MobileActions
from src.core.driver.appium_driver import AppiumDriver
from src.core.driver.driver_manager import DriverManager
from src.core.page_container.ios_container import iOSContainer
from src.utils.logging_utils import logger


@pytest.fixture(scope="package")
def ios():
    logger.info("- Init ios driver")
    DriverManager.get_driver()
    actions = MobileActions()

    yield iOSContainer(actions)

    logger.info("- Clean up ios driver")
    DriverManager.quit_driver()

    logger.info("- Stop Appium service")
    AppiumDriver.stop_appium_service()


@pytest.fixture
def cancel_delete_order(ios):
    yield
    ios.trade_screen.modals.cancel_delete_order()


@pytest.fixture
def cancel_bulk_delete(ios):
    yield
    ios.trade_screen.modals.cancel_bulk_delete()


@pytest.fixture
def cancel_bulk_close(ios):
    yield
    ios.trade_screen.modals.cancel_bulk_close()


@pytest.fixture
def cancel_edit_order(ios):
    yield
    ios.trade_screen.modals.cancel_edit_order()
