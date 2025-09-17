import pytest

from src.data.enums import AssetTabs, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.parametrize(
    "exclude_field, update_field",
    [
        pytest.param("SL", "TP", marks=pytest.mark.critical),
        pytest.param("TP", "SL", marks=pytest.mark.critical),
    ]
)
def test(android, limit_obj, exclude_field, update_field, order_data, cancel_all):
    trade_object = limit_obj()
    update_info = {f"{exclude_field.lower()}_type": None, f"{update_field.lower()}_type": SLTPType.random_values()}

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)} without {exclude_field}")
    order_data(trade_object, **{f"{exclude_field.lower()}_type": None})

    logger.info("Step 2: Select Pending Orders tab")
    android.trade_screen.asset_tab.select_tab(AssetTabs.PENDING_ORDER)
    trade_object.order_id = android.trade_screen.asset_tab.get_last_order_id(AssetTabs.PENDING_ORDER, wait=True)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    android.trade_screen.asset_tab.verify_item_data(trade_object, AssetTabs.PENDING_ORDER, wait=False)

    logger.info(f"Step 3: Update placed order with {update_field!r}")
    android.trade_screen.asset_tab.modify_order(trade_object, **update_info, confirm=False)

    logger.info(f"Verify trade edit confirmation")
    android.trade_screen.modals.verify_edit_trade_confirmation(trade_object)

    logger.info("Step 4: Confirm update order")
    android.trade_screen.modals.confirm_update_order()

    logger.info(f"Verify order updated notification banner")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner())

    logger.info("Step 5: Select Pending Orders tab")
    android.trade_screen.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info(f"Verify order details after update")
    android.trade_screen.asset_tab.verify_item_data(trade_object)
