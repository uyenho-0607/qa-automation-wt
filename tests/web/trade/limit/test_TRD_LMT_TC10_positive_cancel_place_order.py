import pytest

from src.data.enums import AssetTabs, SLTPType
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, limit_obj, close_confirm_modal, get_asset_tab_amount):

    trade_object = limit_obj()
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)}")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=SLTPType.sample_values(), tp_type=SLTPType.sample_values())

    logger.info("Step 2: Cancel Place Order")
    web.trade_page.modals.close_trade_confirm_modal()

    logger.info(f"Verify tab amount is not changed: {tab_amount}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount)
