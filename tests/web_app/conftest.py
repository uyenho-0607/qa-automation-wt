from contextlib import suppress

import pytest

from src.core.driver.driver_manager import DriverManager
from src.core.page_container.web_app_container import WebAppContainer
from src.data.consts import FAILED_ICON_COLOR, QUICK_WAIT
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
        if not web_app.home_page.on_home_page():
            logger.warning(f"- Login failed, refresh page and login again (attempt: {attempt + 1})")
            web_app.login_page.refresh_page()

            with suppress(Exception):
                logger.info("- Perform login again")
                web_app.login_page.login(wait=True)
                web_app.home_page.feature_anm_modal.got_it(timeout=3)

        else:
            break

        if attempt == max_attempts - 1 and not web_app.home_page.on_home_page():
            # login one more time to catch the screenshot
            web_app.login_page.login()
            raise RuntimeError(f"Setup test failed ! Unable to Login to WT {FAILED_ICON_COLOR}")

    logger.info(f"{'=' * 10} Setup Login - Done {'=' * 10}")


@pytest.fixture(scope="package")
def disable_OCT(web_app):
    """disable OCT from place order panel"""
    logger.info("[Setup] Check if OCT mode is enabled/disabled in Admin Config", setup=True)
    is_enable = web_app.trade_page.place_order_panel.is_oct_enable()

    if is_enable:
        logger.info("[Setup] OCT mode is enabled in Admin config - Disable OCT", setup=True)
        web_app.trade_page.place_order_panel.toggle_oct(enable=False, submit=True)

    else:
        logger.info("[Setup] OCT mode already disabled in Admin Config", setup=True)


@pytest.fixture(scope="package")
def enable_OCT(web_app):
    """enable OCT from place order panel"""
    logger.info("[Setup] Check if OCT mode is enabled/disabled in Admin Config", setup=True)
    is_enable = web_app.trade_page.place_order_panel.is_oct_enable()

    if is_enable:
        logger.info("[Setup] OCT mode is enabled in Admin config - Enable OCT", setup=True)
        web_app.trade_page.place_order_panel.toggle_oct(enable=True, submit=True)

    else:
        pytest.skip("OCT mode is disabled in Admin Config - SKIP this test ")


# cleanup trade test
@pytest.fixture
def cancel_all(web_app):
    yield
    logger.info("[Cleanup] Click cancel button (if any)", teardown=True)
    web_app.trade_page.click_cancel_btn()


@pytest.fixture
def cancel_edit_order(web_app):
    yield
    logger.info("[Cleanup] Cancel edit order if any", teardown=True)
    web_app.trade_page.modals.confirm_update_order(confirm=False, timeout=QUICK_WAIT)


@pytest.fixture
def cancel_close_order(web_app):
    yield
    logger.info("[Cleanup] Cancel close order if any", teardown=True)


@pytest.fixture
def cancel_delete_order(web_app):
    yield
    logger.info("[Cleanup] Cancel delete order if any", teardown=True)
    web_app.trade_page.modals.cancel_delete_order()


@pytest.fixture
def cancel_bulk_delete(web_app):
    yield
    logger.info("[Cleanup] Cancel bulk delete orders if any", teardown=True)
    web_app.trade_page.modals.cancel_bulk_delete()


@pytest.fixture
def cancel_bulk_close(web_app):
    yield
    logger.info("[Cleanup] Cancel bulk close orders if any")
    web_app.trade_page.modals.cancel_bulk_close()
