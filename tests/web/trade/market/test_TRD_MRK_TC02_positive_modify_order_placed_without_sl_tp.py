import pytest

from src.data.enums import SLTPType, AssetTabs
from src.data.objects.notification_obj import ObjNoti
from src.utils.logging_utils import logger
from tests.web.trade.conftest import create_order_data


@pytest.mark.parametrize(
    "edit_field, sl_type, tp_type",
    [
        ("SL", SLTPType.random_values(), None),
        ("TP", None, SLTPType.random_values()),
        pytest.param("SL, TP", SLTPType.PRICE, SLTPType.PRICE, marks=pytest.mark.critical),
        pytest.param("SL, TP", SLTPType.POINTS, SLTPType.POINTS, marks=pytest.mark.critical),
        ("SL, TP", *SLTPType.sample_values(amount=2)),
    ]
)
def test(web, market_obj, edit_field, sl_type, tp_type, close_edit_confirm_modal, create_order_data):
    trade_object = market_obj(stop_loss=0, take_profit=0)
    # -------------------

    logger.info(f"Step 1: Place {trade_object.trade_type} Order without SL and TP")
    create_order_data(trade_object)

    logger.info(f"Verify order placed successfully, order_id = {trade_object.order_id!r}")
    web.trade_page.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, trade_object.order_id)

    logger.info(f"Step 2: Update order with {edit_field!r}")
    web.trade_page.asset_tab.modify_order(trade_object, sl_type=sl_type, tp_type=tp_type)

    logger.info(f"Verify trade edit confirmation")
    web.trade_page.modals.verify_edit_trade_confirmation(trade_object)

    logger.info("Step 3: Confirm update order")
    web.trade_page.modals.confirm_update_order()

    logger.info(f"Verify order updated notification banner")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner())

    logger.info(f"Verify order details after update")
    web.trade_page.asset_tab.verify_item_data(trade_object, wait=True)
