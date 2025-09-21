import pytest

from src.data.enums import SLTPType, Expiry, AssetTabs
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize(
    "sl_type, tp_type",
    [
        (SLTPType.POINTS, SLTPType.POINTS),
        (SLTPType.PRICE, SLTPType.PRICE),
        SLTPType.sample_values(amount=2),
    ]
)
def test(web, order_data, sl_type, tp_type, close_edit_confirm_modal, stop_limit_obj):
    trade_object = stop_limit_obj()

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)} with SL and TP")
    order_data(trade_object, SLTPType.PRICE, SLTPType.PRICE)
    trade_object.order_id = web.trade_page.asset_tab.get_last_order_id(AssetTabs.PENDING_ORDER)  # Get latest orderID

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    web.trade_page.asset_tab.verify_item_data(trade_object, AssetTabs.PENDING_ORDER, False)

    logger.info(f"Step 2: Update placed order with SL ({sl_type.capitalize()}), TP ({tp_type.capitalize()})")
    web.trade_page.asset_tab.modify_order(trade_object, sl_type=sl_type, tp_type=tp_type, expiry=Expiry.sample_values(trade_object.order_type))

    logger.info("Verify trade edit confirmation")
    web.trade_page.modals.verify_edit_trade_confirmation(trade_object)

    logger.info("Step 3: Confirm update order")
    web.trade_page.modals.confirm_update_order()

    logger.info("Verify notification banner updated message")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner())

    logger.info(f"Verify item details after update")
    web.trade_page.asset_tab.verify_item_data(trade_object, wait=True)
