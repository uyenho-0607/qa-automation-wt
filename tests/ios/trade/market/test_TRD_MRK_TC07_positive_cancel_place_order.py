import pytest

from src.data.enums import AssetTabs, SLTPType
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(ios, get_asset_tab_amount, market_obj):
    trade_object = market_obj()
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)}, tab:{tab_amount})")
    ios.trade_screen.place_order_panel.place_order(trade_object, confirm=False)

    logger.info("Step 2: Cancel Place Order")
    ios.trade_screen.modals.confirm_trade(confirm=False)

    logger.info(f"Verify Asset Tab amount is not changed: {tab_amount}")
    ios.trade_screen.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount)
