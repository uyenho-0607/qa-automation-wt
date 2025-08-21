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


@pytest.fixture(scope="package")
def login_wt_app(android):
    max_retries = 3

    logger.info(f"- Login to WT App")
    android.login_screen.login(wait=True)
    android.home_screen.feature_anm_modal.got_it()

    logger.info("- Check if login success")
    while not android.home_screen.is_logged_in() and max_retries:
        max_retries -= 1

        logger.debug("- Retry Login")
        android.login_screen.login(wait=True)
        android.home_screen.feature_anm_modal.got_it()


@pytest.fixture
def cancel_delete_order(android):
    yield
    logger.debug("- Cancel delete order")
    android.trade_screen.modals.cancel_delete_order()


@pytest.fixture
def cancel_close_order(android):
    yield
    logger.debug("- Cancel close order")
    android.trade_screen.modals.cancel_close_order()


@pytest.fixture
def cancel_bulk_delete(android):
    yield
    logger.debug("- Cancel bulk delete orders")
    android.trade_screen.modals.cancel_bulk_delete()


@pytest.fixture
def cancel_bulk_close(android):
    yield
    logger.debug("- Cancel bulk close orders")
    android.trade_screen.modals.cancel_bulk_close()


@pytest.fixture
def cancel_edit_order(android):
    yield
    logger.debug("- Cancel edit order")
    android.trade_screen.modals.cancel_edit_order()
