import time
from contextlib import suppress

import pytest

from src.apis.api_client import APIClient
from src.core.driver.driver_manager import DriverManager
from src.core.page_container.web_container import WebContainer
from src.data.consts import FAILED_ICON_COLOR
from src.utils.logging_utils import logger


@pytest.fixture(scope="package")
def web():
    logger.info("[Setup] Init Web Driver")
    DriverManager.get_driver()

    yield WebContainer()

    logger.info("[Cleanup] Quit Web Driver")
    DriverManager.quit_driver()


@pytest.fixture(scope="package")
def login_member_site(web):
    max_attempts = 5

    logger.info(f"{'=' * 10} Setup Login - Start {'=' * 10}")
    logger.info("- Navigate to WT Member Site", setup=True)
    web.login_page.goto()

    logger.info("- Login to Member Site", setup=True)
    web.login_page.login(wait=True)

    logger.info("- Skipping feature ann modal (if any)", setup=True)
    web.home_page.feature_announcement_modal.got_it()

    logger.info("- Check if logged in success", setup=True)
    for attempt in range(max_attempts):
        if not web.home_page.is_logged_in():

            logger.warning(f"- Login failed, refresh page and login again (attempt: {attempt + 1})")
            web.login_page.refresh_page()
            time.sleep(3)

            with suppress(Exception):
                logger.info("- Perform login again")
                web.login_page.login(wait=True)
                web.home_page.feature_announcement_modal.got_it()

        else:
            break

        if attempt == max_attempts - 1 and not web.home_page.is_logged_in():
            # login one more time to catch the screenshot
            web.login_page.login()
            raise RuntimeError(f"Setup test failed ! Unable to Login to WT {FAILED_ICON_COLOR}")

    logger.info(f"{'=' * 10} Setup Login - Done {'=' * 10}")


@pytest.fixture(scope="package")
def disable_OCT():
    logger.info("[Setup] Send API request to disable OCT", setup=True)
    APIClient().user.patch_oct(enable=False)


@pytest.fixture(scope="package")
def enable_OCT():
    logger.info("[Setup] Send API request to enable OCT")
    APIClient().user.patch_oct(enable=True)


@pytest.fixture
def close_confirm_modal(web):
    yield
    logger.info("[Cleanup]: Close trade confirm modal if any", teardown=True)
    web.trade_page.modals.close_trade_confirm_modal()


@pytest.fixture
def close_edit_confirm_modal(web):
    yield
    logger.info("[Cleanup]: Close edit confirm modal if any", teardown=True)
    web.trade_page.modals.close_edit_confirm_modal()


@pytest.fixture
def cancel_close_order(web):
    yield
    logger.info("[Cleanup]: Cancel close order modal if any")
    web.trade_page.modals.cancel_close_order()


@pytest.fixture
def cancel_delete_order(web):
    yield
    logger.info("[Cleanup]: Cancel delete order modal if any")
    web.trade_page.modals.cancel_delete_order()


@pytest.fixture
def cancel_bulk_delete(web):
    yield
    logger.info("[Cleanup]: Cancel bulk delete modal if any")
    web.trade_page.modals.cancel_bulk_delete()


@pytest.fixture
def cancel_bulk_close(web):
    yield
    logger.info("[Cleanup]: Cancel bulk close modal if any")
    web.trade_page.modals.cancel_bulk_close()
