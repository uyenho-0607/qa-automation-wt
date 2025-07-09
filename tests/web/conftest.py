import pytest

from src.apis.api_client import APIClient
from src.utils.logging_utils import logger


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
