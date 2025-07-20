import pytest

from src.data.enums import SLTPType, OrderType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize(
    "edit_field, sl_type, tp_type",
    [
        ("SL", SLTPType.random_values(), None),
        ("TP", None, SLTPType.random_values()),
        ("SL, TP", *SLTPType.random_values(amount=2)),
    ]
)
def test(android, symbol, edit_field, sl_type, tp_type, create_order_data):
    trade_object = ObjTrade(order_type=OrderType.STOP_LIMIT, symbol=symbol, stop_loss=0, take_profit=0)
    # -------------------

    logger.info("Step 1: Place order without Stop Loss and Take Profit")
    create_order_data(trade_object)

    logger.info(f"Step 2: Update placed order with {edit_field!r}")
    android.trade_screen.modals.modify_order(trade_object, sl_type=sl_type, tp_type=tp_type)

    logger.info("Verify edit confirmation info")
    android.trade_screen.modals.verify_edit_trade_confirmation(trade_object)

    logger.info("Step 3: Confirm update order")
    android.trade_screen.modals.confirm_update_order()

    logger.info("Verify notification banner updated message")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner(**trade_object))

    logger.info(f"Verify placed order details after update")
    android.trade_screen.asset_tab.verify_item_data(trade_object)
