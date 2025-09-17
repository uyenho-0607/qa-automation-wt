from src.apis.api_client import APIClient
from src.utils.logging_utils import logger


def test(android):
    logger.info(f"Step 1: Disable the OCT")
    android.trade_screen.place_order_panel.toggle_oct(enable=False)

    logger.info(f"Verify OCT mode disabled")
    android.trade_screen.place_order_panel.verify_oct_mode(enable=False)

    logger.info(f"Step 2: Enable the OCT")
    android.trade_screen.place_order_panel.toggle_oct(submit=True)

    logger.info(f"Verify OCT mode enabled")
    android.trade_screen.place_order_panel.verify_oct_mode(enable=True)


def setup_test():
    yield
    logger.info("[Cleanup] Enable OCT mode for other tests")
    APIClient().user.patch_oct(enable=True)
