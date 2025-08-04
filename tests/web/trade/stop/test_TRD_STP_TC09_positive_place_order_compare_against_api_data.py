import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs
from src.utils.logging_utils import logger


@pytest.mark.order(1)
@pytest.mark.critical
def test(web, symbol, get_asset_tab_amount, close_confirm_modal, stop_obj):
    trade_object = stop_obj()

    logger.info("Step 1: Get asset tab amount")
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 2: Place {trade_object.trade_type} order (tab amount:{tab_amount!r})")
    web.trade_page.place_order_panel.place_order(trade_object, submit=True)

    logger.info(f"Verify Asset Tab amount is: {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount + 1)

    logger.info("Step 3: Select Pending Orders tab")
    web.trade_page.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info("Step 4: Get order_id of placed order")
    web.trade_page.asset_tab.get_last_order_id(trade_object)

    logger.info(f"Step 5: Get placed order API data, order_id: {trade_object.order_id!r}")
    api_data = APIClient().order.get_orders_details(
        symbol=trade_object.symbol, order_id=trade_object.order_id, order_type=trade_object.order_type
    )

    logger.info("Verify placed order against API data")
    web.trade_page.verify_placed_order_data(trade_object, api_data)
