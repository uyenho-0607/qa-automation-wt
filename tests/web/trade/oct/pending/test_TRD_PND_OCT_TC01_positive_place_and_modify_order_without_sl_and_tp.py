import random

import pytest

from src.data.enums import AssetTabs, SLTPType, OrderType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize("order_type", [random.choice([OrderType.LIMIT, OrderType.STOP_LIMIT]), OrderType.STOP_LIMIT])
@pytest.mark.parametrize(
    "update_field, sl_type, tp_type",
    [
        ("SL", SLTPType.random_values(), None),
        ("TP", None, SLTPType.random_values()),
        ("SL, TP", *SLTPType.random_values(amount=2)),
    ]
)
def test(web, symbol, get_asset_tab_amount, update_field, sl_type, tp_type, close_edit_confirm_modal, order_type):

    trade_object = ObjTrade(order_type=order_type, symbol=symbol)
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order without SL and TP")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=None, tp_type=None)

    logger.info("Verify notification banner displays correct input trade information")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_submitted_banner())

    logger.info(f"Verify Asset Tab amount is: {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount + 1)

    logger.info(f"Verify Asset Tab item details")
    web.trade_page.asset_tab.verify_item_data(trade_object)

    logger.info(f" Step 2: Update Asset Tab item with {update_field!r}")
    web.trade_page.asset_tab.modify_order(trade_object, sl_type=sl_type, tp_type=tp_type)

    logger.info("Verify notification banner updated message")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner())

    logger.info(f"Verify Asset Tab item details after update")
    web.trade_page.asset_tab.verify_item_data(trade_object)
