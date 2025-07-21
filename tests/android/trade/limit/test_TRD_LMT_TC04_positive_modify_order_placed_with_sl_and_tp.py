import pytest

from src.data.enums import AssetTabs, SLTPType, OrderType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize(
    "sl_type, tp_type",
    [
        SLTPType.random_values(amount=2),
    ]
)
def test(android, symbol, create_order_data, sl_type, tp_type):
    trade_object = ObjTrade(order_type=OrderType.LIMIT, symbol=symbol, indicate=SLTPType.sample_values())
    # -------------------

    logger.info(f"Step 1: Place {trade_object.trade_type} Order with stop loss and take profit")
    create_order_data(trade_object)

    logger.info(f"Step 2: Update order with sl_type: {sl_type.capitalize()!r} - tp_type: {tp_type.capitalize()!r}")
    android.trade_screen.modals.modify_order(trade_object, sl_type=sl_type, tp_type=tp_type)

    logger.info("Verify edit confirmation info")
    android.trade_screen.modals.verify_edit_trade_confirmation(trade_object)

    logger.info("Step 3: Confirm update order")
    android.trade_screen.modals.confirm_update_order()

    logger.info("Verify notification banner updated message")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner(**trade_object))

    logger.info(f"Verify item details after updated")
    android.trade_screen.asset_tab.verify_item_data(trade_object)
