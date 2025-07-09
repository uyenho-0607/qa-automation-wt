import random

import pytest

from src.data.enums import AssetTabs, SLTPType, OrderType
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize(
    "sl_type, tp_type, edit_sl_type, edit_tp_type",
    [
        (SLTPType.POINTS, SLTPType.POINTS, SLTPType.POINTS, SLTPType.POINTS),
        (SLTPType.PRICE, SLTPType.PRICE, SLTPType.PRICE, SLTPType.PRICE),
        (*SLTPType.sample_values(amount=2), *SLTPType.sample_values(amount=2)),
    ]
)
def test(web, symbol, get_asset_tab_amount, sl_type, tp_type, edit_sl_type, edit_tp_type, close_edit_confirm_modal, update_entry_price):
    trade_object = ObjectTrade(order_type=OrderType.MARKET, symbol=symbol)
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order with Stop Loss ({sl_type.capitalize()}) and Take Profit ({tp_type.capitalize()})")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type)

    logger.info("Verify notification banner displays correct input trade information")
    web.home_page.notifications.verify_notification_banner(*ObjectNoti(trade_object).order_submitted_banner())

    logger.info(f"Verify Asset Tab amount is: {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info(f"Verify item details in Asset Tab")
    update_entry_price(trade_object)
    web.trade_page.asset_tab.verify_item_data(trade_object)

    logger.info("Verify Open Position noti in Notification Box")
    web.home_page.notifications.verify_notification_result(ObjectNoti(trade_object).open_position_details(order_id=trade_object.order_id))

    logger.info(f"Step 2: Update order with SL ({edit_sl_type.capitalize()}), TP ({edit_tp_type.capitalize()})")
    web.trade_page.modals.modify_order(trade_object, sl_type=edit_sl_type, tp_type=edit_tp_type)

    logger.info("Verify notification banner updated message")
    web.home_page.notifications.verify_notification_banner(*ObjectNoti(trade_object).order_updated_banner(**trade_object))

    logger.info(f"Verify order details after update")
    web.trade_page.asset_tab.verify_item_data(trade_object)
