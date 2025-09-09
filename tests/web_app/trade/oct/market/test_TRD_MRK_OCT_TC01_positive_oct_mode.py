import pytest

from src.apis.api_client import APIClient
from src.utils.logging_utils import logger


@pytest.mark.critical
def test_disable_and_enable(web_app):

    logger.info("Step 1: Disable OCT mode")
    web_app.trade_page.place_order_panel.toggle_oct(enable=False)

    logger.info("Verify OCT mode disabled")
    web_app.trade_page.place_order_panel.verify_oct_mode(enable=False)

    logger.info("Step 2: Enable OCT mode")
    web_app.trade_page.place_order_panel.toggle_oct(enable=True)

    logger.info("Verify OCT mode enabled")
    web_app.trade_page.place_order_panel.verify_oct_mode(enable=True)


@pytest.mark.critical
def test_cancel_enable(web_app):

    logger.info("Step 1: Disable OCT mode")
    web_app.trade_page.place_order_panel.toggle_oct(enable=False)

    logger.info("Step 2: Enable OCT and select Cancel")
    web_app.trade_page.place_order_panel.toggle_oct(enable=True, submit=False)

    logger.info("Verify OCT mode is not enabled")
    web_app.trade_page.place_order_panel.verify_oct_mode(enable=False)


@pytest.fixture(autouse=True, scope="module")
def cleanup_test():
    yield
    logger.info("[Cleanup] Enable OCT mode for other tests")
    APIClient().user.patch_oct(enable=True)

