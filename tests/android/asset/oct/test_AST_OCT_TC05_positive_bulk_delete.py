import pytest
import random
from src.data.enums import AssetTabs, Features, OrderType, BulkCloseOpts
from src.data.objects.notification_obj import ObjNoti
from src.utils.logging_utils import logger


@pytest.mark.parametrize("order_type", (
        [
            OrderType.STOP_LIMIT,
            random.choice([OrderType.STOP, OrderType.LIMIT]),
        ]
))
def test(android, symbol, order_type, setup_bulk_asset_test, cancel_bulk_close):
    tab_amount, order_ids = setup_bulk_asset_test(order_type=order_type)
    # -------------------

    logger.info("Step 1: Select Pending Orders tab")
    android.trade_screen.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info(f"Step 2: Bulk delete orders")
    android.trade_screen.asset_tab.bulk_delete_orders()

    logger.info(f"Verify bulk delete notification banner")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti.bulk_delete_order_banner(order_ids))
    android.home_screen.notifications.close_noti_banner()

    logger.info(f"Step 3: Select tab: {AssetTabs.HISTORY}")
    android.trade_screen.asset_tab.select_tab(AssetTabs.HISTORY)

    logger.info("Verify items displayed in History Tab")
    android.trade_screen.asset_tab.verify_item_displayed(AssetTabs.POSITIONS_HISTORY, order_ids)


@pytest.fixture(autouse=True)
def setup_test(android):
    yield
    logger.info("Step 1: Navigate back to Asset Page")
    android.home_screen.go_back()
