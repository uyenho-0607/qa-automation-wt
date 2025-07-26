import random

import pytest

from src.data.enums import AssetTabs, SLTPType, OrderType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize(
    "update_field",
    [
        "SL",
        "TP",
        "SL,TP",
    ]
)
def test(web, symbol, get_asset_tab_amount, update_field, close_edit_confirm_modal, ):

    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)
    sl_type, tp_type = random.sample([None, SLTPType.random_values()], k=2)
    update_info = {f"{item.lower()}_type": SLTPType.random_values() for item in update_field.split(",")}

    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order, sl_type: {sl_type}, tp_type: {tp_type}")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type)

    logger.info("Verify notification banner displays correct input trade information")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_submitted_banner())

    logger.info(f"Verify Asset Tab amount: {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info(f"Verify item details in Asset Tab")
    web.trade_page.asset_tab.verify_item_data(trade_object)

    logger.info("Verify Open Position noti in Notification Box")
    web.home_page.notifications.verify_notification_result(ObjNoti(trade_object).open_position_details(trade_object.order_id))

    logger.info(f"Step 2: Modify order with {update_field!r} {' - '.join(list(update_info.values()))}")
    web.trade_page.modals.modify_order(trade_object, **update_info)

    logger.info("Verify notification banner updated message")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner(**trade_object))

    logger.info(f"Verify order details after update")
    web.trade_page.asset_tab.verify_item_data(trade_object)
