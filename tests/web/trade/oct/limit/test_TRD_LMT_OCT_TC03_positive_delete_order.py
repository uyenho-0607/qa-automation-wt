import pytest

from src.data.enums import AssetTabs, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, limit_obj, cancel_delete_order, order_data, get_asset_tab_amount):
    trade_object = limit_obj()
    tab = AssetTabs.PENDING_ORDER
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)}")
    order_data(trade_object, SLTPType.PRICE, SLTPType.PRICE, confirm=False)
    trade_object.order_id = web.trade_page.asset_tab.get_last_order_id(AssetTabs.PENDING_ORDER)

    logger.info(f"Verify tab amount increased to {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(tab, tab_amount + 1)

    logger.info(f"Step 2: Delete pending order")
    web.trade_page.asset_tab.delete_order(trade_object, confirm=False)

    logger.info("Verify Delete order notification banner")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).delete_order_banner())

    logger.info(f"Verify tab amount decreased to {tab_amount}")
    web.trade_page.asset_tab.verify_tab_amount(tab, tab_amount)

    logger.info("Verify item is no longer displayed")
    web.trade_page.asset_tab.verify_item_displayed(tab, trade_object.order_id, is_display=False)
