import random

import pytest

from src.data.enums import TradeType, AssetTabs, SLTPType, OrderType, Expiry
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize(
    "sl_type, tp_type, edit_sl_type, edit_tp_type",
    [
        (SLTPType.POINTS, SLTPType.POINTS, SLTPType.POINTS, SLTPType.POINTS),
        (SLTPType.PRICE, SLTPType.PRICE, SLTPType.PRICE, SLTPType.PRICE),
        (*SLTPType.sample_values(amount=2), *SLTPType.sample_values(amount=2)),
        random.choices(SLTPType.list_values(), k=4),
    ]
)
def test(web, symbol, get_asset_tab_amount, sl_type, tp_type, edit_sl_type, edit_tp_type, close_edit_confirm_modal):
    trade_object = ObjectTrade(TradeType.SELL, OrderType.STOP, symbol=symbol)
    tab_amount = get_asset_tab_amount(trade_object.order_type)
    # ------------------- #

    logger.info(f"Step 1: Place {trade_object.trade_type} Order with Stop Loss ({sl_type.capitalize()}) and Take Profit ({tp_type.capitalize()})")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type)

    logger.info("Verify notification banner displays correct input trade information")
    web.home_page.notifications.verify_notification_banner(*ObjectNoti(trade_object).order_submitted_banner())

    logger.info(f"Verify amount is: {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount + 1)

    logger.info(f"Verify item details in Asset Tab")
    web.trade_page.asset_tab.verify_item_data(trade_object)

    logger.info(f" Step 2: Update item with Stop Loss ({edit_sl_type.capitalize()}), Take Profit ({edit_tp_type.capitalize()})")
    web.trade_page.modals.modify_order(trade_object, sl_type=edit_sl_type, tp_type=edit_tp_type, expiry=Expiry.sample_values(trade_object.order_type))

    logger.info("Verify notification banner updated message")
    web.home_page.notifications.verify_notification_banner(*ObjectNoti(trade_object).order_updated_banner())

    logger.info(f"Verify item details after update")
    web.trade_page.asset_tab.verify_item_data(trade_object)
