import pytest

from src.data.enums import AssetTabs, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize(
    "edit_field, sl_type, tp_type",
    [
        ("SL, TP", SLTPType.PRICE, SLTPType.PRICE),
        ("SL, TP", SLTPType.POINTS, SLTPType.POINTS),
    ]
)
def test(web, edit_field, sl_type, tp_type, close_edit_confirm_modal, market_obj):
    trade_obj = market_obj()

    logger.info("Step 1: Get tab amount")
    tab_amount = web.trade_page.asset_tab.get_tab_amount(AssetTabs.OPEN_POSITION)

    logger.info(f"Step 2: Place {trade_obj.trade_type.upper()} Market Order via OCT tab (tab:{tab_amount})")
    web.trade_page.place_order_panel.place_oct_order(trade_obj)

    logger.info(f"Verify tab amount increased to: {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info(f"Step 2: Update order with {edit_field!r}")
    web.trade_page.asset_tab.modify_order(trade_obj, sl_type=sl_type, tp_type=tp_type, oct_mode=True)

    logger.info("Verify notification banner updated message")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_obj).order_updated_banner(**trade_obj))

    logger.info(f"Verify order details after update")
    web.trade_page.asset_tab.verify_item_data(trade_obj, wait=True)
