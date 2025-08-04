import random

import pytest

from src.data.enums import AssetTabs
from src.data.enums import SLTPType, OrderType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize(
    "exclude_field, update_field",
    [
        ("SL", "SL"),
        pytest.param("SL", "TP", marks=pytest.mark.critical),
        ("SL", "SL,TP"),
        pytest.param("TP", "SL", marks=pytest.mark.critical),
        ("TP", "TP"),
        ("TP", "SL,TP"),
    ]
)
def test(android, symbol, get_asset_tab_amount, exclude_field, update_field, create_order_data, close_edit_confirmation):

    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)
    trade_object[exclude_field] = 0
    update_info = {f"{item.lower()}_type": SLTPType.random_values() for item in update_field.split(",")}
    # -------------------

    logger.info(f"Step 1: Place {trade_object.trade_type} Order with SL/ TP ({exclude_field} = 0)")
    create_order_data(trade_object)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    android.trade_screen.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, trade_object.order_id)

    logger.info(f"Step 2: Modify order with {update_field!r} {' - '.join(list(update_info.values()))}")
    android.trade_screen.modals.modify_order(trade_object, **update_info)

    logger.info(f"Verify trade edit confirmation")
    android.trade_screen.modals.verify_edit_trade_confirmation(trade_object)

    logger.info("Step 3: Confirm update order")
    android.trade_screen.modals.confirm_update_order()

    logger.info(f"Verify order updated notification banner")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner(**trade_object))

    logger.info(f"Verify order details after update")
    android.trade_screen.asset_tab.verify_item_data(trade_object)
