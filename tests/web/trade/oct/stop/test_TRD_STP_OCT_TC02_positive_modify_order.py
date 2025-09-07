import pytest

from src.data.enums import SLTPType, OrderType, Expiry, AssetTabs
from src.data.objects.notification_obj import ObjNoti
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize(
    "edit_field, sl_type, tp_type",
    [
        ("SL, TP", SLTPType.PRICE, SLTPType.PRICE),
        ("SL, TP", SLTPType.POINTS, SLTPType.POINTS),
    ]
)
def test(web, edit_field, sl_type, tp_type, close_edit_confirm_modal, create_order_data, stop_obj):
    trade_object = stop_obj(stop_loss=0, take_profit=0)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order without SL and TP")
    create_order_data(trade_object, update_price=False)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    web.trade_page.asset_tab.verify_item_displayed(AssetTabs.PENDING_ORDER, trade_object.order_id)

    logger.info(f"Step 2: Modify order with {edit_field!r}")
    web.trade_page.asset_tab.modify_order(trade_object, sl_type=sl_type, tp_type=tp_type, expiry=Expiry.sample_values(OrderType.LIMIT), oct_mode=True)

    logger.info("Verify notification banner updated message")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner())

    logger.info(f"Verify item details after update")
    web.trade_page.asset_tab.verify_item_data(trade_object, wait=True)
