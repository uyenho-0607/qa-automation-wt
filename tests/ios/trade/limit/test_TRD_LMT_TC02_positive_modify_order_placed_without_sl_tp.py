import json

import pytest

from src.data.enums import AssetTabs
from src.data.enums import SLTPType
from src.data.objects.notification_obj import ObjNoti
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
def test(ios, limit_obj, edit_field, sl_type, tp_type, order_data):
    trade_object = limit_obj()

    logger.info(f"Step 1: Place order {json.dumps(trade_object.to_dict(), indent=2)} without SL and TP")
    order_data(trade_object, None, None)

    logger.info("Step 2: Select Pending Orders tab")
    ios.trade_screen.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    trade_object.order_id = ios.trade_screen.asset_tab.get_last_order_id(AssetTabs.PENDING_ORDER, True)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    ios.trade_screen.asset_tab.verify_item_data(trade_object, AssetTabs.PENDING_ORDER)

    logger.info(f"Step 3: Update placed order with {edit_field!r}")
    ios.trade_screen.asset_tab.modify_order(trade_object, sl_type, tp_type, confirm=False)

    logger.info(f"Verify trade edit confirmation")
    ios.trade_screen.modals.verify_edit_trade_confirmation(trade_object)

    logger.info("Step 4: Confirm update order")
    ios.trade_screen.modals.confirm_update_order()

    logger.info(f"Verify order updated notification banner")
    ios.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).order_updated_banner())

    logger.info("Step 5: Select Pending Orders tab")
    ios.trade_screen.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info(f"Verify order details after update")
    ios.trade_screen.asset_tab.verify_item_data(trade_object)
