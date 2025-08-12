import random

import pytest

from src.data.enums import SLTPType, OrderType, Features, AssetTabs
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize("order_type", (
        [
            OrderType.MARKET,
            OrderType.STOP_LIMIT,
            random.choice([OrderType.LIMIT, OrderType.STOP])
        ]
))
def test(web, symbol, search_symbol, close_edit_confirm_modal, order_type):
    trade_object = ObjTrade(order_type=order_type, symbol=symbol)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=SLTPType.sample_values(), tp_type=SLTPType.sample_values())
    web.home_page.notifications.close_noti_banner()

    logger.info("Step 2: Navigate to Asset Page")
    web.home_page.navigate_to(Features.ASSETS, wait=True)

    logger.info(f"Step 3: Select tab: {AssetTabs.get_tab(order_type)}")
    web.trade_page.asset_tab.select_tab(AssetTabs.get_tab(order_type))

    logger.info(f"Verify item details in Asset Page")
    web.assets_page.asset_tab.verify_item_data(trade_object)

    logger.info(f" Step 4: Update placed order")
    web.assets_page.asset_tab.modify_order(trade_object, sl_type=SLTPType.random_values(), tp_type=SLTPType.random_values(), oct_mode=True)

    logger.info(f"Verify notification banner updated message")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner(**trade_object))

    logger.info(f"Step 5: Select tab: {AssetTabs.get_tab(order_type)}")
    web.trade_page.asset_tab.select_tab(AssetTabs.get_tab(order_type))

    logger.info(f"Verify item details after updated")
    web.assets_page.asset_tab.verify_item_data(trade_object, wait=True)
