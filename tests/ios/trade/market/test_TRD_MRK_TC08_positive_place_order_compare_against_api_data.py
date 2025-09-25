import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(ios, market_obj, get_asset_tab_amount, order_data):
    trade_object = market_obj()
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)}")
    order_data(trade_object)
    trade_object.order_id = ios.trade_screen.asset_tab.get_last_order_id(AssetTabs.OPEN_POSITION, True)

    logger.info(f"Verify Asset Tab amount is: {tab_amount + 1}")
    ios.trade_screen.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info(f"Step 2: Get placed order API data, order_id: {trade_object.order_id!r}")
    api_data = APIClient().order.get_orders_details(
        trade_object.symbol, trade_object.order_type, trade_object.order_id
    )

    logger.info("Verify placed order against API data")
    ios.trade_screen.verify_placed_order_data(trade_object, api_data)
