import pytest

from src.data.enums import AssetTabs, SLTPType, OrderType
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize(
    "field, place_type, edit_type",
    [
        ("stop_loss", SLTPType.POINTS, SLTPType.POINTS),
        ("stop_loss", SLTPType.PRICE, SLTPType.PRICE),
        ("stop_loss", *SLTPType.sample_values(amount=2)),
        ("take_profit", SLTPType.POINTS, SLTPType.POINTS),
        ("take_profit", SLTPType.PRICE, SLTPType.PRICE),
        ("take_profit", *SLTPType.sample_values(amount=2)),
    ]
)
def test(android, symbol, get_asset_tab_amount, field, place_type, edit_type, create_order_data):
    # handle parameters
    sl_tp_val = {("stop_loss" if field == "take_profit" else "take_profit"): 0, "indicate": place_type}
    update_sl_type, update_tp_type = (edit_type, None) if field == "stop_loss" else (None, edit_type)

    trade_object = ObjectTrade(order_type=OrderType.STOP_LIMIT, symbol=symbol, **sl_tp_val)
    tab = AssetTabs.PENDING_ORDER
    # -------------------

    logger.info(f"Step 1: Place {trade_object.trade_type} Order with {field!r}")
    create_order_data(trade_object)

    logger.info(f"Step 2: Update {tab.title()} with {field!r} - type: {edit_type.capitalize()!r}")
    android.trade_screen.modals.modify_order(tab, trade_object, sl_type=update_sl_type, tp_type=update_tp_type)

    logger.info("Verify edit confirmation info")
    android.trade_screen.modals.verify_edit_trade_confirmation(trade_object)

    logger.info("Step 3: Confirm update order")
    android.trade_screen.modals.confirm_update_order()

    logger.info("Verify notification banner updated message")
    android.home_screen.notifications.verify_notification_banner(*ObjectNoti(trade_object).order_updated_banner(**trade_object))

    logger.info(f"Verify {tab.title()} item details after update")
    android.trade_screen.asset_tab.verify_item_data(trade_object)
