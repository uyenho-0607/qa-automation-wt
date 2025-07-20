import pytest

from src.data.enums import OrderType, Features, AssetTabs
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


def test(web, symbol, search_symbol):
    trade_object = ObjectTrade(order_type=OrderType.MARKET, symbol=symbol)
    # -------------------

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    web.trade_page.place_order_panel.place_order(trade_object, submit=True)

    logger.info("Step 2: Close Noti banner")
    web.home_page.notifications.close_noti_banner()

    logger.info("Step 3: Get item order_id from notification")
    web.home_page.notifications.get_open_position_order_id(trade_object)

    logger.info("Step 4: Navigate to Asset Page")
    web.home_page.navigate_to(Features.ASSETS)

    logger.info("Step 5: Full Close Position")
    web.assets_page.asset_tab.full_close_position(trade_object.order_id)

    logger.info("Verify Close order notification banner")
    exp_noti = ObjectNoti(trade_object)
    web.home_page.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    logger.info("Verify Close Position noti in notification box")
    web.home_page.notifications.verify_notification_result(exp_noti.position_closed_details())

    logger.info(f"Verify item is no longer displayed in Open Positions tab")
    web.assets_page.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, trade_object.order_id, is_display=False)

    logger.info("Verify history order item details")
    web.assets_page.asset_tab.verify_item_data(trade_object, AssetTabs.HISTORY)


@pytest.fixture(autouse=True)
def teardown(web):
    yield
    web.home_page.navigate_to(Features.TRADE)