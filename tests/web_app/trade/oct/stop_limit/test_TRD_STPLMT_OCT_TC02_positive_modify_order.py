import random

import pytest

from src.data.enums import AssetTabs, SLTPType, OrderType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize("edit_field, sl_type, tp_type", [("SL, TP", SLTPType.PRICE, SLTPType.PRICE)])
def test(web_app, symbol, edit_field, sl_type, tp_type, create_order_data):
    trade_object = ObjTrade(order_type=OrderType.STOP_LIMIT, symbol=symbol)
    tab = AssetTabs.PENDING_ORDER
    # -------------------

    logger.info(f"Step 1: Place {trade_object.trade_type.upper()} {trade_object.order_type.upper()} order")
    create_order_data(trade_object)

    logger.info(f"Step 2: Select Pending Orders tab")
    web_app.trade_page.asset_tab.select_tab(tab)

    logger.info(f"Step 3: Update {tab.title()} item with {edit_field!r}")
    web_app.trade_page.asset_tab.modify_order(trade_object, sl_type=sl_type, tp_type=tp_type, oct_mode=True)

    logger.info("Verify Order Updated Notification banner")
    web_app.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner())

    logger.info(f"Step 4: Select Pending Orders tab")
    web_app.trade_page.asset_tab.select_tab(tab)

    logger.info(f"Verify {tab.title()} item details after update")
    web_app.trade_page.asset_tab.verify_item_data(trade_object)
