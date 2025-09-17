import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, SLTPType
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(android, market_obj, order_data):
    trade_object = market_obj()

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)} without SL and TP")
    order_data(trade_object, None, None)
    android.trade_screen.asset_tab.get_last_order_id(trade_object, wait=True)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    android.trade_screen.asset_tab.verify_item_data(trade_object, AssetTabs.OPEN_POSITION, wait=False)

    logger.info(f"Step 2: Modify order with SL and TP")
    android.trade_screen.asset_tab.modify_order(trade_object, sl_type=SLTPType.random_values(), tp_type=SLTPType.random_values(), confirm=True)

    logger.info(f"Verify item details after update")
    android.trade_screen.asset_tab.verify_item_data(trade_object)

    logger.info(f"Step 3: Get placed order API data, order_id: {trade_object.order_id!r}")
    api_data = APIClient().order.get_orders_details(
        symbol=trade_object.symbol, order_id=trade_object.order_id, order_type=trade_object.order_type
    )

    logger.info("Verify against API data")
    android.trade_screen.verify_placed_order_data(trade_object, api_data)
