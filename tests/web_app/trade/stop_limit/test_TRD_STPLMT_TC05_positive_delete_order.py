import pytest

from src.data.enums import AssetTabs
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web_app, stop_limit_obj, order_data, cancel_all):
    trade_object = stop_limit_obj()

    tab_amount = web_app.trade_page.asset_tab.get_tab_amount(AssetTabs.PENDING_ORDER)

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)} (tab:{tab_amount})")
    order_data(trade_object)
    web_app.home_page.notifications.close_noti_banner()

    logger.info("Step 2: Select Pending Orders tab")
    web_app.trade_page.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info(f"Verify order placed successfully, tab amount: {tab_amount + 1}")
    web_app.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount + 1)

    logger.info("Step 3: Delete pending order")
    web_app.trade_page.asset_tab.delete_order(trade_object)

    logger.info(f"Verify delete order notification banner")
    web_app.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).delete_order_banner())

    logger.info(f"Verify asset tab amount: {tab_amount}")
    web_app.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount)

    logger.info(f"Verify item is no longer displayed")
    web_app.trade_page.asset_tab.verify_item_displayed(AssetTabs.PENDING_ORDER, trade_object.order_id, is_display=False)
