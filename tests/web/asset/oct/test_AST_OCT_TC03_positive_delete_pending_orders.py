import random

import pytest

from src.data.enums import AssetTabs, SLTPType, OrderType, Features
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize("order_type", (
        [
            OrderType.STOP_LIMIT,
            random.choice([OrderType.STOP, OrderType.LIMIT]),
        ]
))
def test(web, symbol, search_symbol, order_type, cancel_close_order):
    trade_object = ObjectTrade(order_type=order_type, symbol=symbol)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    web.trade_page.place_order_panel.place_order(trade_object)
    web.home_page.notifications.close_noti_banner()

    logger.info("Step 2: Navigate to Asset Page")
    web.home_page.navigate_to(Features.ASSETS, wait=True)

    logger.info("Step 3: Get order_id from asset tab")
    web.assets_page.asset_tab.get_last_order_id(trade_object)

    logger.info("Step 4: Delete pending order")
    web.assets_page.asset_tab.delete_pending_order(trade_object=trade_object, confirm=False)

    logger.info(f"Verify notification banner pending orders deleted")
    web.home_page.notifications.verify_notification_banner(*ObjectNoti(trade_object).delete_order_banner())

    logger.info("Verify item is no longer displayed")
    web.trade_page.asset_tab.verify_item_displayed(AssetTabs.PENDING_ORDER, trade_object.order_id, is_display=False)
