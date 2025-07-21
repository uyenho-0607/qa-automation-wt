import pytest

from src.data.enums import AssetTabs, OrderType, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


def test(web, symbol, get_asset_tab_amount, cancel_close_order, create_order_data, ):
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    create_order_data(trade_object)

    logger.info("Step 2: Close Position")
    web.trade_page.asset_tab.full_close_position(trade_object.order_id, confirm=False)

    logger.info("Verify Close order notification banner")
    exp_noti = ObjNoti(trade_object)
    web.home_page.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    logger.info("Verify notification details in notification box")
    web.home_page.notifications.verify_notification_result(exp_noti.position_closed_details())

    logger.info("Verify item is no longer displayed")
    web.trade_page.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, trade_object.order_id, is_display=False)

    logger.info(f"Verify asset tab amount = {tab_amount}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount)

    logger.info("Verify item details in History Tab")
    web.trade_page.asset_tab.verify_item_data(trade_object, AssetTabs.HISTORY)
