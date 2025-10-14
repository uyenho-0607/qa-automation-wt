import pytest

from src.data.enums import AssetTabs, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.parametrize(
    "edit_field, sl_type, tp_type",
    [
        ("SL", SLTPType.random_values(), None),
        ("TP", None, SLTPType.random_values()),
        pytest.param("SL, TP", SLTPType.PRICE, SLTPType.PRICE, marks=pytest.mark.critical),
        pytest.param("SL, TP", SLTPType.POINTS, SLTPType.POINTS, marks=pytest.mark.critical),
        ("SL, TP", *SLTPType.random_values(amount=2)),
    ]
)
def test(web_app, market_obj, edit_field, sl_type, tp_type, order_data, cancel_all):
    trade_object = market_obj()

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)} without SL and TP")
    order_data(trade_object, None, None)
    trade_object.order_id = web_app.trade_page.asset_tab.get_last_order_id(AssetTabs.OPEN_POSITION)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    web_app.trade_page.asset_tab.verify_item_data(trade_object, AssetTabs.OPEN_POSITION, False)

    logger.info(f"Step 2: Update placed order with {edit_field!r}")
    web_app.trade_page.asset_tab.modify_order(trade_object, sl_type=sl_type, tp_type=tp_type, confirm=False)

    logger.info(f"Verify trade edit confirmation")
    web_app.trade_page.modals.verify_edit_trade_confirmation(trade_object)

    logger.info("Step 3: Confirm update order")
    web_app.trade_page.modals.confirm_update_order()

    logger.info(f"Verify order updated notification banner")
    web_app.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner())

    logger.info(f"Verify order details after update")
    web_app.trade_page.asset_tab.verify_item_data(trade_object)
