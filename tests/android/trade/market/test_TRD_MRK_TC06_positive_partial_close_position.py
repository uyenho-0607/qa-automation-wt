import pytest

from src.data.enums import AssetTabs, OrderType, Features
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(android, symbol, get_asset_tab_amount, create_order_data):
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)

    logger.info("Step 1: Get asset tab amount")
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 2: Place {trade_object.trade_type} Order")
    create_order_data(trade_object)

    logger.info(f"Step 3: Select tab {AssetTabs.POSITIONS_HISTORY.value!r}")
    android.trade_screen.asset_tab.select_tab(AssetTabs.POSITIONS_HISTORY)

    logger.info(f"Verify order placed successfully, order_id = {trade_object.order_id!r}")
    android.trade_screen.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, trade_object.order_id)

    # Object for new created open position
    new_object = ObjTrade(**{k: v for k, v in trade_object.items() if k != "order_id"})

    logger.info("Step 4: Select Open Position tab")
    android.trade_screen.asset_tab.select_tab(AssetTabs.OPEN_POSITION)

    logger.info("Step 5: Partial close position")
    android.trade_screen.asset_tab.partial_close_position(new_object, trade_object.order_id, confirm=True)

    # update new volume, units after partial close
    trade_object.volume, trade_object.units = new_object.close_volume, new_object.close_units

    logger.info(f"Verify close order notification banner")
    exp_noti = ObjNoti(trade_object)
    android.home_screen.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    logger.info(f"Verify asset tab amount = {tab_amount + 1}")
    android.trade_screen.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info(f"Verify Open Position details in asset tab")
    android.trade_screen.asset_tab.verify_item_data(new_object)

    logger.info(f"Step 6: Select tab {AssetTabs.POSITIONS_HISTORY.value.capitalize()}")
    android.trade_screen.asset_tab.select_tab(AssetTabs.POSITIONS_HISTORY)

    logger.info(f"Verify history order item details")
    android.trade_screen.asset_tab.verify_item_data(trade_object, AssetTabs.POSITIONS_HISTORY)

    logger.info("Step 7: Navigate to Home screen")
    android.trade_screen.navigate_to(Features.HOME)

    logger.info(f"Verify position closed noti in notification box")
    android.home_screen.notifications.verify_notification_result(exp_noti.position_closed_details())


@pytest.fixture(autouse=True)
def teardown(android, cancel_close_order):
    yield
    logger.info("- Navigate to Trade screen")
    android.home_screen.navigate_to(Features.TRADE)