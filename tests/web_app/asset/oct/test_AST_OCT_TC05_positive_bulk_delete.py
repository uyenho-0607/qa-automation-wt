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
def test(web_app, symbol, order_type, setup_bulk_asset_test, cancel_bulk_close):
    tab_amount, order_ids = setup_bulk_asset_test(order_type=order_type)
    # -------------------

    logger.info("Step 1: Select Pending Orders tab")
    web_app.trade_page.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info(f"Step 2: Bulk delete orders")
    web_app.trade_page.asset_tab.bulk_delete_orders()

    logger.info(f"Verify bulk delete notification banner")
    web_app.home_page.notifications.verify_notification_banner(*ObjNoti.bulk_delete_order_banner(order_ids))
    web_app.home_page.notifications.close_noti_banner()

    logger.info(f"Step 3: Select tab: {AssetTabs.HISTORY}")
    web_app.trade_page.asset_tab.select_tab(AssetTabs.HISTORY)

    logger.info("Verify items displayed in History Tab")
    web_app.trade_page.asset_tab.verify_item_displayed(AssetTabs.HISTORY, order_ids)


@pytest.fixture(autouse=True)
def setup_test(web_app):
    yield
    logger.info("[Cleanup] Navigate back to Asset Page")
    web_app.home_page.go_back()
