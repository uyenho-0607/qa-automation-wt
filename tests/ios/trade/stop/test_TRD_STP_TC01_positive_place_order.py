import pytest

from src.data.enums import AssetTabs, SLTPType, Features
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
def test(ios, stop_obj, sl_type, tp_type, get_asset_tab_amount):
    trade_object = stop_obj()

    tab = AssetTabs.PENDING_ORDER

    logger.info("Step 1: Get asset tab amount")
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 2: Place order: {format_display_dict(trade_object)} - (SL:{sl_type.value.title() if sl_type else None}, TP:{tp_type.value.title() if tp_type else None}, tab:{tab_amount})")
    ios.trade_screen.place_order_panel.place_order(trade_object, sl_type, tp_type, confirm=False)

    logger.info(f"Verify trade confirmation")
    ios.trade_screen.modals.verify_trade_confirmation(trade_object)

    logger.info("Step 3: Confirm place order")
    ios.trade_screen.modals.confirm_trade()

    logger.info(f"Verify order submitted notification banner")
    ios.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).order_submitted_banner())

    logger.info(f"Step 4: Select {tab.value.title()!r} tab")
    ios.trade_screen.asset_tab.select_tab(tab)

    logger.info(f"Verify tab amount increased to {tab_amount + 1}")
    ios.trade_screen.asset_tab.verify_tab_amount(tab, tab_amount + 1)

    logger.info(f"Verify order details in tab")
    ios.trade_screen.asset_tab.verify_item_data(trade_object)


@pytest.fixture(autouse=True)
def teardown(ios):
    yield
    logger.info("[Cleanup] Navigate back to Trade Screen", teardown=True)
    ios.home_screen.navigate_to(Features.TRADE)