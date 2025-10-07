from contextlib import suppress

import pytest

from src.data.enums import AssetTabs
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, market_obj, get_asset_tab_amount):
    trade_obj = market_obj()
    tab_amount = get_asset_tab_amount(trade_obj.order_type)

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_obj)} via OCT tab")
    web.trade_page.place_order_panel.place_oct_order(trade_obj)

    logger.info(f"Verify tab amount increased to {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info("Step 2: Full Close Position")
    web.trade_page.asset_tab.full_close_position(trade_object=trade_obj, confirm=False)

    logger.info("Verify Close order notification banner")
    exp_noti = ObjNoti(trade_obj)
    web.home_page.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    logger.info("Verify notification details in notification box")
    web.home_page.notifications.verify_notification_result(exp_noti.position_closed_details())

    logger.info("Verify item is no longer displayed in Open Positions tab")
    web.trade_page.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, trade_obj.order_id, is_display=False)

    logger.info(f"Verify asset tab amount decreased to: {tab_amount}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount)

    logger.info(f"Step 3: Select tab {AssetTabs.HISTORY.value.capitalize()}")
    web.trade_page.asset_tab.select_tab(AssetTabs.HISTORY)

    logger.info("Verify history order item details")
    web.trade_page.asset_tab.verify_item_data(trade_obj, AssetTabs.HISTORY)


@pytest.fixture(autouse=True)
def cleanup_test(web):
    yield
    logger.info("[Cleanup] Select Open Positions tab", teardown=True)
    with suppress(Exception):
        web.assets_page.asset_tab.select_tab(AssetTabs.OPEN_POSITION)