import pytest

from src.data.enums import AssetTabs
from src.data.objects.notification_obj import ObjNoti
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, stop_limit_obj, cancel_delete_order, create_order_data):
    trade_object = stop_limit_obj()
    tab = AssetTabs.PENDING_ORDER

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    *_, tab_amount = create_order_data(trade_object, update_price=False)

    logger.info(f"Verify order placed successfully - order_id: {trade_object.order_id!r}, tab:{tab_amount + 1}")
    web.trade_page.asset_tab.verify_item_displayed(tab, trade_object.order_id)

    logger.info(f"Step 2: Delete pending order")
    web.trade_page.asset_tab.delete_order(trade_object, confirm=False)

    logger.info("Verify Delete order notification banner")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).delete_order_banner())

    logger.info(f"Verify {tab.title()} amount decreased to: {tab_amount}")
    web.trade_page.asset_tab.verify_tab_amount(tab, tab_amount)

    logger.info("Verify item is no longer displayed")
    web.trade_page.asset_tab.verify_item_displayed(tab, trade_object.order_id, is_display=False)
