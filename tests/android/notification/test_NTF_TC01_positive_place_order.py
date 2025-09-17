import pytest

from src.data.enums import AssetTabs, OrderType, Features, SLTPType, NotificationTab
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


def test(android, symbol, get_asset_tab_amount, get_notification_tab_amount):
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)
    noti_tab_amount = get_notification_tab_amount()
    # -------------------

    logger.info(f"Step 1: Place {trade_object.trade_type} order for {symbol!r}")
    android.trade_screen.place_order_panel.place_order(trade_object, confirm=True)

    logger.info(f"Step 2: Get placed order_id = {trade_object.order_id!r}")
    android.trade_screen.asset_tab.get_last_order_id(trade_object)

    logger.info("Step 3: Navigate to Home Screen")
    android.home_screen.navigate_to(Features.HOME)

    logger.info(f"Verify notification tab amount increased to {noti_tab_amount + 1}")
    android.home_screen.notifications.verify_tab_amount(NotificationTab.ORDER, noti_tab_amount + 1)

    logger.info("Verify Open Position noti in Notification Box")
    android.home_screen.notifications.verify_notification_result(
        ObjNoti(trade_object).open_position_details(trade_object.order_id), go_back=False)