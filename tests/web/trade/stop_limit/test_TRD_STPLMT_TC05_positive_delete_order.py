import pytest

from src.data.enums import AssetTabs, OrderType, SLTPType
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade

from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, symbol, get_asset_tab_amount, cancel_delete_order, create_order_data):
    trade_object = ObjectTrade(order_type=OrderType.STOP_LIMIT, symbol=symbol, indicate=SLTPType.sample_values())
    tab = AssetTabs.PENDING_ORDER
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    create_order_data(trade_object)

    logger.info("Step 2: Delete pending order")
    web.trade_page.asset_tab.delete_pending_order(order_id=trade_object.order_id)

    logger.info("Verify Delete order notification banner")
    web.home_page.notifications.verify_notification_banner(*ObjectNoti(trade_object).delete_order_banner())

    logger.info(f"Verify {tab.title()} amount = {tab_amount}")
    web.trade_page.asset_tab.verify_tab_amount(tab, tab_amount)

    logger.info("Verify item is no longer displayed")
    web.trade_page.asset_tab.verify_item_displayed(tab, trade_object.order_id, is_display=False)
