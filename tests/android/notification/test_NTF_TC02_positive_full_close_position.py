import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, OrderType, Features, NotificationTab
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


def test(android, symbol, get_asset_tab_amount, get_notification_tab_amount):
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    APIClient().trade.post_order(trade_object, update_price=True)

    logger.info("Step 2: Get Notification tab amount")
    noti_tab_amount = get_notification_tab_amount()

    logger.info("Step 3: Select Open Position tab")
    android.trade_screen.asset_tab.select_tab(AssetTabs.OPEN_POSITION)

    logger.info(f"Verify order placed successfully, order_id = {trade_object.order_id!r}")
    android.trade_screen.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, trade_object.order_id)

    logger.info("Step 4: Full close position")
    android.trade_screen.asset_tab.full_close_position(trade_object.order_id)

    logger.info(f"Verify close order notification banner")
    exp_noti = ObjNoti(trade_object)
    android.home_screen.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    logger.info("Step 5: Navigate to Home screen")
    android.trade_screen.navigate_to(Features.HOME)

    logger.info(f"Verify notification tab amount increased to {noti_tab_amount + 1}")
    android.home_screen.notifications.verify_tab_amount(NotificationTab.ORDER, noti_tab_amount + 1)

    logger.info(f"Verify Position Closed noti in notification box")
    android.home_screen.notifications.verify_notification_result(exp_noti.position_closed_details())