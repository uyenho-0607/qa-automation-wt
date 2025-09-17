import random

import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, OrderType, Features
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize("order_type", (
    [
        random.choice([OrderType.STOP, OrderType.LIMIT]),
        OrderType.STOP_LIMIT
    ]
))
def test(android, symbol, order_type, cancel_all):
    trade_object = ObjTrade(order_type=order_type, symbol=symbol)

    logger.info("Step 1: Navigate to Asset Page")
    android.home_screen.navigate_to(Features.ASSETS)

    logger.info("Step 2: Click on View all Transaction tab")
    android.assets_screen.click_view_all_transaction()

    logger.info("Step 3: Select Pending Orders tab")
    android.trade_screen.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info(f"Step 4: Place {trade_object.trade_type} Order")
    APIClient().trade.post_order(trade_object, update_price=True)

    logger.info(f"Verify order placed successfully, order_id = {trade_object.order_id!r}")
    android.trade_screen.asset_tab.verify_item_displayed(tab=AssetTabs.PENDING_ORDER, order_id=trade_object.order_id)

    logger.info("Step 5: Delete pending order")
    android.trade_screen.asset_tab.delete_order(trade_object=trade_object, confirm=True)

    logger.info(f"Verify notification banner pending orders deleted")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).delete_order_banner())

    logger.info("Verify item is no longer displayed")
    android.trade_screen.asset_tab.verify_item_displayed(AssetTabs.PENDING_ORDER, trade_object.order_id, is_display=False)