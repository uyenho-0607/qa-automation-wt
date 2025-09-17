import pytest

from src.data.enums import AssetTabs, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.parametrize(
    "sl_type, tp_type",
    [
        pytest.param(SLTPType.POINTS, SLTPType.POINTS, marks=pytest.mark.critical),
        pytest.param(SLTPType.PRICE, SLTPType.PRICE, marks=pytest.mark.critical),
    ]
)
def test(android, market_obj, sl_type, tp_type, order_data, cancel_all):
    trade_object = market_obj()

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)}")
    order_data(trade_object, SLTPType.PRICE, SLTPType.PRICE)
    android.trade_screen.asset_tab.get_last_order_id(trade_object, wait=True)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    android.trade_screen.asset_tab.verify_item_data(trade_object, AssetTabs.OPEN_POSITION, False)

    logger.info(f"Step 2: Update order with sl_type: {sl_type.capitalize()!r} - tp_type: {tp_type.capitalize()!r}")
    android.trade_screen.asset_tab.modify_order(trade_object, sl_type, tp_type, confirm=False)

    logger.info(f"Verify trade edit confirmation")
    android.trade_screen.modals.verify_edit_trade_confirmation(trade_object)

    logger.info("Step 3: Confirm update order")
    android.trade_screen.modals.confirm_update_order()

    logger.info(f"Verify order updated notification banner")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner())

    logger.info(f"Verify order details after update")
    android.trade_screen.asset_tab.verify_item_data(trade_object)
