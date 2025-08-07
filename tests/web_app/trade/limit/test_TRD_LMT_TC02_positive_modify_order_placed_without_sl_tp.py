import pytest

from src.data.enums import AssetTabs
from src.data.enums import SLTPType, OrderType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
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
def test(web_app, limit_obj, edit_field, sl_type, tp_type, create_order_data, cancel_all):
    trade_object = limit_obj(stop_loss=0, take_profit=0)
    # -------------------

    logger.info("Step 1: Place order without SL and TP")
    create_order_data(trade_object)

    logger.info("Step 2: Select Pending Orders tab")
    web_app.trade_page.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    web_app.trade_page.asset_tab.verify_item_displayed(AssetTabs.PENDING_ORDER, trade_object.order_id)

    logger.info(f"Step 3: Update placed order with {edit_field!r}")
    web_app.trade_page.asset_tab.modify_order(trade_object, sl_type=sl_type, tp_type=tp_type)

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
