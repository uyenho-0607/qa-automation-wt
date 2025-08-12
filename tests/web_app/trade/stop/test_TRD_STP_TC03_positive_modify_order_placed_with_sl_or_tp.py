import pytest

from src.data.enums import AssetTabs, SLTPType
from src.data.objects.notification_obj import ObjNoti
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
def test(web_app, stop_obj, get_asset_tab_amount, exclude_field, update_field, create_order_data, cancel_all):

    trade_object = stop_obj()
    trade_object[exclude_field] = 0
    update_info = {f"{item.lower()}_type": SLTPType.POINTS for item in update_field.split(",")}
    # -------------------

    logger.info(f"Step 1: Place {trade_object.trade_type} Order with SL/ TP ({exclude_field} = 0)")
    create_order_data(trade_object)

    logger.info("Step 2: Select Pending Orders tab")
    web_app.trade_page.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    web_app.trade_page.asset_tab.verify_item_displayed(AssetTabs.PENDING_ORDER, trade_object.order_id)

    logger.info(f"Step 3: Modify order with {update_field!r} {' - '.join(list(update_info.values()))}")
    web_app.trade_page.asset_tab.modify_order(trade_object, **update_info)

    logger.info(f"Verify trade edit confirmation")
    web_app.trade_page.modals.verify_edit_trade_confirmation(trade_object)

    logger.info("Step 4: Confirm update order")
    web_app.trade_page.modals.confirm_update_order()

    logger.info(f"Verify order updated notification banner")
    web_app.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner(**trade_object))

    logger.info("Step 5: Select Pending Orders tab")
    web_app.trade_page.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info(f"Verify order details after update")
    web_app.trade_page.asset_tab.verify_item_data(trade_object)
