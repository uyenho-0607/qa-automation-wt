import pytest

from src.data.enums import AssetTabs, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize("edit_field, sl_type, tp_type", [("SL, TP", SLTPType.PRICE, SLTPType.PRICE)])
def test(web, edit_field, sl_type, tp_type, close_edit_confirm_modal, market_obj, get_asset_tab_amount):
    trade_obj = market_obj()
    tab_amount = get_asset_tab_amount(trade_obj.order_type)

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_obj)} via OCT tab")
    web.trade_page.place_order_panel.place_oct_order(trade_obj)
    web.home_page.notifications.close_noti_banner()

    logger.info(f"Verify tab amount increased to {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info(f"Step 2: Update placed order with {edit_field!r}")
    web.trade_page.asset_tab.modify_order(trade_obj, sl_type=sl_type, tp_type=tp_type, oct_mode=True)

    logger.info("Verify notification banner updated message")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_obj).order_updated_banner())

    logger.info(f"Verify order details after update")
    web.trade_page.asset_tab.verify_item_data(trade_obj, wait=True)
