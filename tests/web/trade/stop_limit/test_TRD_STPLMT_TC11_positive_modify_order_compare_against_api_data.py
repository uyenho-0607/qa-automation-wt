import pytest

from src.apis.api_client import APIClient
from src.data.enums import SLTPType, OrderType, Expiry
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, symbol, close_edit_confirm_modal, create_order_data):
    trade_object = ObjectTrade(order_type=OrderType.STOP_LIMIT, symbol=symbol)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order without Stop Loss and Take Profit")
    create_order_data(trade_object)

    logger.info(f"Step 2: Update item stop loss and take profit")
    web.trade_page.modals.modify_order(trade_object, sl_type=SLTPType.random_values(), tp_type=SLTPType.random_values(), expiry=Expiry.sample_values(OrderType.LIMIT), confirm=True)

    logger.info(f"Verify item details after update")
    web.trade_page.asset_tab.verify_item_data(trade_object)

    logger.info("Step 3: Get placed order API data")
    api_data = APIClient().order.get_orders_details(
        symbol=trade_object.symbol, order_id=trade_object.order_id, order_type=trade_object.order_type
    )

    logger.info("Verify against API data")
    web.trade_page.verify_placed_order_data(trade_object, api_data)
