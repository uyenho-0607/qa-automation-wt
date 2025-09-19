import pytest

from src.utils.logging_utils import logger


@pytest.mark.critical
def test_disable_and_enable(ios):

    logger.info("Step 1: Disable OCT mode")
    ios.trade_screen.place_order_panel.toggle_oct(enable=False)

    logger.info("Verify OCT mode disabled")
    ios.trade_screen.place_order_panel.verify_oct_mode(enable=False)

    logger.info("Step 2: Enable OCT mode")
    ios.trade_screen.place_order_panel.toggle_oct(enable=True)

    logger.info("Verify OCT mode enabled")
    ios.trade_screen.place_order_panel.verify_oct_mode(enable=True)


@pytest.mark.critical
def test_cancel_enable(ios):

    logger.info("Step 1: Disable OCT mode")
    ios.trade_screen.place_order_panel.toggle_oct(enable=False)

    logger.info("Step 2: Enable OCT and select Cancel")
    ios.trade_screen.place_order_panel.toggle_oct(enable=True, submit=False)

    logger.info("Verify OCT mode is not enabled")
    ios.trade_screen.place_order_panel.verify_oct_mode(enable=False)


@pytest.fixture(autouse=True, scope="module")
def teardown(ios):
    yield
    logger.info("[Cleanup] Enable OCT mode for other tests", teardown=True)
    ios.trade_screen.place_order_panel.toggle_oct(enable=True)