import pytest

from src.data.enums import AssetTabs, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize(
    "sl_type, tp_type",
    [
        (None, None),
        (SLTPType.POINTS, None),
        (None, SLTPType.PRICE),
        (SLTPType.PRICE, SLTPType.PRICE)
    ]
)
def test(android, cancel_all, sl_type, tp_type, stop_obj, get_asset_tab_amount):
    trade_object = stop_obj()
    tab = AssetTabs.PENDING_ORDER

    logger.info("Step 1: Get asset tab amount")
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 2: Place order with: {format_display_dict(trade_object)} - (SL:{sl_type.value.title() if sl_type else None}, TP:{tp_type.value.title() if tp_type else None}, tab:{tab_amount})")
    android.trade_screen.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type)

    logger.info(f"Verify trade confirmation")
    android.trade_screen.modals.verify_trade_confirmation(trade_object)

    logger.info("Step 3: Confirm place order")
    android.trade_screen.modals.confirm_trade()

    logger.info(f"Verify order submitted notification banner")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).order_submitted_banner())

    logger.info("Step 4: Select Pending Orders tab")
    android.trade_screen.asset_tab.select_tab(tab)

    logger.info(f"Verify Pending Order tab amount increased to {tab_amount + 1}")
    android.trade_screen.asset_tab.verify_tab_amount(tab, tab_amount + 1)

    logger.info(f"Verify order details in Pending Order tab")
    android.trade_screen.asset_tab.verify_item_data(trade_object)

