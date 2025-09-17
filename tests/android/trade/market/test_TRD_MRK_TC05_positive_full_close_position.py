import pytest

from src.data.enums import AssetTabs, Features
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(android, market_obj, get_asset_tab_amount, order_data):
    trade_object = market_obj()
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)} (tab:{tab_amount})")
    order_data(trade_object)
    trade_object.order_id = android.trade_screen.asset_tab.get_last_order_id(AssetTabs.OPEN_POSITION, wait=True)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    android.trade_screen.asset_tab.verify_item_data(trade_object, AssetTabs.OPEN_POSITION, wait=False)

    logger.info("Step 2: Full close position")
    trade_object.current_price = android.trade_screen.place_order_panel.get_current_price(trade_object.trade_type, trade_object.order_type)
    android.trade_screen.asset_tab.full_close_position(trade_object.order_id)

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

    logger.info(f"Verify asset tab amount = {tab_amount}")
    android.trade_screen.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount)

    logger.info(f"Step 5: Select tab {AssetTabs.HISTORY.value.capitalize()}")
    android.trade_screen.asset_tab.select_tab(AssetTabs.HISTORY)

    logger.info(f"Verify history order item details")
    android.trade_screen.asset_tab.verify_item_data(trade_object, AssetTabs.POSITIONS_HISTORY)


@pytest.fixture(autouse=True)
def teardown(android, cancel_all):
    yield
    logger.info("[Cleanup] Navigate to Trade screen", teardown=True)
    android.home_screen.navigate_to(Features.TRADE)

    logger.info("[Cleanup] Select Open Positions tab", teardown=True)
    android.trade_screen.asset_tab.select_tab(AssetTabs.OPEN_POSITION)
