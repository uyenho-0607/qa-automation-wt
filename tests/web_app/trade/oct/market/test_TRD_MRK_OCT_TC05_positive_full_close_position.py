import pytest

from src.data.enums import AssetTabs, Features
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web_app, market_obj, order_data, get_asset_tab_amount):
    trade_object = market_obj()
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info("Step 1: Open pre-trade details form")
    web_app.trade_page.place_order_panel.open_pre_trade_details()

    logger.info(f"Step 2: Place order with: {format_display_dict(trade_object)}")
    order_data(trade_object, confirm=False)
    trade_object.order_id = web_app.trade_page.asset_tab.get_last_order_id(AssetTabs.OPEN_POSITION, wait=True)

    logger.info(f"Verify order placed successfully, order_id = {trade_object.order_id!r}")
    web_app.trade_page.asset_tab.verify_item_data(trade_object, AssetTabs.OPEN_POSITION)

    logger.info("Step 3: Full close position")
    web_app.trade_page.asset_tab.full_close_position(trade_object, confirm=False)
    web_app.trade_page.asset_tab.get_current_price(trade_object, oct_mode=True)

    logger.info("Verify Close Order notification banner")
    web_app.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).close_order_success_banner())

    logger.info("Step 4: Navigate to Home Screen")
    web_app.trade_page.navigate_to(Features.HOME)

    logger.info("Verify Position Closed noti in notification box")
    web_app.home_page.notifications.verify_notification_result(ObjNoti(trade_object).position_closed_details())

    logger.info("Step 5: Navigate back to Trade Screen")
    web_app.home_page.navigate_to(Features.TRADE, wait=True)

    logger.info(f"Verify asset tab amount = {tab_amount}")
    web_app.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount)

    logger.info(f"Verify item is no longer displayed in Open Positions tab")
    web_app.trade_page.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, trade_object.order_id, is_display=False)

    logger.info(f"Step 6: Select tab {AssetTabs.HISTORY.value.capitalize()}")
    web_app.trade_page.asset_tab.select_tab(AssetTabs.HISTORY)

    logger.info("Verify history order item details")
    web_app.trade_page.asset_tab.verify_item_data(trade_object, AssetTabs.POSITIONS_HISTORY)


@pytest.fixture(autouse=True)
def cleanup_test(web_app, cancel_all):

    yield
    logger.info("[Cleanup] Navigate back to Trade Screen", teardown=True)
    web_app.home_page.navigate_to(Features.TRADE)

    logger.info("[Cleanup] Select Open Positions tab", teardown=True)
    web_app.trade_page.asset_tab.select_tab(AssetTabs.OPEN_POSITION)
