import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(ios, stop_limit_obj, get_asset_tab_amount, cancel_all):
    trade_object = stop_limit_obj()
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)} (tab:{tab_amount})")
    ios.trade_screen.place_order_panel.place_order(trade_object, confirm=True)

    logger.info(f"Verify Asset Tab amount is: {tab_amount + 1}")
    ios.trade_screen.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount + 1)

    logger.info("Step 2: Select Pending Order tab")
    ios.trade_screen.asset_tab.select_tab(AssetTabs.PENDING_ORDER)
    trade_object.order_id = ios.trade_screen.asset_tab.get_last_order_id(AssetTabs.PENDING_ORDER, wait=True)

    logger.info(f"Step 3: Get placed order API data, order_id: {trade_object.order_id!r}")
    api_data = APIClient().order.get_orders_details(
        symbol=trade_object.symbol, order_id=trade_object.order_id, order_type=trade_object.order_type, exclude_issue_symbols=False
    )

    logger.info("Verify placed order against API data")
    ios.trade_screen.verify_placed_order_data(trade_object, api_data)