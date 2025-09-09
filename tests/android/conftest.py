import pytest

from src.apis.api_client import APIClient
from src.core.actions.mobile_actions import MobileActions
from src.core.driver.appium_driver import AppiumDriver
from src.core.driver.driver_manager import DriverManager
from src.core.page_container.android_container import AndroidContainer
from src.utils.logging_utils import logger


@pytest.fixture(scope="package")
def android():
    logger.info("[Setup] Init Android driver")
    DriverManager.get_driver()

    yield AndroidContainer()

    logger.info("[Cleanup] Quit Android driver")
    DriverManager.quit_driver()

    logger.info("[Cleanup] Stop Appium service")
    AppiumDriver.stop_appium_service()


@pytest.fixture(scope="package")
def login_wt_app(android):
    logger.info(f"- Login to WT App")
    android.login_screen.login(wait=True)
    android.home_screen.feature_anm_modal.got_it()


@pytest.fixture
def cancel_delete_order(android):
    yield
    logger.debug("[Cleanup] Cancel delete order")
    android.trade_screen.modals.cancel_delete_order()


@pytest.fixture
def cancel_close_order(android):
    yield
    logger.debug("[Cleanup] Cancel close order")
    android.trade_screen.modals.cancel_close_order()


@pytest.fixture
def cancel_bulk_delete(android):
    yield
    logger.debug("[Cleanup] Cancel bulk delete orders")
    android.trade_screen.modals.cancel_bulk_delete()


@pytest.fixture
def cancel_bulk_close(android):
    yield
    logger.debug("[Cleanup] Cancel bulk close orders")
    android.trade_screen.modals.cancel_bulk_close()


@pytest.fixture
def cancel_edit_order(android):
    yield
    logger.debug("[Cleanup] Cancel edit order")
    android.trade_screen.modals.cancel_edit_order()


@pytest.fixture(scope="package")
def disable_OCT():
    logger.info("[Setup] Send API to disable OCT")
    APIClient().user.patch_oct(enable=False)


@pytest.fixture(scope="package")
def enable_OCT():
    logger.info("[Setup] Send API to enable OCT")
    APIClient().user.patch_oct(enable=True)
