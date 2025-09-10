import pytest

from src.data.enums import TradeType, AssetTabs, OrderType, SLTPType, Features
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize(
    "trade_type", [
        TradeType.BUY,
        TradeType.SELL,
    ]
)
def test(android, symbol, get_asset_tab_amount, trade_type, create_order_data):
    # -------------------
    trade_object = ObjTrade(trade_type, OrderType.MARKET, symbol=symbol)
    tab_amount = get_asset_tab_amount(AssetTabs.OPEN_POSITION)
    # -------------------
    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    create_order_data(trade_object)

    logger.info("Step 3: Close Position")
    android.trade_screen.asset_tab.full_close_position(trade_object.order_id, confirm=False)

    logger.info("Verify Close Order notification banner")
    exp_noti = ObjNoti(trade_object)
    android.home_screen.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    logger.info("Verify Position Closed noti in notification box")
    android.trade_screen.navigate_to(Features.HOME)
    android.home_screen.notifications.verify_notification_result(exp_noti.position_closed_details())

    logger.info(f"Verify item is no longer displayed in Open Positions tab")
    android.home_screen.navigate_to(Features.TRADE)
    android.trade_screen.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, trade_object.order_id, is_display=False)

    logger.info(f"Verify asset tab amount = {tab_amount}")
    android.trade_screen.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount)

    logger.info(f"Step 7: Select tab {AssetTabs.POSITIONS_HISTORY.value.capitalize()}")
    android.trade_screen.asset_tab.select_tab(AssetTabs.POSITIONS_HISTORY)
    
    logger.info("Verify history order item details")
    android.trade_screen.asset_tab.verify_item_data(trade_object, AssetTabs.POSITIONS_HISTORY)
