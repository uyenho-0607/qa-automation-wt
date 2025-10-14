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
def test(web_app, symbol, order_type, cancel_all):
    trade_object = ObjTrade(order_type=order_type, symbol=symbol)

    logger.info("Step 1: Navigate to Asset Page")
    web_app.home_page.navigate_to(Features.ASSETS)

    logger.info("Step 2: Click on View all Transaction tab")
    web_app.assets_page.click_view_all_transaction()

    logger.info("Step 3: Select Pending Orders tab")
    web_app.trade_page.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info(f"Step 4: Place {trade_object.trade_type} Order")
    APIClient().trade.post_order(trade_object, update_price=True)

    logger.info(f"Verify order placed successfully, order_id = {trade_object.order_id!r}")
    web_app.trade_page.asset_tab.verify_item_displayed(tab=AssetTabs.PENDING_ORDER, order_id=trade_object.order_id)

    logger.info("Step 5: Delete pending order")
    web_app.trade_page.asset_tab.delete_order(trade_object=trade_object, confirm=True)

    logger.info(f"Verify notification banner pending orders deleted")
    web_app.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).delete_order_banner())

    logger.info("Verify item is no longer displayed")
    web_app.trade_page.asset_tab.verify_item_displayed(AssetTabs.PENDING_ORDER, trade_object.order_id, is_display=False)