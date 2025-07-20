import pytest

from src.data.enums import AssetTabs, OrderType, SLTPType, Features
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


def test(web, symbol, search_symbol, cancel_close_order):
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    web.trade_page.place_order_panel.place_order(trade_object)
    web.home_page.notifications.close_noti_banner()

    logger.info("Step 2: Get item order_id from notification")
    web.home_page.notifications.get_open_position_order_id(trade_object)

    logger.info("Step 3: Navigate to Asset Page and close Position")
    web.home_page.navigate_to(Features.ASSETS)

    logger.info("Step 4: Full close position")
    web.assets_page.asset_tab.full_close_position(order_id=trade_object.order_id, confirm=False)

    logger.info("Verify Close order notification banner")
    exp_noti = ObjNoti(trade_object)
    web.home_page.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    logger.info("Verify Close Position noti in notification box")
    web.home_page.notifications.verify_notification_result(exp_noti.position_closed_details(), check_contains=True)

    logger.info(f"Verify item is no longer displayed in Open Positions tab")
    web.assets_page.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, trade_object.order_id, is_display=False)

    logger.info("Verify history order item details")
    web.assets_page.asset_tab.verify_item_data(trade_object, AssetTabs.HISTORY)
