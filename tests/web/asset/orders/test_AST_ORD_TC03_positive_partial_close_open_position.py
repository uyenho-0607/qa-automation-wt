import pytest

from src.data.enums import AssetTabs, OrderType, SLTPType, Features
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


def test(web, symbol, search_symbol):
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    web.trade_page.place_order_panel.place_order(trade_object, submit=True)

    logger.info("Step 2: Close Noti banner")
    web.home_page.notifications.close_noti_banner()

    logger.info("Step 3: Get item order_id from notification")
    web.home_page.notifications.get_open_position_order_id(trade_object)

    # Object for new created open position
    new_object = ObjTrade(**{k: v for k, v in trade_object.items() if k != "order_id"})

    logger.info("Step 4: Navigate to Asset Page")
    web.home_page.navigate_to(Features.ASSETS)

    logger.info("Step 5: Partial Close Position")
    web.assets_page.asset_tab.partial_close_position(trade_object.order_id, trade_object=new_object)

    # update new volume, units after partial close
    trade_object.volume, trade_object.units = new_object.close_volume, new_object.close_units

    logger.info("Verify Close order notification banner")
    exp_noti = ObjNoti(trade_object)
    web.home_page.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    logger.info("Verify Close Position noti in notification box")
    web.home_page.notifications.verify_notification_result(exp_noti.position_closed_details())

    logger.info("Verify Open Position details in asset tab")
    web.trade_page.asset_tab.verify_item_data(new_object)

    logger.info("Verify history order item details")
    web.trade_page.asset_tab.verify_item_data(trade_object, AssetTabs.HISTORY)
