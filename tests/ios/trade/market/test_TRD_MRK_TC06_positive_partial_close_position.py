import random

import pytest

from src.data.enums import AssetTabs, Features
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(ios, symbol, get_asset_tab_amount, order_data, market_obj):
    trade_object = market_obj(volume=random.randint(2, 3))
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)}")
    order_data(trade_object, None, None)
    trade_object.order_id = ios.trade_screen.asset_tab.get_last_order_id(AssetTabs.OPEN_POSITION, True)

    logger.info(f"Verify tab amount increased to {tab_amount + 1}, adding order_id: {trade_object.order_id!r}")
    ios.trade_screen.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info(f"Step 2: Partial close position, order_id: {trade_object.order_id!r}")
    open_trade_object = ios.trade_screen.asset_tab.partial_close_position(trade_object)
    open_trade_object.order_id = ios.trade_screen.asset_tab.get_last_order_id(AssetTabs.OPEN_POSITION, True)

    logger.info(f"Verify close order notification banner")
    exp_noti = ObjNoti(trade_object)
    ios.home_screen.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    logger.info(f"Verify asset tab amount = {tab_amount + 1}")
    ios.trade_screen.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info(f"Verify Open Position details in asset tab")
    ios.trade_screen.asset_tab.verify_item_data(open_trade_object)

    logger.info(f"Step 3: Select tab {AssetTabs.HISTORY.value.capitalize()}")
    ios.trade_screen.asset_tab.select_tab(AssetTabs.HISTORY)

    logger.info(f"Verify history order item details")
    ios.trade_screen.asset_tab.verify_item_data(trade_object, AssetTabs.POSITIONS_HISTORY)

    logger.info("Step 4: Navigate to Home screen")
    ios.trade_screen.navigate_to(Features.HOME)

    logger.info(f"Verify position closed noti in notification box")
    ios.home_screen.notifications.verify_notification_result(exp_noti.position_closed_details(), close=True)


@pytest.fixture(autouse=True)
def teardown(ios, cancel_all):
    yield
    logger.info("[Cleanup] Navigate to Trade screen", teardown=True)
    ios.home_screen.navigate_to(Features.TRADE)

    logger.info("[Cleanup] Select Open Positions tab", teardown=True)
    ios.trade_screen.asset_tab.select_tab(AssetTabs.OPEN_POSITION)
