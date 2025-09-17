import pytest

from src.data.enums import AssetTabs, OrderType, BulkCloseOpts
from src.data.objects.notification_obj import ObjNoti
from src.utils.logging_utils import logger


@pytest.mark.parametrize("bulk_close_option", list(BulkCloseOpts))
def test(android, symbol, setup_bulk_test, cancel_bulk_close, bulk_close_option):
    order_ids = setup_bulk_test(order_type=OrderType.MARKET)
    expected_amount = 0 if len(order_ids) <= 30 else len(order_ids) - 30
    # -------------------

    if bulk_close_option == BulkCloseOpts.PROFIT:
        pytest.skip("Skipping PROFIT option for this test")

    logger.info(f"Step 1: Bulk close positions with {bulk_close_option}")
    android.trade_screen.asset_tab.bulk_close_positions(option=bulk_close_option, submit=True)

    logger.info(f"Verify bulk close notification banner")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti.bulk_close_open_position_banner(order_ids))
    android.home_screen.notifications.close_noti_banner()

    logger.info(f"Verify asset tab amount is {expected_amount}")
    android.trade_screen.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, expected_amount)
