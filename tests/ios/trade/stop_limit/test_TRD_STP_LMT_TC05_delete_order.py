import pytest

from src.data.enums import AssetTabs
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(ios, order_data, stop_limit_obj, cancel_all, get_asset_tab_amount):
    trade_object = stop_limit_obj()

    logger.info("Step 1: Get asset tab amount")
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 2: Place order with: {format_display_dict(trade_object)}, (tab amount: {tab_amount!r})")
    order_data(trade_object)

    logger.info("Step 3: Select Pending Orders tab")
    ios.trade_screen.asset_tab.select_tab(AssetTabs.PENDING_ORDER)
    trade_object.order_id = ios.trade_screen.asset_tab.get_last_order_id(AssetTabs.PENDING_ORDER, wait=True)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id}")
    ios.trade_screen.asset_tab.verify_item_data(trade_object, wait=False)

    logger.info("Step 4: Delete order")
    ios.trade_screen.asset_tab.delete_order(trade_object)

    logger.info(f"Verify delete order notification banner")
    ios.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).delete_order_banner())

    logger.info(f"Verify asset tab amount: {tab_amount}")
    ios.trade_screen.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount)

    logger.info(f"Verify order {trade_object.order_id!r} no longer displayed in Pending Orders")
    ios.trade_screen.asset_tab.verify_items_displayed(AssetTabs.PENDING_ORDER, trade_object.order_id, is_display=False)