import random
import pytest

from src.data.enums import SLTPType, OrderType, Expiry
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize(
    "update_field",
    [
        "SL",
        "TP",
        "SL,TP",
    ]
)
def test(web, update_field, close_edit_confirm_modal, symbol, create_order_data):

    update_info = {f"{field.lower()}_type": SLTPType.random_values() for field in update_field.split(",")}

    exclude_field = random.choice(["stop_loss", "take_profit"])  # the field will be set to zero
    trade_object = ObjTrade(order_type=OrderType.LIMIT, symbol=symbol)
    trade_object[exclude_field] = 0

    logger.info(f"Step 1: Place order with only SL/ TP ({exclude_field} = 0)")
    create_order_data(trade_object)

    logger.info(f"Step 2: Modify order with {update_field!r} {' - '.join(list(update_info.values()))}")
    web.trade_page.modals.modify_order(trade_object, **update_info, expiry=Expiry.sample_values(trade_object.order_type))

    logger.info("Verify edit confirmation info")
    web.trade_page.modals.verify_edit_trade_confirmation(trade_object)

    logger.info("Step 3: Confirm update order")
    web.trade_page.modals.confirm_update_order()

    logger.info("Verify notification banner updated message")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner())

    logger.info("Verify item details after update")
    web.trade_page.asset_tab.verify_item_data(trade_object)
