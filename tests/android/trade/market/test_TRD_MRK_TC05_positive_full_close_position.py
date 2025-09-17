import pytest

from src.data.enums import AssetTabs, OrderType, Features
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(android, symbol, get_asset_tab_amount, create_order_data):
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    android.trade_screen.place_order_panel.place_order(trade_object, submit=True)

    logger.info(f"Verify Order Submitted Notification")
    android.home_screen.notifications.verify_notification_banner(expected_title=ObjNoti(trade_object).order_submitted_banner()[0])

    logger.info("Step 1: Get asset tab amount")
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info("Step 2: Full close position")
    android.trade_screen.asset_tab.full_close_position(trade_object)

    logger.info(f"Verify close order notification banner")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).close_order_success_banner())

    logger.info("Step 3: Navigate to Home screen")
    android.trade_screen.navigate_to(Features.HOME)

    logger.info(f"Verify Position Closed noti in notification box")
    android.home_screen.notifications.verify_notification_result(ObjNoti(trade_object).position_closed_details(), close=True)

    logger.info("Step 4: Navigate to Trade screen")
    android.home_screen.navigate_to(Features.TRADE)

    logger.info(f"Verify item no longer displays in Open Positions tab")
    android.trade_screen.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, trade_object.order_id, is_display=False)

    logger.info(f"Verify asset tab amount = {tab_amount - 1}")
    android.trade_screen.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount - 1)

    logger.info(f"Step 5: Select tab {AssetTabs.HISTORY.value.capitalize()}")
    android.trade_screen.asset_tab.select_tab(AssetTabs.HISTORY)

    logger.info(f"Verify history order item details")
    android.trade_screen.asset_tab.verify_item_data(trade_object, AssetTabs.POSITIONS_HISTORY)


@pytest.fixture(autouse=True)
def teardown(android, cancel_all):
    yield
    logger.info("[Cleanup] Navigate to Trade screen")
    android.home_screen.navigate_to(Features.TRADE)

    logger.info("[Cleanup] Select Open Positions tab")
    android.trade_screen.asset_tab.select_tab(AssetTabs.OPEN_POSITION)
