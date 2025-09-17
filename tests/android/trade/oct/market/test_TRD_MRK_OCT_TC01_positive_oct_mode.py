import pytest

from src.apis.api_client import APIClient
from src.utils.logging_utils import logger


@pytest.mark.critical
def test_disable_and_enable(android):

    logger.info("Step 1: Disable OCT mode")
    android.trade_screen.place_order_panel.toggle_oct(enable=False)

    logger.info("Verify OCT mode disabled")
    android.trade_screen.place_order_panel.verify_oct_mode(enable=False)

    logger.info("Step 2: Enable OCT mode")
    android.trade_screen.place_order_panel.toggle_oct(enable=True)

    logger.info("Verify OCT mode enabled")
    android.trade_screen.place_order_panel.verify_oct_mode(enable=True)


@pytest.mark.critical
def test_cancel_enable(android):

    logger.info("Step 1: Disable OCT mode")
    android.trade_screen.place_order_panel.toggle_oct(enable=False)

    logger.info("Step 2: Enable OCT and select Cancel")
    android.trade_screen.place_order_panel.toggle_oct(enable=True, confirm=False)

    logger.info("Verify OCT mode is not enabled")
    android.trade_screen.place_order_panel.verify_oct_mode(enable=False)


@pytest.fixture(autouse=True, scope="module")
def teardown(android):
    yield
    logger.info("[Cleanup] Enable OCT mode for other tests", teardown=True)
    android.trade_screen.place_order_panel.toggle_oct(enable=True)
