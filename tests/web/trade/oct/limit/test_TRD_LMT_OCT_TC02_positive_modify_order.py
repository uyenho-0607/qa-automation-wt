import pytest

from src.data.enums import SLTPType, OrderType, Expiry, AssetTabs
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize("edit_field, sl_type, tp_type", [("SL, TP", SLTPType.PRICE, SLTPType.PRICE)])
def test(web, edit_field, sl_type, tp_type, close_edit_confirm_modal, order_data, limit_obj):
    trade_object = limit_obj()

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)}")
    order_data(trade_object, SLTPType.PRICE, SLTPType.PRICE, confirm=False)
    trade_object.order_id = web.trade_page.asset_tab.get_last_order_id(AssetTabs.PENDING_ORDER)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    web.trade_page.asset_tab.verify_item_data(trade_object, AssetTabs.PENDING_ORDER, False)

    logger.info(f"Step 2: Update placed order with {edit_field!r}")
    web.trade_page.asset_tab.modify_order(trade_object, sl_type=sl_type, tp_type=tp_type, expiry=Expiry.sample_values(OrderType.LIMIT), oct_mode=True)

    logger.info("Verify notification banner updated message")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner())

    logger.info(f"Verify item details after update")
    web.trade_page.asset_tab.verify_item_data(trade_object, wait=True)
