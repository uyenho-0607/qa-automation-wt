import time

import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, OrderType
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.order(1)
@pytest.mark.critical
def test(web, symbol, get_asset_tab_amount, close_confirm_modal):
    trade_object = ObjTrade(order_type=OrderType.STOP, symbol=symbol)
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place {trade_object.trade_type} order")
    web.trade_page.place_order_panel.place_order(trade_object, submit=True)

    logger.info(f"Verify Asset Tab amount is: {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount + 1)

    logger.info("Step 2: Get order_id of placed order")
    web.trade_page.asset_tab.get_last_order_id(trade_object)

    # logger.info("Verify placed order details")
    # web.trade_page.asset_tab.verify_item_data(trade_object)

    logger.info("Step 3: Get placed order API data")
    api_data = APIClient().order.get_orders_details(
        symbol=trade_object.symbol, order_id=trade_object.order_id, order_type=trade_object.order_type
    )

    logger.info("Verify placed order against API data")
    web.trade_page.verify_placed_order_data(trade_object, api_data)
