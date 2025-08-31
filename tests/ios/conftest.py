import pytest

from src.core.driver.appium_driver import AppiumDriver
from src.core.driver.driver_manager import DriverManager
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


@pytest.fixture(scope="package")
def login_wt_app(ios):
    # Check current app state
    is_logged_in = ios.home_screen.wait_for_loaded()
    if is_logged_in:
        return
        logger.info("- Logout first")
        ios.home_screen.settings.logout()

    max_retries = 3

    logger.info("- Login to WT app")
    ios.login_screen.login(wait=True)

    logger.info("- Wait for home screen loaded")
    while not ios.home_screen.wait_for_loaded() and max_retries:
        max_retries -= 1

        logger.info(f"- Login failed, retry again")
        ios.login_screen.login(wait=True)


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
