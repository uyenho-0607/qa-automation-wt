import pytest

from src.data.enums import AssetTabs, SLTPType, OrderType, Expiry
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize(
    "field, place_type, edit_type",
    [
        ("stop_loss", *SLTPType.random_values(amount=2)),
        ("take_profit", *SLTPType.random_values(amount=2)),
    ]
)
def test(web, symbol, create_order_data, field, place_type, edit_type, close_edit_confirm_modal):
    sl_tp_val = {("stop_loss" if field == "take_profit" else "take_profit"): 0, "indicate": place_type}
    update_sl_type, update_tp_type = (edit_type, None) if field == "stop_loss" else (None, edit_type)

    trade_object = ObjectTrade(order_type=OrderType.STOP_LIMIT, symbol=symbol, **sl_tp_val)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order with {field!r}")
    create_order_data(trade_object)

    logger.info(f"Step 2: Update pending order with {field!r} - type: {edit_type.capitalize()!r}")
    web.trade_page.modals.modify_order(trade_object, sl_type=update_sl_type, tp_type=update_tp_type, expiry=Expiry.sample_values(trade_object.order_type))

    logger.info("Verify edit confirmation info")
    web.trade_page.modals.verify_edit_trade_confirmation(trade_object)

    logger.info("Step 3: Confirm update order")
    web.trade_page.modals.confirm_update_order()

    logger.info("Verify notification banner updated message")
    web.home_page.notifications.verify_notification_banner(*ObjectNoti(trade_object).order_updated_banner())

    logger.info(f"Verify item details after update")
    web.trade_page.asset_tab.verify_item_data(trade_object)
