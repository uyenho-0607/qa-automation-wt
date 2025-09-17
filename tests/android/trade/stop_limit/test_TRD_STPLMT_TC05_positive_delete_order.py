import pytest

from src.data.enums import AssetTabs
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(android, stop_limit_obj, order_data, cancel_all):
    trade_object = stop_limit_obj()
    tab = AssetTabs.PENDING_ORDER

    logger.info("Step 1: Get asset tab amount")
    tab_amount = android.trade_screen.asset_tab.get_tab_amount(AssetTabs.PENDING_ORDER)

    logger.info(f"Step 2: Place order with: {format_display_dict(trade_object)} (tab amount: {tab_amount!r})")
    order_data(trade_object)

    logger.info("Step 3: Select Pending Orders tab")
    android.trade_screen.asset_tab.select_tab(tab)

    logger.info(f"Verify order placed successfully, tab = {tab_amount + 1}")
    android.trade_screen.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount + 1)

    logger.info("Step 4: Delete pending order")
    android.trade_screen.asset_tab.delete_order(trade_object)

    logger.info(f"Verify delete order notification banner")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).delete_order_banner())

    logger.info(f"Verify asset tab amount: {tab_amount}")
    android.trade_screen.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount)

    logger.info(f"Verify item is no longer displayed")
    android.trade_screen.asset_tab.verify_item_displayed(AssetTabs.PENDING_ORDER, trade_object.order_id, is_display=False)
