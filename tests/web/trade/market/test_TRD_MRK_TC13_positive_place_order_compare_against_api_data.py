import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, OrderType
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, update_trade_obj, market_obj, get_asset_tab_amount, symbol, close_confirm_modal):
    step_idx = 2

    logger.info("Step 1: Get current placed orders")
    order_data = web.trade_page.asset_tab.get_item_data(AssetTabs.OPEN_POSITION)
    trade_object = update_trade_obj(order_data)

    if not trade_object:
        trade_object = market_obj()

        logger.info("Step 2: No available placed orders - get asset tab amount")
        tab_amount = get_asset_tab_amount(trade_object.order_type)

        logger.info(f"Step 3: Place {trade_object.trade_type} order (tab:{tab_amount!r})")
        web.trade_page.place_order_panel.place_order(trade_object, submit=True)

        logger.info(f"Verify Asset Tab amount is: {tab_amount + 1}")
        web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

        logger.info("Step 4: Get order_id of placed order")
        web.trade_page.asset_tab.get_last_order_id(trade_object)
        step_idx = 5

    logger.info(f"Step {step_idx}: Get placed order API data (order_id:{trade_object.order_id!r})")
    api_data = APIClient().order.get_orders_details(
        symbol=symbol, order_id=trade_object.order_id, order_type=trade_object.order_type
    )

    logger.info("Verify placed order against API data")
    web.trade_page.verify_placed_order_data(trade_object, api_data)


@pytest.fixture
def update_trade_obj(symbol):
    def _handler(order_data):
        if not order_data:
            return None

        order_data['trade_type'] = order_data.pop("order_type", None)
        trade_obj = ObjTrade(order_type=OrderType.MARKET, symbol=symbol, **order_data)

        return trade_obj

    return _handler
