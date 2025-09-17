import pytest

from src.apis.api_client import APIClient
from src.core.driver.appium_driver import AppiumDriver
from src.core.driver.driver_manager import DriverManager
from src.core.page_container.android_container import AndroidContainer
from src.utils.logging_utils import logger
from contextlib import suppress
from src.data.consts import FAILED_ICON_COLOR
from src.data.project_info import RuntimeConfig

@pytest.fixture(scope="package")
def android():
    logger.info("[Setup] Init Android driver", setup=True)
    DriverManager.get_driver()

    yield AndroidContainer()

    logger.info("[Cleanup] Quit Android driver", teardown=True)
    DriverManager.quit_driver()

    logger.info("[Cleanup] Stop Appium service", teardown=True)
    AppiumDriver.stop_appium_service()


@pytest.fixture(scope="package")
def login_wt_app(android):
    
    # handle login with max attempts = 3
    max_retries = 3

    logger.info("[Setup] Login to WT app", setup=True)
    android.login_screen.login(wait=True)

    logger.info("[Setup] Skip feature ann modal if any", setup=True)
    android.home_screen.feature_anm_modal.got_it()

    logger.info("[Setup] Wait for home screen loaded", setup=True)

    for attempt in range(max_retries + 1):
        if not android.home_screen.is_logged_in():
            with suppress(Exception):
                logger.info("[Setup] Perform login again", setup=True)
                android.login_screen.login(wait=True)
                android.home_screen.feature_anm_modal.got_it()
        else:
            break

        if attempt == max_retries - 1 and not android.home_screen.is_logged_in():
            # login one more time to catch the screenshot
            android.login_screen.login()
            raise RuntimeError(f"Setup test failed ! Unable to Login to WT {FAILED_ICON_COLOR}")


@pytest.fixture
def cancel_delete_order(android):
    yield
    logger.debug("[Cleanup] Cancel delete order", teardown=True)
    android.trade_screen.modals.cancel_delete_order()


@pytest.fixture
def cancel_close_order(android):
    yield
    logger.debug("[Cleanup] Cancel close order", teardown=True)
    android.trade_screen.modals.cancel_close_order()


@pytest.fixture
def cancel_bulk_delete(android):
    yield
    logger.debug("[Cleanup] Cancel bulk delete orders", teardown=True)
    android.trade_screen.modals.cancel_bulk_delete()


@pytest.fixture
def cancel_bulk_close(android):
    yield
    logger.debug("[Cleanup] Cancel bulk close orders", teardown=True)
    android.trade_screen.modals.cancel_bulk_close()


# cleanup trade test
@pytest.fixture
def cancel_all(android):
    yield
    logger.info("[Cleanup] Click cancel button (if any)", teardown=True)
    android.trade_screen.click_cancel_btn()


@pytest.fixture
def cancel_edit_order(android):
    yield
    logger.debug("[Cleanup] Cancel edit order", teardown=True)
    android.trade_screen.modals.cancel_edit_order()


@pytest.fixture(scope="package")
def disable_OCT(android):
    """disable OCT from place order panel"""

    logger.info("[Setup] Check if OCT mode is enabled/disabled in Admin Config", setup=True)
    is_enable = android.trade_screen.place_order_panel.is_oct_enable()

    if is_enable:
        logger.info("[Setup] Disable OCT", setup=True)
        android.trade_screen.place_order_panel.toggle_oct(enable=False, submit=True)

    else:
        logger.info("[Setup] OCT mode already disabled in Admin Config", setup=True)


@pytest.fixture(scope="package")
def enable_OCT(android):
    """enable OCT from place order panel"""
    logger.info("[Setup] Check if OCT mode is enabled/disabled in Admin Config", setup=True)
    is_enable = android.trade_screen.place_order_panel.is_oct_enable()

    if is_enable:
        logger.info("[Setup] OCT mode is enabled in Admin config - Enable OCT", setup=True)
        android.trade_screen.place_order_panel.toggle_oct(enable=True, submit=True)

    else:
        pytest.skip("OCT mode is disabled in Admin Config - SKIP this test ")
