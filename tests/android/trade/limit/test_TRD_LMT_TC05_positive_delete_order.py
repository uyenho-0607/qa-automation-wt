import pytest

from src.data.enums import AssetTabs
from src.data.objects.notification_obj import ObjNoti
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(android, limit_obj, create_order_data, cancel_all):
    trade_object = limit_obj()
    tab = AssetTabs.PENDING_ORDER

    logger.info("Step 1: Get asset tab amount")
    tab_amount = android.trade_screen.asset_tab.get_tab_amount(AssetTabs.PENDING_ORDER)

    logger.info(f"Step 2: Place {trade_object.trade_type} Order, (tab amount: {tab_amount!r})")
    create_order_data(trade_object)

    logger.info("Step 4: Select Pending Orders tab")
    android.trade_screen.asset_tab.select_tab(tab)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id}")
    android.trade_screen.asset_tab.verify_item_displayed(AssetTabs.PENDING_ORDER, trade_object.order_id)

    logger.info("Step 4: Delete pending order")
    android.trade_screen.asset_tab.delete_order(trade_object)

    logger.info(f"Verify delete order notification banner")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).delete_order_banner())

    logger.info(f"Verify asset tab amount: {tab_amount}")
    android.trade_screen.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount)

    logger.info(f"Verify item is no longer displayed")
    android.trade_screen.asset_tab.verify_item_displayed(AssetTabs.PENDING_ORDER, trade_object.order_id, is_display=False)
