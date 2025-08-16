from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, OrderType, Features
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


def test(web, symbol, cancel_close_order):
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    APIClient().trade.post_order(trade_object, update_price=True)

    logger.info("Step 2: Navigate to Assets Page")
    web.home_page.navigate_to(Features.ASSETS)

    logger.info("Verify order placed successfully")
    web.assets_page.asset_tab.verify_item_displayed(tab=AssetTabs.OPEN_POSITION, order_id=trade_object.order_id)

    logger.info("Step 3: Full close position")
    web.assets_page.asset_tab.full_close_position(order_id=trade_object.order_id, trade_object=trade_object, confirm=False)

    logger.info("Verify Close order notification banner")
    exp_noti = ObjNoti(trade_object)
    web.home_page.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    logger.info("Verify Close Position noti in notification box")
    web.home_page.notifications.verify_notification_result(exp_noti.position_closed_details(), check_contains=True)

    logger.info(f"Verify item is no longer displayed in Open Positions tab")
    web.assets_page.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, trade_object.order_id, is_display=False)

    logger.info(f"Step 4: Select Tab {AssetTabs.HISTORY.value!r}")
    web.assets_page.asset_tab.select_tab(AssetTabs.HISTORY)

    logger.info("Verify history order item details")
    web.assets_page.asset_tab.verify_item_data(trade_object, AssetTabs.HISTORY, wait=True)
