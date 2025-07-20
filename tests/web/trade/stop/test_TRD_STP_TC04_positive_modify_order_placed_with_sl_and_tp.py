import pytest

from src.data.enums import SLTPType, OrderType, Expiry
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
def test(web, symbol, create_order_data, sl_type, tp_type, close_edit_confirm_modal):
    trade_object = ObjTrade(order_type=OrderType.STOP, symbol=symbol, indicate=SLTPType.sample_values())
    # -------------------

    logger.info(f"Step 1: Place {trade_object.trade_type} Order with SL and TP")
    create_order_data(trade_object)

    logger.info(f"Step 2: Update order with SL ({sl_type.capitalize()}), TP ({tp_type.capitalize()})")
    web.trade_page.modals.modify_order(trade_object, sl_type=sl_type, tp_type=tp_type, expiry=Expiry.sample_values(trade_object.order_type))

    logger.info("Verify edit confirmation info")
    web.trade_page.modals.verify_edit_trade_confirmation(trade_object)

    logger.info("Step 3: Confirm update order")
    web.trade_page.modals.confirm_update_order()

    logger.info("Verify notification banner updated message")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner())

    logger.info(f"Verify item details after update")
    web.trade_page.asset_tab.verify_item_data(trade_object)
