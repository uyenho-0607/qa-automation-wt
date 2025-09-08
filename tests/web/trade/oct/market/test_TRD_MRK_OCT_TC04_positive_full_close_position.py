from contextlib import suppress

import pytest

from src.data.enums import AssetTabs
from src.data.objects.notification_obj import ObjNoti
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, market_obj):
    trade_obj = market_obj()

    logger.info("Step 1: Get tab amount")
    tab_amount = web.trade_page.asset_tab.get_tab_amount(AssetTabs.OPEN_POSITION)

    logger.info(f"Step 2: Place {trade_obj.trade_type.upper()} Market Order via OCT tab (tab:{tab_amount})")
    web.trade_page.place_order_panel.place_oct_order(trade_obj)

    logger.info(f"Verify tab amount increased to: {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info("Step 3: Full Close Position")
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

    logger.info("Step 4: Select History Tab")
    web.trade_page.asset_tab.select_tab(AssetTabs.HISTORY)

    logger.info("Verify item details in History Tab")
    web.trade_page.asset_tab.verify_item_data(trade_obj, AssetTabs.HISTORY)


@pytest.fixture(autouse=True)
def cleanup_test(web):
    yield

    with suppress(Exception):
        web.assets_page.asset_tab.select_tab(AssetTabs.OPEN_POSITION)