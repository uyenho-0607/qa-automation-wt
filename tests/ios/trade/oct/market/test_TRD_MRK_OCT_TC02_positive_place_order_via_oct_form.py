import pytest

from src.data.enums import AssetTabs, OrderType, Features
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(ios, symbol, get_asset_tab_amount):
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)
    tab = AssetTabs.OPEN_POSITION

    logger.info("Step 1: Get tab amount")
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 2: Place order with: {format_display_dict(trade_object)} via OCT form (tab:{tab_amount})")
    ios.trade_screen.place_order_panel.place_oct_order(trade_object)

    logger.info("Verify Order Submitted Notification banner")
    ios.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).order_submitted_banner())

    logger.info(f"Verify Asset Tab amount {tab.title()} is: {tab_amount + 1}")
    ios.trade_screen.asset_tab.verify_tab_amount(tab, tab_amount + 1)

    logger.info(f"Verify {tab.title()} item details in Asset Tab")
    ios.trade_screen.asset_tab.verify_item_data(trade_object)

    logger.info("Step 3: Navigate to Home screen")
    ios.home_screen.navigate_to(Features.HOME)

    logger.info("Verify Open Position noti in Notification Box")
    ios.home_screen.notifications.verify_notification_result(ObjNoti(trade_object).open_position_details(trade_object.order_id), close=True)


@pytest.fixture(autouse=True)
def teardown(ios):
    yield
    logger.info("[Cleanup] Navigate back to Trade screen", teardown=True)
    ios.home_screen.navigate_to(Features.TRADE)