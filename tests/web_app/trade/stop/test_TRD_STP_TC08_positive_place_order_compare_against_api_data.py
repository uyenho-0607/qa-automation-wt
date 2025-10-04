import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web_app, stop_obj, get_asset_tab_amount, order_data, cancel_all):
    trade_object = stop_obj()

    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)} (tab:{tab_amount})")
    order_data(trade_object)

    logger.info("Step 2: Select Pending Orders tab")
    web_app.trade_page.asset_tab.select_tab(AssetTabs.PENDING_ORDER)
    web_app.trade_page.asset_tab.get_last_order_id(trade_object) # get placed order_id

    logger.info(f"Verify Asset Tab amount is: {tab_amount + 1}")
    web_app.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount + 1)

    logger.info(f"Step 3: Get placed order API data, order_id: {trade_object.order_id!r}")
    api_data = APIClient().order.get_orders_details(
        symbol=trade_object.symbol, order_id=trade_object.order_id, order_type=trade_object.order_type
    )

    logger.info("Verify placed order against API data")
    web_app.trade_page.verify_placed_order_data(trade_object, api_data)
