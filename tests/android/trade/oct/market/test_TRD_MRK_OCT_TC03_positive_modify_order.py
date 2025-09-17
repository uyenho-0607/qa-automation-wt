import random

import pytest

from src.data.enums import AssetTabs, SLTPType, OrderType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize("edit_field, sl_type, tp_type", [("SL, TP", SLTPType.PRICE, SLTPType.PRICE)])
def test(android, symbol, edit_field, sl_type, tp_type, create_order_data, ):
    # -------------------
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)
    tab = AssetTabs.OPEN_POSITION
    # -------------------

    logger.info(f"Step 1: Place {trade_object.trade_type.upper()} {trade_object.order_type.upper()} order")
    create_order_data(trade_object)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    android.trade_screen.asset_tab.verify_item_displayed(tab, trade_object.order_id)

    logger.info(f"Step 2: Update {tab.title()} item with {edit_field!r} ({sl_type}, {tp_type})")
    android.trade_screen.asset_tab.modify_order(trade_object, sl_type=sl_type, tp_type=tp_type, confirm=False)

    logger.info("Verify Order Updated Notification banner")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner())

    logger.info(f"Verify {tab.title()} item details after update")
    android.trade_screen.asset_tab.verify_item_data(trade_object, wait=True)