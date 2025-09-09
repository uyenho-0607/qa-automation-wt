import random

import pytest

from src.data.enums import AssetTabs, SLTPType, OrderType, Expiry
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize(
    "edit_field, sl_type, tp_type",
    random.choices([
        ("SL, TP", SLTPType.PRICE, SLTPType.PRICE),
        ("SL, TP", SLTPType.POINTS, SLTPType.POINTS),
    ])
)
def test(android, symbol, edit_field, sl_type, tp_type, create_order_data):
    trade_object = ObjTrade(order_type=OrderType.STOP_LIMIT, symbol=symbol, expiry=Expiry.sample_values(OrderType.STOP))
    tab = AssetTabs.PENDING_ORDER
    # -------------------

    logger.info(f"Step 1: Place {trade_object.trade_type.upper()} {trade_object.order_type.upper()} order")
    create_order_data(trade_object)

    logger.info(f"Step 2: Select Pending Orders tab")
    android.trade_screen.asset_tab.select_tab(tab)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    android.trade_screen.asset_tab.verify_item_displayed(tab, trade_object.order_id)

    logger.info(f"Step 3: Modify order with {edit_field!r}")
    android.trade_screen.modals.modify_order(trade_object, sl_type=sl_type, tp_type=tp_type)

    logger.info("Verify notification banner updated message")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner())

    logger.info(f"Step 4: Select Pending Orders tab")
    android.trade_screen.asset_tab.select_tab(tab)

    logger.info(f"Verify {tab.title()} item details after update")
    android.trade_screen.asset_tab.verify_item_data(trade_object, wait=True)
