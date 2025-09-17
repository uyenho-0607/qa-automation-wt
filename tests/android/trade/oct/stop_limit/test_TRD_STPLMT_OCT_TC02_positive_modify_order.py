import pytest

from src.data.enums import SLTPType, AssetTabs
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize("edit_field, sl_type, tp_type", [("SL, TP", SLTPType.PRICE, SLTPType.PRICE)])
def test(android, stop_limit_obj, edit_field, sl_type, tp_type, order_data):

    trade_object = stop_limit_obj()
    tab = AssetTabs.PENDING_ORDER

    logger.info("Step 1: Open pre-trade details form")
    android.trade_screen.place_order_panel.open_pre_trade_details()

    logger.info(f"Step 2: Place order with: {format_display_dict(trade_object)}")
    order_data(trade_object, confirm=False)

    logger.info("Step 3: Select Pending Orders tab")
    android.trade_screen.asset_tab.select_tab(tab)
    trade_object.order_id = android.trade_screen.asset_tab.get_last_order_id(AssetTabs.PENDING_ORDER, wait=True)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    android.trade_screen.asset_tab.verify_item_data(trade_object, tab, False)

    logger.info(f"Step 4: Update {tab.title()} item with {edit_field!r} ({sl_type}, {tp_type})")
    android.trade_screen.asset_tab.modify_order(trade_object, sl_type=sl_type, tp_type=tp_type, confirm=False)

    logger.info("Verify notification banner updated message")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner())

    logger.info(f"Step 5: Select Pending Orders tab")
    android.trade_screen.asset_tab.select_tab(tab)

    logger.info(f"Verify {tab.title()} item details after update")
    android.trade_screen.asset_tab.verify_item_data(trade_object)
