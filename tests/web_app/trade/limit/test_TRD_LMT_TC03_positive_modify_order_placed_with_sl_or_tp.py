import pytest

from src.data.enums import AssetTabs, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
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
def test(web_app, limit_obj, exclude_field, update_field, order_data, cancel_all):
    trade_object = limit_obj()
    update_info = {f"{item.lower()}_type": SLTPType.random_values() for item in update_field.split(",")}

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)} without {exclude_field}")
    order_data(trade_object, **{f"{exclude_field.lower()}_type": None})

    logger.info("Step 2: Select Pending Orders tab")
    web_app.trade_page.asset_tab.select_tab(AssetTabs.PENDING_ORDER)
    trade_object.order_id = web_app.trade_page.asset_tab.get_last_order_id(AssetTabs.PENDING_ORDER) # get placed order_id

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    web_app.trade_page.asset_tab.verify_item_data(trade_object, AssetTabs.PENDING_ORDER, wait=False)

    logger.info(f"Step 3: Update placed order with {update_field!r}")
    web_app.trade_page.asset_tab.modify_order(trade_object, **update_info, confirm=False)

    logger.info(f"Verify trade edit confirmation")
    web_app.trade_page.modals.verify_edit_trade_confirmation(trade_object)

    logger.info("Step 4: Confirm update order")
    web_app.trade_page.modals.confirm_update_order()

    logger.info(f"Verify order updated notification banner")
    web_app.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner())

    logger.info("Step 5: Select Pending Orders tab")
    web_app.trade_page.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info(f"Verify order details after update")
    web_app.trade_page.asset_tab.verify_item_data(trade_object)
