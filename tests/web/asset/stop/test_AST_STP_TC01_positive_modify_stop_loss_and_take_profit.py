import random

import pytest

from src.data.enums import AssetTabs, SLTPType, OrderType, Expiry, Features
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize(
    "edit_field, sl_type, tp_type",
    [
        ("stop_loss", SLTPType.sample_values(), None),
        ("take_profit", None, SLTPType.sample_values()),
        ("stop_loss, take_profit", *SLTPType.sample_values(amount=2)),
    ]
)
def test(web, symbol, edit_field, sl_type, tp_type, close_edit_confirm_modal, search_symbol, update_entry_price):
    # -------------------
    trade_object = ObjectTrade(order_type=OrderType.STOP, symbol=symbol)
    tab = AssetTabs.PENDING_ORDER
    update_expiry = Expiry.sample_values(trade_object.order_type)
    order_sl_type = random.choice([None, SLTPType.sample_values()])
    order_tp_type = random.choice([None, SLTPType.sample_values()])
    # -------------------

    logger.info(f"Step 1: Place {trade_object.trade_type} Order with SL: {order_sl_type!r}, TP: {order_tp_type!r}")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=order_sl_type, tp_type=order_tp_type, submit=True)
    web.home_page.notifications.close_noti_banner()

    logger.info("Step 2: Navigate to Asset Page")
    web.home_page.navigate_to(Features.ASSETS, wait=True)

    logger.info(f"Verify {tab.title()} item details in Asset Page")
    update_entry_price(trade_object)
    web.assets_page.asset_tab.verify_item_data(trade_object)

    logger.info(f" Step 3: Update {tab.title()} with {edit_field!r}, expiry = {update_expiry!r}")
    web.assets_page.modals.modify_order(trade_object, sl_type=sl_type, tp_type=tp_type, expiry=update_expiry)

    logger.info("Verify edit confirmation info")
    web.assets_page.modals.verify_edit_trade_confirmation(trade_object)

    logger.info("Step 4: Confirm update order")
    web.assets_page.modals.confirm_update_order()

    logger.info(f"Verify {tab.title()} notification banner updated message")
    web.home_page.notifications.verify_notification_banner(*ObjectNoti(trade_object).order_updated_banner(**trade_object))

    logger.info(f"Verify {tab.title()} item details in Asset Page")
    web.assets_page.asset_tab.verify_item_data(trade_object)
