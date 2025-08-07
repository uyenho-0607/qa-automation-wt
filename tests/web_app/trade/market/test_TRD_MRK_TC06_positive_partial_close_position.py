import pytest

from src.data.enums import AssetTabs, OrderType, Features
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.order(1)
@pytest.mark.critical
def test(web_app, symbol, get_asset_tab_amount, create_order_data):
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    *_, tab_amount = create_order_data(trade_object)

    logger.info(f"Verify order placed successfully, order_id = {trade_object.order_id!r}")
    web_app.trade_page.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, trade_object.order_id)

    logger.info("Step 2: Partial close position")
    new_object = web_app.trade_page.asset_tab.partial_close_position(trade_object)

    logger.info(f"Verify close order notification banner")
    exp_noti = ObjNoti(trade_object)
    web_app.home_page.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    logger.info(f"Verify asset tab amount = {tab_amount}")
    web_app.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount)

    logger.info(f"Verify Open Position details in asset tab")
    web_app.trade_page.asset_tab.verify_item_data(new_object)

    logger.info(f"Step 3: Select tab {AssetTabs.HISTORY.value.capitalize()}")
    web_app.trade_page.asset_tab.select_tab(AssetTabs.HISTORY)

    logger.info(f"Verify history order item details")
    web_app.trade_page.asset_tab.verify_item_data(trade_object, AssetTabs.POSITIONS_HISTORY)

    logger.info("Step 4: Navigate to Home screen")
    web_app.trade_page.navigate_to(Features.HOME)

    logger.info(f"Verify position closed noti in notification box")
    web_app.home_page.notifications.verify_notification_result(exp_noti.position_closed_details(), close=True)


@pytest.fixture(autouse=True)
def teardown(web_app, cancel_all):
    yield
    logger.info("- Navigate to Trade screen")
    web_app.home_page.navigate_to(Features.TRADE)

    logger.info("- Select Open Positions tab")
    web_app.trade_page.asset_tab.select_tab(AssetTabs.OPEN_POSITION)
