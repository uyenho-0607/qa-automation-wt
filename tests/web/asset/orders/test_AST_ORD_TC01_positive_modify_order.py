import random

import pytest

from src.apis.api_client import APIClient
from src.data.enums import SLTPType, OrderType, Features, AssetTabs
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize("order_type", (
        [
            OrderType.MARKET,
            random.choice([OrderType.LIMIT, OrderType.STOP]),
            OrderType.STOP_LIMIT,
        ]
))
def test(web, symbol, close_edit_confirm_modal, order_type):
    trade_object = ObjTrade(order_type=order_type, symbol=symbol)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    APIClient().trade.post_order(trade_object, update_price=True)

    logger.info("Step 2: Navigate to Asset Page")
    web.home_page.navigate_to(Features.ASSETS)

    logger.info(f"Step 3: Select tab: {AssetTabs.get_tab(order_type)}")
    web.assets_page.asset_tab.select_tab(AssetTabs.get_tab(order_type))

    logger.info(f" Step 4: Update order with SL and TP")
    web.assets_page.asset_tab.modify_order(trade_object, sl_type=SLTPType.random_values(), tp_type=SLTPType.random_values())

    logger.info("Verify trade edit confirmation")
    web.assets_page.modals.verify_edit_trade_confirmation(trade_object)

    logger.info("Step 5: Confirm update order")
    web.assets_page.modals.confirm_update_order()

    logger.info(f"Verify notification banner updated message")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner(**trade_object))

    logger.info(f"Verify item details in Asset Page")
    web.assets_page.asset_tab.verify_item_data(trade_object)
