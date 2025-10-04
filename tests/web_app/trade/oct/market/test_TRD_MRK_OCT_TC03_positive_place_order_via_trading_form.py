import random

import pytest

from src.data.enums import AssetTabs, OrderType, Features, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize("sl_type, tp_type", [(SLTPType.PRICE, SLTPType.PRICE)])
def test(web_app, market_obj, get_asset_tab_amount, sl_type, tp_type):
    trade_object = market_obj()
    tab = AssetTabs.OPEN_POSITION

    logger.info("Step 1: Get tab amount")
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info("Step 2: Open pre-trade details form")
    web_app.trade_page.place_order_panel.open_pre_trade_details()

    logger.info(f"Step 3: Place order with {format_display_dict(trade_object)} (sl_type:{sl_type!r}, tp_type:{tp_type!r}, tab:{tab_amount})")
    web_app.trade_page.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=sl_type, confirm=False)

    logger.info("Verify notification banner displays correct input trade information")
    web_app.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_submitted_banner())

    logger.info(f"Verify Asset Tab amount {tab.title()} is: {tab_amount + 1}")
    web_app.trade_page.asset_tab.verify_tab_amount(tab, tab_amount + 1)

    logger.info(f"Verify {tab.title()} item details in Asset Tab")
    web_app.trade_page.asset_tab.verify_item_data(trade_object, wait=True)

    logger.info("Step 4: Navigate to Home screen")
    web_app.home_page.navigate_to(Features.HOME)

    logger.info("Verify Open Position noti in Notification Box")
    web_app.home_page.notifications.verify_notification_result(ObjNoti(trade_object).open_position_details(trade_object.order_id))


@pytest.fixture(autouse=True)
def teardown(web_app):
    yield
    logger.info("[Cleanup] Navigate back to Trade screen", teardown=True)
    web_app.home_page.navigate_to(Features.TRADE)
