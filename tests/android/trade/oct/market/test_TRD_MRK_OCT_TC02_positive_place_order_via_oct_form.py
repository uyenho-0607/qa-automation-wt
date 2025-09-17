import pytest

from src.data.enums import AssetTabs, OrderType, Features
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.common_utils import log_page_source
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(android, symbol, get_asset_tab_amount):
    # -------------------
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)
    tab = AssetTabs.OPEN_POSITION

    logger.info("Step 1: Get tab amount")
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 2: Place {trade_object.trade_type} Order (tab:{tab_amount})")
    android.trade_screen.place_order_panel.place_oct_order(trade_object)

    logger.info("Verify Order Submitted Notification banner")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).order_submitted_banner())

    logger.info(f"Verify Asset Tab amount {tab.title()} is: {tab_amount + 1}")
    android.trade_screen.asset_tab.verify_tab_amount(tab, tab_amount + 1)

    logger.info(f"Verify {tab.title()} item details in Asset Tab")
    android.trade_screen.asset_tab.verify_item_data(trade_object)

    logger.info("Step 3: Navigate to Home screen")
    log_page_source("home")
    android.home_screen.navigate_to(Features.HOME)

    logger.info("Verify Open Position noti in Notification Box")
    android.home_screen.notifications.verify_notification_result(ObjNoti(trade_object).open_position_details(trade_object.order_id), close=True)


@pytest.fixture(autouse=True)
def navigate_to_trade_screen(android):
    yield
    logger.info("[Cleanup] Navigate back to Trade screen")
    android.home_screen.navigate_to(Features.TRADE)
