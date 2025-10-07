import pytest

from src.data.enums import AssetTabs, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, market_obj, cancel_close_order, order_data):
    trade_object = market_obj()
    tab_amount = web.assets_page.asset_tab.get_tab_amount(AssetTabs.OPEN_POSITION)

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)}")
    order_data(trade_object, SLTPType.PRICE, SLTPType.PRICE)

    logger.info(f"Verify tab amount increased to {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info(f"Step 2: Partial close position")
    new_object = web.trade_page.asset_tab.partial_close_position(trade_object)

    logger.info("Verify Close order notification banner")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).close_order_success_banner())

    logger.info("Verify Close Position noti in notification box")
    web.home_page.notifications.verify_notification_result(ObjNoti(trade_object).position_closed_details())

    logger.info(f"Verify asset tab amount remains unchanged for partial closed: {tab_amount + 1!r}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info("Verify Open Position details in asset tab")
    web.trade_page.asset_tab.verify_item_data(new_object)

    logger.info(f"Step 3: Select tab {AssetTabs.HISTORY.value.capitalize()}")
    web.trade_page.asset_tab.select_tab(AssetTabs.HISTORY)

    logger.info("Verify history order item details")
    web.trade_page.asset_tab.verify_item_data(trade_object, AssetTabs.HISTORY)


@pytest.fixture(autouse=True)
def teardown(web):
    yield
    logger.info("[Cleanup] Select Open Positions tab", teardown=True)
    web.trade_page.asset_tab.select_tab(AssetTabs.OPEN_POSITION)
