import pytest

from src.data.enums import AssetTabs, Features
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(android, order_data, market_obj, get_asset_tab_amount):
    trade_object = market_obj()

    logger.info("Step 1: Get asset tab amount")
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info("Step 2: Open pre-trade details")
    android.trade_screen.place_order_panel.open_pre_trade_details()

    logger.info(f"Step 3: Place order with: {format_display_dict(trade_object)} (tab:{tab_amount})")
    order_data(trade_object, None, None)
    trade_object.order_id = android.trade_screen.asset_tab.get_last_order_id(AssetTabs.OPEN_POSITION, wait=True)

    logger.info(f"Verify order placed successfully, tab = {tab_amount + 1}")
    android.trade_screen.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info("Step 5: Full close position")
    trade_object.current_price = android.trade_screen.asset_tab.get_current_price(trade_object.trade_type, trade_object.order_type, oct_mode=True)
    android.trade_screen.asset_tab.full_close_position(trade_object.order_id, confirm=False)

    logger.info("Verify Close Order notification banner")
    exp_noti = ObjNoti(trade_object)
    android.home_screen.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    logger.info("Step 6: Navigate to Home Screen")
    android.trade_screen.navigate_to(Features.HOME)

    logger.info("Verify Position Closed noti in notification box")
    android.home_screen.notifications.verify_notification_result(exp_noti.position_closed_details(), close=True)

    logger.info("Step 7: Navigate back to Trade Screen")
    android.home_screen.navigate_to(Features.TRADE, wait=True)

    logger.info(f"Verify asset tab amount = {tab_amount}")
    android.trade_screen.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount)

    logger.info(f"Verify item is no longer displayed in Open Positions tab")
    android.trade_screen.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, trade_object.order_id, is_display=False)

    logger.info(f"Step 8: Select tab {AssetTabs.HISTORY.value.capitalize()}")
    android.trade_screen.asset_tab.select_tab(AssetTabs.HISTORY)

    logger.info("Verify history order item details")
    android.trade_screen.asset_tab.verify_item_data(trade_object, AssetTabs.POSITIONS_HISTORY)


@pytest.fixture(autouse=True)
def teardown(android, cancel_all):

    yield
    logger.info("[Cleanup] Navigate back to Trade Screen", teardown=True)
    android.home_screen.navigate_to(Features.TRADE)

    logger.info("[Cleanup] Select Open Positions tab", teardown=True)
    android.trade_screen.asset_tab.select_tab(AssetTabs.OPEN_POSITION)