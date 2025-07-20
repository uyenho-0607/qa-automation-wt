import random

import pytest

from src.data.enums import AssetTabs, SLTPType, OrderType
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize("order_type", [random.choice([OrderType.LIMIT, OrderType.STOP]), OrderType.STOP_LIMIT])
def test(web, symbol, get_asset_tab_amount, close_edit_confirm_modal, order_type):
    trade_object = ObjectTrade(order_type=OrderType.LIMIT, symbol=symbol)
    tab_amount = get_asset_tab_amount(trade_object.order_type)
    # ------------------- #
    logger.info(f"Step 1: Place {trade_object.trade_type} Order with  SL & TP")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=SLTPType.random_values(), tp_type=SLTPType.random_values())

    logger.info("Verify notification banner displays correct input trade information")
    web.home_page.notifications.verify_notification_banner(*ObjectNoti(trade_object).order_submitted_banner())

    logger.info(f"Verify Asset Tab amount is: {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount + 1)

    logger.info(f"Verify Asset Tab item details")
    web.trade_page.asset_tab.verify_item_data(trade_object)

    logger.info(f"Step 2: Update order with SL & TP")
    web.trade_page.modals.modify_order(trade_object, sl_type=SLTPType.random_values(), tp_type=SLTPType.random_values())

    logger.info("Verify notification banner updated message")
    web.home_page.notifications.verify_notification_banner(*ObjectNoti(trade_object).order_updated_banner())

    logger.info(f"Verify Asset Tab item details after update")
    web.trade_page.asset_tab.verify_item_data(trade_object)
