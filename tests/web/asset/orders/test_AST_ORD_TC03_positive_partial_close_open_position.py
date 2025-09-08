from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, OrderType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


def test(web, symbol, search_symbol):
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    APIClient().trade.post_order(trade_object, update_price=True)

    logger.info("Step 2: Partial Close Position")
    new_object = web.assets_page.asset_tab.partial_close_position(trade_object)

    logger.info("Verify Close order notification banner")
    exp_noti = ObjNoti(trade_object)
    web.home_page.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    logger.info("Verify Close Position noti in notification box")
    web.home_page.notifications.verify_notification_result(exp_noti.position_closed_details())

    logger.info(f"Step 3: Select tab: {AssetTabs.OPEN_POSITION}")
    web.assets_page.asset_tab.select_tab(AssetTabs.OPEN_POSITION)

    logger.info("Verify Open Position details in asset tab")
    web.trade_page.asset_tab.verify_item_data(new_object)

    logger.info(f"Step 4: Select tab: {AssetTabs.HISTORY}")
    web.assets_page.asset_tab.select_tab(AssetTabs.HISTORY)

    logger.info("Verify history order item details")
    web.trade_page.asset_tab.verify_item_data(trade_object, AssetTabs.HISTORY)
