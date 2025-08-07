import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web_app, limit_obj, cancel_all, ):
    trade_object = limit_obj()

    logger.info("Step 1: Get asset tab amount")
    tab_amount = web_app.trade_page.asset_tab.get_tab_amount(AssetTabs.PENDING_ORDER)

    logger.info(f"Step 2: Place {trade_object.trade_type} order (tab amount: {tab_amount!r})")
    web_app.trade_page.place_order_panel.place_order(trade_object, submit=True)

    logger.info(f"Verify Asset Tab amount is: {tab_amount + 1}")
    web_app.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount + 1)

    logger.info("Step 3: Select Pending Order tab")
    web_app.trade_page.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info("Step 4: Get order_id of placed order")
    web_app.trade_page.asset_tab.get_last_order_id(trade_object)

    logger.info(f"Step 5: Get placed order API data, order_id: {trade_object.order_id!r}")
    api_data = APIClient().order.get_orders_details(
        symbol=trade_object.symbol, order_id=trade_object.order_id, order_type=trade_object.order_type
    )

    logger.info("Verify placed order against API data")
    web_app.trade_page.verify_placed_order_data(trade_object, api_data)
