import pytest

from src.core.driver.driver_manager import DriverManager
from src.core.page_container.web_container import WebContainer
from src.apis.api_client import APIClient
from src.utils.logging_utils import logger


@pytest.fixture(scope="package")
def web():
    logger.info("- Init Web Driver")
    DriverManager.get_driver()

    yield WebContainer()

    logger.info("- Clean up Web Driver")
    DriverManager.quit_driver()


@pytest.fixture(scope="package")
def login_member_site(web):
    retries = 3
    logger.info("- Navigate to WT Member Site")
    web.login_page.goto()

    logger.info("- Login to Member Site")
    web.login_page.login(wait=True)
    web.home_page.feature_announcement_modal.got_it()

    logger.info("- Check if logged success")
    while not web.home_page.is_logged_in() and retries:
        logger.info("- Retry login")
        web.login_page.login(wait=True)
        web.home_page.feature_announcement_modal.got_it()

        retries -= 1


@pytest.fixture(scope="package")
def disable_OCT():
    logger.info("- Check and disable OCT")
    APIClient().user.patch_oct(enable=False)


@pytest.fixture(scope="package")
def enable_OCT():
    logger.info("- Check and enable OCT")
    APIClient().user.patch_oct(enable=True)


@pytest.fixture
def close_confirm_modal(web):
    yield
    web.trade_page.modals.close_trade_confirm_modal()


@pytest.fixture
def close_edit_confirm_modal(web):
    yield
    web.trade_page.modals.close_edit_confirm_modal()


@pytest.fixture
def cancel_close_order(web):
    yield
    web.trade_page.modals.cancel_close_order()


@pytest.fixture
def cancel_delete_order(web):
    yield
    web.trade_page.modals.cancel_delete_order()


@pytest.fixture
def cancel_bulk_delete(web):
    yield
    web.trade_page.modals.cancel_bulk_delete()


@pytest.fixture
def cancel_bulk_close(web):
    yield
    web.trade_page.modals.cancel_bulk_close()
