import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, OrderType
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(android, symbol, get_asset_tab_amount, ):
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)

    logger.info("Step 1: Get asset tab amount")
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 2: Place {trade_object.trade_type} order (tab amount: {tab_amount!r})")
    android.trade_screen.place_order_panel.place_order(trade_object, submit=True)

    logger.info(f"Verify Asset Tab amount is: {tab_amount + 1}")
    android.trade_screen.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info("Step 3: Get order_id of placed order")
    android.trade_screen.asset_tab.get_last_order_id(trade_object)

    logger.info(f"Step 4: Get placed order API data, order_id: {trade_object.order_id!r}")
    api_data = APIClient().order.get_orders_details(
        symbol=trade_object.symbol, order_id=trade_object.order_id, order_type=trade_object.order_type, exclude_issue_symbols=False
    )

    logger.info("Verify placed order against API data")
    android.trade_screen.verify_placed_order_data(trade_object, api_data)


@pytest.fixture(autouse=True)
def teardown_test(android):
    yield
    logger.info("- Teardown test")
    android.trade_screen.place_order_panel.click_cancel_btn()
