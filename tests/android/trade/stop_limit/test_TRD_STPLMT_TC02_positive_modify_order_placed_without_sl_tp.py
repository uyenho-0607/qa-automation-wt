import pytest

from src.data.enums import AssetTabs, SLTPType, OrderType, Expiry
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize(
    "edit_field, sl_type, tp_type",
    [
        ("stop_loss", SLTPType.PRICE, None),
        ("stop_loss", SLTPType.POINTS, None),
        ("take_profit", None, SLTPType.PRICE),
        ("take_profit", None, SLTPType.POINTS),
        ("stop_loss, take_profit", SLTPType.PRICE, SLTPType.PRICE),
        ("stop_loss, take_profit", SLTPType.POINTS, SLTPType.POINTS),
        ("stop_loss, take_profit", *SLTPType.sample_values(amount=2)),
    ]
)
def test(android, symbol, edit_field, sl_type, tp_type, cancel_edit_order, create_order_data):
    # -------------------
    trade_object = ObjectTrade(
        order_type=OrderType.STOP_LIMIT, symbol,
        stop_loss=0, take_profit=0, expiry=Expiry.sample_values(OrderType.STOP_LIMIT)
    )
    tab = AssetTabs.PENDING_ORDER
    # -------------------

    logger.info("Step 1: Place order without Stop Loss and Take Profit")
    create_order_data(trade_object)

    logger.info(f"Step 2: Update {tab.title()} item with {edit_field!r}")
    android.trade_screen.modals.modify_order(tab, trade_object, sl_type=sl_type, tp_type=tp_type)

    logger.info("Verify edit confirmation info")
    android.trade_screen.modals.verify_edit_trade_confirmation(trade_object)

    logger.info("Step 3: Confirm update order")
    android.trade_screen.modals.confirm_update_order()

    logger.info("Verify notification banner updated message")
    android.home_screen.notifications.verify_notification_banner(*ObjectNoti(trade_object).order_updated_banner(**trade_object))

    logger.info(f"Verify {tab.title()} item details after update")
    android.trade_screen.asset_tab.verify_item_data(trade_object)
