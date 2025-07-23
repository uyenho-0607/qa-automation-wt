import pytest

from src.data.enums import OrderType, SLTPType, AssetTabs
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize(
    "exclude_field, update_field",
    [
        ("SL", "SL"),
        pytest.param("SL", "TP", marks=pytest.mark.critical),
        ("SL", "SL,TP"),
        pytest.param("TP", "SL", marks=pytest.mark.critical),
        ("TP", "TP"),
        ("TP", "SL,TP"),
    ]
)
def test(web, symbol, create_order_data, exclude_field, update_field, close_edit_confirm_modal):
    trade_object = ObjTrade(order_type=OrderType.STOP, symbol=symbol)
    trade_object[exclude_field] = 0
    update_info = {f"{item.lower()}_type": SLTPType.random_values() for item in update_field.split(",")}

    logger.info(f"Step 1: Place {trade_object.trade_type} Order with SL/ TP ({exclude_field} = 0)")
    create_order_data(trade_object)

    logger.info("Verify order placed successfully")
    web.trade_page.asset_tab.verify_item_displayed(AssetTabs.PENDING_ORDER, trade_object.order_id)

    logger.info(f"Step 2: Modify order with {update_field!r} {' - '.join(list(update_info.values()))}")
    web.trade_page.modals.modify_order(trade_object, **update_info)

    logger.info("Verify edit confirmation info")
    web.trade_page.modals.verify_edit_trade_confirmation(trade_object)

    logger.info("Step 3: Confirm update order")
    web.trade_page.modals.confirm_update_order()

    logger.info("Verify notification banner updated message")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner())

    logger.info(f"Verify order details after update")
    web.trade_page.asset_tab.verify_item_data(trade_object)
