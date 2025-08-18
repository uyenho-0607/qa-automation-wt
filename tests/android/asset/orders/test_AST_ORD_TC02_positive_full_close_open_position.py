from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, OrderType, Features
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


def test(android, symbol, get_asset_tab_amount, cancel_close_order):
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)

    logger.info("Step 1: Navigate to Assets Page")
    android.home_screen.navigate_to(Features.ASSETS)

    logger.info("Step 2: Click on View all Transaction tab")
    android.assets_screen.click_view_all_transaction()

    logger.info(f"Step 3: Place {trade_object.trade_type} Order")
    APIClient().trade.post_order(trade_object, update_price=True)

    logger.info(f"Verify order placed successfully, order_id = {trade_object.order_id!r}")
    android.trade_screen.asset_tab.verify_item_displayed(tab=AssetTabs.OPEN_POSITION, order_id=trade_object.order_id)

    logger.info("Step 4: Full close position")
    android.trade_screen.asset_tab.full_close_position(order_id=trade_object.order_id, confirm=True)

    logger.info("Verify Close order notification banner")
    exp_noti = ObjNoti(trade_object)
    android.home_screen.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    logger.info(f"Verify item is no longer displayed in Open Positions tab")
    android.trade_screen.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, trade_object.order_id, is_display=False)

    logger.info(f"Step 5: Select Tab {AssetTabs.HISTORY.value!r}")
    android.trade_screen.asset_tab.select_tab(AssetTabs.HISTORY)

    logger.info("Verify history order item details")
    android.trade_screen.asset_tab.verify_item_data(trade_object, AssetTabs.POSITIONS_HISTORY)

    logger.info("Step 6: Navigate to Home screen")
    android.home_screen.go_back()
    android.trade_screen.navigate_to(Features.HOME)

    logger.info("Verify Close Position noti in notification box")
    android.home_screen.notifications.verify_notification_result(exp_noti.position_closed_details())

