import random

import pytest

from src.data.enums import AssetTabs, Features
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web_app, market_obj, get_asset_tab_amount, order_data):
    trade_object = market_obj(volume=random.randint(5, 10))

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)}")
    order_data(trade_object)
    web_app.home_page.notifications.close_noti_banner()
    trade_object.order_id = web_app.trade_page.asset_tab.get_last_order_id(AssetTabs.OPEN_POSITION)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    web_app.trade_page.asset_tab.verify_item_data(trade_object, AssetTabs.OPEN_POSITION, wait=False)

    logger.info("Step 2: Get asset tab amount")
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info("Step 3: Partial close position")
    new_object = web_app.trade_page.asset_tab.partial_close_position(trade_object)

    logger.info(f"Verify close order notification banner")
    web_app.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).close_order_success_banner())

    logger.info(f"Verify asset tab amount = {tab_amount}")
    web_app.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount)

    logger.info(f"Verify Open Position details in asset tab")
    web_app.trade_page.asset_tab.verify_item_data(new_object)

    logger.info(f"Step 4: Select tab {AssetTabs.HISTORY.value.capitalize()}")
    web_app.trade_page.asset_tab.select_tab(AssetTabs.HISTORY)

    logger.info(f"Verify history order item details")
    web_app.trade_page.asset_tab.verify_item_data(trade_object, AssetTabs.POSITIONS_HISTORY)

    logger.info("Step 5: Navigate to Home screen")
    web_app.trade_page.navigate_to(Features.HOME)

    logger.info(f"Verify position closed noti in notification box")
    web_app.home_page.notifications.verify_notification_result(ObjNoti(trade_object).position_closed_details())


@pytest.fixture(autouse=True)
def teardown(web_app, cancel_all):
    yield
    logger.info("- Navigate to Trade screen", teardown=True)
    web_app.home_page.navigate_to(Features.TRADE)

    logger.info("- Select Open Positions tab", teardown=True)
    web_app.trade_page.asset_tab.select_tab(AssetTabs.OPEN_POSITION)
