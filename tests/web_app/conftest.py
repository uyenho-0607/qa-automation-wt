from contextlib import suppress

import pytest

from src.apis.api_client import APIClient
from src.core.driver.driver_manager import DriverManager
from src.core.page_container.web_app_container import WebAppContainer
from src.data.consts import FAILED_ICON_COLOR
from src.utils.logging_utils import logger


@pytest.fixture(scope="package")
def web_app():
    logger.info("[Setup] Init Web Driver")
    DriverManager.get_driver()

    yield WebAppContainer()

    logger.info("[Cleanup] Quit Web Driver")
    DriverManager.quit_driver()


@pytest.fixture(scope="package")
def login_member_site(web_app):
    max_attempts = 5
    logger.info(f"{'=' * 10} Setup Login - Start {'=' * 10}")

    logger.info("- Navigate to WT Member Site")
    web_app.login_page.goto()
    web_app.login_page.wait_for_spin_loader(timeout=5)

    logger.info("- Login to Member Site")
    web_app.login_page.login(wait=True)

    logger.info("- Skipping feature ann modal (if any)")
    web_app.home_page.feature_anm_modal.got_it(timeout=3)

    logger.info("- Check if logged in success")
    for attempt in range(max_attempts):
        if not web_app.home_page.is_logged_in():
            logger.warning(f"- Login failed, refresh page and login again (attempt: {attempt + 1})")
            web_app.login_page.refresh_page()

            with suppress(Exception):
                logger.info("- Perform login again")
                web_app.login_page.login(wait=True)
                web_app.home_page.feature_anm_modal.got_it(timeout=3)

        else:
            break

        if attempt == max_attempts - 1 and not web_app.home_page.is_logged_in():
            # login one more time to catch the screenshot
            web_app.login_page.login()
            raise RuntimeError(f"Setup test failed ! Unable to Login to WT {FAILED_ICON_COLOR}")

    logger.info(f"{'=' * 10} Setup Login - Done {'=' * 10}")


@pytest.fixture(scope="package")
def disable_OCT():
    logger.info("[Setup] Send API request to disable OCT")
    APIClient().user.patch_oct(enable=False)


@pytest.fixture(scope="package")
def enable_OCT():
    logger.info("[Setup] Send API request enable OCT")
    APIClient().user.patch_oct(enable=True)


# cleanup trade test
@pytest.fixture
def cancel_all(web_app):
    yield
    logger.info("[Cleanup] Click cancel button (if any)")
    web_app.trade_page.click_cancel_btn()


@pytest.fixture
def cancel_edit_order(web_app):
    yield
    logger.debug("[Cleanup] Cancel edit order if any")
    web_app.trade_page.modals.cancel_edit_order()


@pytest.fixture
def cancel_close_order(web_app):
    yield
    logger.debug("[Cleanup] Cancel close order if any")
    web_app.trade_page.modals.cancel_close_order()


@pytest.fixture
def cancel_delete_order(web_app):
    yield
    logger.debug("[Cleanup] Cancel delete order if any")
    web_app.trade_page.modals.cancel_delete_order()


@pytest.fixture
def cancel_bulk_delete(web_app):
    yield
    logger.debug("[Cleanup] Cancel bulk delete orders if any")
    web_app.trade_page.modals.cancel_bulk_delete()


@pytest.fixture
def cancel_bulk_close(web_app):
    yield
    logger.debug("[Cleanup] Cancel bulk close orders if any")
    web_app.trade_page.modals.cancel_bulk_close()
