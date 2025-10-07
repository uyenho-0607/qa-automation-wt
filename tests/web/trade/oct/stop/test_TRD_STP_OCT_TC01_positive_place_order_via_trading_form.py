import pytest

from src.data.enums import AssetTabs, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize("sl_type, tp_type", [(SLTPType.PRICE, SLTPType.PRICE)])
def test(web, stop_obj, sl_type, tp_type, get_asset_tab_amount):
    trade_object = stop_obj()
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)} (SL:{sl_type.value.title() if sl_type else None}, TP:{tp_type.value.title() if tp_type else None})")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type, submit=False)
    web.home_page.get_server_device_time(trade_object)

    logger.info(f"Verify order submitted notification banner")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_submitted_banner())

    logger.info(f"Verify tab amount increased to {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount + 1)

    logger.info(f"Verify order details in tab")
    web.trade_page.asset_tab.verify_item_data(trade_object)
