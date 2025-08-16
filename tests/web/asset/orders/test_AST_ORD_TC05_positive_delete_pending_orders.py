import random

import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, OrderType, Features
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize('order_type', (
        [
            OrderType.STOP_LIMIT,
            random.choice([OrderType.LIMIT, OrderType.STOP])
        ]
))
def test(web, symbol, order_type):
    trade_object = ObjTrade(order_type=order_type, symbol=symbol)
    # -------------------

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    APIClient().trade.post_order(trade_object, update_price=True)

    logger.info("Step 2: Select Pending Orders tab")
    web.assets_page.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info("Step 3: Delete pending order")
    web.assets_page.asset_tab.delete_order(trade_object)

    logger.info(f"Verify notification banner deleted message")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).delete_order_banner())

    logger.info("Verify item is no longer displayed")
    web.trade_page.asset_tab.verify_item_displayed(AssetTabs.PENDING_ORDER, trade_object.order_id, is_display=False)
