import random
import time
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
        OrderType.STOP_LIMIT
    ]
))
def test(android, symbol, order_type):
    trade_object = ObjTrade(order_type=order_type, symbol=symbol)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    APIClient().trade.post_order(trade_object, update_price=True)

    logger.info("Step 2: Navigate to Asset Page")
    android.home_screen.navigate_to(Features.ASSETS)

    logger.info("Step 3: Click on View all Transaction tab")
    android.assets_screen.click_view_all_transaction()

    logger.info(f"Step 4: Select tab: {AssetTabs.get_tab(order_type)}")
    android.trade_screen.asset_tab.select_tab(AssetTabs.get_tab(order_type))

    logger.info(f"Step 5: Update placed order")
    android.trade_screen.modals.modify_order(trade_object, sl_type=SLTPType.random_values(), tp_type=SLTPType.random_values())

    logger.info(f"Verify trade edit confirmation")
    android.trade_screen.modals.verify_edit_trade_confirmation(trade_object)

    logger.info("Step 6: Confirm update order")
    android.trade_screen.modals.confirm_update_order()

    logger.info(f"Verify notification banner updated message")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner(**trade_object))

    logger.info(f"Step 7: Select tab: {AssetTabs.get_tab(order_type)}")
    android.trade_screen.asset_tab.select_tab(AssetTabs.get_tab(order_type))

    logger.info(f"Verify item details after updated")
    android.trade_screen.asset_tab.verify_item_data(trade_object, wait=True)


@pytest.fixture(autouse=True)
def setup_test(android):
    yield
    logger.info("[Cleanup] Navigate back to Asset Screen")
    android.home_screen.go_back()
