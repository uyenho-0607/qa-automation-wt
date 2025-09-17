import pytest

from src.data.enums import AssetTabs, Features, OrderType, BulkCloseOpts
from src.data.objects.notification_obj import ObjNoti
from src.utils.logging_utils import logger


@pytest.mark.parametrize("bulk_close_option", list(BulkCloseOpts))
def test(android, symbol, setup_bulk_asset_test, cancel_all, bulk_close_option):
    tab_amount, order_ids = setup_bulk_asset_test(order_type=OrderType.MARKET)
    # -------------------

    if bulk_close_option == BulkCloseOpts.PROFIT:
        pytest.skip("Skipping PROFIT option for this test")

    logger.info(f"Step 1: Bulk close positions with {bulk_close_option}")
    android.trade_screen.asset_tab.bulk_close_positions(option=bulk_close_option, confirm=True)

    logger.info(f"Verify bulk close notification banner")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti.bulk_close_open_position_banner(order_ids))
    android.home_screen.notifications.close_noti_banner()

    logger.info(f"Step 2: Select tab: {AssetTabs.HISTORY}")
    android.trade_screen.asset_tab.select_tab(AssetTabs.HISTORY)

    logger.info("Verify items displayed in History Tab")
    android.trade_screen.asset_tab.verify_item_displayed(AssetTabs.HISTORY, order_ids)


@pytest.fixture(autouse=True)
def setup_test(android):
    yield
    logger.info("[Cleanup] Navigate back to Asset Screen")
    android.home_screen.go_back()
