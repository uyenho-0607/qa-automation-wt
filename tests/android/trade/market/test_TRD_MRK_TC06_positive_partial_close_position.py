import random

import pytest

from src.data.enums import AssetTabs, Features
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger

@pytest.mark.critical
def _test(android, market_obj, get_asset_tab_amount, order_data):
    trade_object = market_obj(volume=random.randint(5, 10))
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)}")
    order_data(trade_object)
    trade_object.order_id = android.trade_screen.asset_tab.get_last_order_id(AssetTabs.PENDING_ORDER, wait=True)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    android.trade_screen.asset_tab.verify_item_data(trade_object, AssetTabs.OPEN_POSITION, wait=False)

    logger.info("Step 2: Partial close position")
    new_object = android.trade_screen.asset_tab.partial_close_position(trade_object)

    logger.info(f"Verify close order notification banner")
    exp_noti = ObjNoti(trade_object)
    android.home_screen.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    logger.info(f"Verify asset tab amount = {tab_amount}")
    android.trade_screen.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount)

    logger.info(f"Verify Open Position details in asset tab")
    android.trade_screen.asset_tab.verify_item_data(new_object)

    logger.info(f"Step 3: Select tab {AssetTabs.HISTORY.value.capitalize()}")
    android.trade_screen.asset_tab.select_tab(AssetTabs.HISTORY)

    logger.info(f"Verify history order item details")
    android.trade_screen.asset_tab.verify_item_data(trade_object, AssetTabs.POSITIONS_HISTORY)

    logger.info("Step 4: Navigate to Home screen")
    android.trade_screen.navigate_to(Features.HOME)

    logger.info(f"Verify position closed noti in notification box")
    android.home_screen.notifications.verify_notification_result(exp_noti.position_closed_details(), close=True)


@pytest.fixture(autouse=True)
def teardown(android, cancel_all):
    yield
    logger.info("- Navigate to Trade screen", teardown=True)
    android.home_screen.navigate_to(Features.TRADE)

    logger.info("- Select Open Positions tab", teardown=True)
    android.trade_screen.asset_tab.select_tab(AssetTabs.OPEN_POSITION)