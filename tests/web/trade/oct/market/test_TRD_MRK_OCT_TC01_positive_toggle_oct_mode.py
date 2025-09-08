import pytest

from src.apis.api_client import APIClient
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web):

    logger.info("Step 1: Disable OCT mode")
    web.trade_page.place_order_panel.toggle_oct(enable=False)

    logger.info("Verify OCT mode disabled")
    web.trade_page.place_order_panel.verify_oct_mode(enable=False)

    logger.info("Step 2: Enable OCT mode")
    web.trade_page.place_order_panel.toggle_oct(enable=True)

    logger.info("Verify OCT mode enabled")
    web.trade_page.place_order_panel.verify_oct_mode(enable=True)


@pytest.fixture(scope="module", autouse=True)
def setup_test(web):
    yield
    logger.info("[Cleanup] Enable OCT mode for other tests")
    APIClient().user.patch_oct(enable=True)

