import pytest

from src.data.enums import AssetTabs, BulkCloseOpts, OrderType
from src.data.objects.notification_object import ObjectNoti
from src.utils.logging_utils import logger


@pytest.mark.parametrize("close_option", (BulkCloseOpts.ALL,))
def test(android, symbol, setup_bulk_test, close_option, cancel_bulk_close):
    order_ids = setup_bulk_test(order_type=OrderType.MARKET)
    expected_amount = 0 if len(order_ids) <= 30 else len(order_ids) - 30
    # -------------------

    logger.info(f"Step 1: Bulk close positions")
    android.trade_screen.asset_tab.bulk_close_positions(close_option)

    logger.info("Verify bulk close notification banner")
    android.home_screen.notifications.verify_notification_banner(*ObjectNoti.bulk_close_open_position_banner(order_ids))
    android.home_screen.notifications.close_noti_banner()

    logger.info(f"Verify asset tab amount is: {expected_amount}")
    android.trade_screen.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, expected_amount)
