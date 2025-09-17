import pytest

from src.data.enums import AssetTabs, OrderType, Features
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(android, symbol, create_order_data):
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)

    logger.info(f"Step 1: Place {trade_object.trade_type.upper()} {trade_object.order_type.upper()} Order")
    *_, tab_amount = create_order_data(trade_object)

    logger.info(f"Verify order placed successfully, order_id = {trade_object.order_id!r} (tab:{tab_amount!r})")
    android.trade_screen.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, trade_object.order_id)

    logger.info("Step 2: Full close position")
    android.trade_screen.asset_tab.full_close_position(trade_object, trade_object.order_id, confirm=False)

    logger.info("Verify Close Order notification banner")
    exp_noti = ObjNoti(trade_object)
    android.home_screen.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    logger.info("Step 3: Navigate to Home Screen")
    android.trade_screen.navigate_to(Features.HOME)

    logger.info("Verify Position Closed noti in notification box")
    android.home_screen.notifications.verify_notification_result(exp_noti.position_closed_details(), close=True)

    logger.info("Step 4: Navigate back to Trade Screen")
    android.home_screen.navigate_to(Features.TRADE, wait=True)

    logger.info(f"Verify asset tab amount = {tab_amount - 1}")
    android.trade_screen.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount - 1)

    logger.info(f"Verify item is no longer displayed in Open Positions tab")
    android.trade_screen.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, trade_object.order_id, is_display=False)

    logger.info(f"Step 5: Select tab {AssetTabs.HISTORY.value.capitalize()}")
    android.trade_screen.asset_tab.select_tab(AssetTabs.HISTORY)

    logger.info("Verify history order item details")
    android.trade_screen.asset_tab.verify_item_data(trade_object, AssetTabs.POSITIONS_HISTORY)


@pytest.fixture(autouse=True)
def cleanup_test(android, cancel_all):

    yield
    logger.info("[Cleanup] Navigate back to Trade Screen")
    android.home_screen.navigate_to(Features.TRADE)

    logger.info("[Cleanup] Select Open Positions tab")
    android.trade_screen.asset_tab.select_tab(AssetTabs.OPEN_POSITION)