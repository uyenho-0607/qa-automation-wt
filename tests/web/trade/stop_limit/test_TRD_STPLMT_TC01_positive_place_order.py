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
def test(web, stop_limit_obj, get_asset_tab_amount, sl_type, tp_type, close_confirm_modal):
    trade_object = stop_limit_obj()
    tab = AssetTabs.PENDING_ORDER
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)} (SL:{sl_type.value.title() if sl_type else None}, TP:{tp_type.value.title() if tp_type else None})")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type)

    logger.info(f"Verify trade confirmation")
    web.trade_page.modals.verify_trade_confirmation(trade_object)

    logger.info("Step 2: Confirm place order")
    web.home_page.get_server_device_time(trade_object)
    web.trade_page.modals.confirm_trade()

    logger.info("Verify notification banner displays correct input trade information")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_submitted_banner())

    logger.info(f"Verify tab amount increased to {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(tab, tab_amount + 1)

    logger.info(f"Verify order details in tab")
    web.trade_page.asset_tab.verify_item_data(trade_object)
