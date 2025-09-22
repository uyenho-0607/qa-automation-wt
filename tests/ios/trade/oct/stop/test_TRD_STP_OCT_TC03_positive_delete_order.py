import pytest

from src.data.enums import AssetTabs, Features
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(ios, order_data, stop_obj, get_asset_tab_amount):
    trade_object = stop_obj()
    tab = AssetTabs.PENDING_ORDER

    logger.info("Step 1: Get tab amount")
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info("Step 2: Open pre-trade details form")
    ios.trade_screen.place_order_panel.open_pre_trade_details()

    logger.info(f"Step 3: Place order with: {format_display_dict(trade_object)}, (tab amount: {tab_amount!r})")
    order_data(trade_object, confirm=False)

    logger.info("Step 4: Get placed orderID")
    ios.trade_screen.asset_tab.select_tab(tab)
    trade_object.order_id = ios.trade_screen.asset_tab.get_last_order_id(tab, wait=True)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id}")
    ios.trade_screen.asset_tab.verify_item_data(trade_object, wait=False)

    logger.info("Step 5: Delete order")
    ios.trade_screen.asset_tab.delete_order(trade_object, confirm=False)

    logger.info(f"Verify delete order notification banner")
    ios.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).delete_order_banner())

    logger.info(f"Verify asset tab amount: {tab_amount}")
    ios.trade_screen.asset_tab.verify_tab_amount(tab, tab_amount)

    logger.info(f"Verify order {trade_object.order_id!r} no longer displayed in Pending Orders")
    ios.trade_screen.asset_tab.verify_items_displayed(tab, trade_object.order_id, is_display=False)
