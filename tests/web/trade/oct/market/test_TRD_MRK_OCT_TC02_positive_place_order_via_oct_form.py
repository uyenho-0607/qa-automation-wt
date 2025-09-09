import pytest
from src.data.enums import AssetTabs
from src.data.objects.notification_obj import ObjNoti
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, market_obj, get_asset_tab_amount):
    trade_obj = market_obj()

    logger.info("Step 1: Get tab amount")
    tab_amount = get_asset_tab_amount(trade_obj.order_type)

    logger.info(f"Step 2: Place {trade_obj.trade_type.upper()} Market Order from OCT tab (tab:{tab_amount})")
    web.trade_page.place_order_panel.place_oct_order(trade_obj)

    logger.info("Verify Market Order Submitted notification banner")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_obj).order_submitted_banner())

    logger.info(f"Verify tab amount increased to: {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info(f"Verify order details in Asset Tab")
    web.trade_page.asset_tab.verify_item_data(trade_obj)

    logger.info(f"Verify Open Position noti in Notification Box")
    web.home_page.notifications.verify_notification_result(ObjNoti(trade_obj).open_position_details(trade_obj.order_id))
