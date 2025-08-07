import pytest

from src.data.enums import AssetTabs
from src.apis.api_client import APIClient
from src.data.enums import SLTPType, OrderType, Expiry
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.order(2)
@pytest.mark.critical
def test(android, symbol, create_order_data):
    trade_object = ObjTrade(order_type=OrderType.STOP, symbol=symbol)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    create_order_data(trade_object)
    
    logger.info("Step 2: Select Pending Order tab")
    android.trade_screen.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    android.trade_screen.asset_tab.verify_item_displayed(AssetTabs.PENDING_ORDER, trade_object.order_id)
    
    logger.info(f"Step 3: Modify order with SL and TP")
    android.trade_screen.modals.modify_order(trade_object, sl_type=SLTPType.random_values(), tp_type=SLTPType.random_values(), expiry=Expiry.sample_values(OrderType.STOP), confirm=True)

    logger.info("Step 4: Select Pending Order tab")
    android.trade_screen.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info(f"Verify item details after update")
    android.trade_screen.asset_tab.verify_item_data(trade_object)

    logger.info(f"Step 5: Get placed order API data, order_id: {trade_object.order_id!r}")
    api_data = APIClient().order.get_orders_details(
        symbol=trade_object.symbol, order_id=trade_object.order_id, order_type=trade_object.order_type
    )

    logger.info("Verify against API data")
    android.trade_screen.verify_placed_order_data(trade_object, api_data)
