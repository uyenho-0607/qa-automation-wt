import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, SLTPType, OrderType, Expiry
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(ios, stop_obj, order_data):
    trade_object = stop_obj()

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)}")
    order_data(trade_object)

    logger.info("Step 2: Select Pending Order tab")
    ios.trade_screen.asset_tab.select_tab(AssetTabs.PENDING_ORDER)
    trade_object.order_id = ios.trade_screen.asset_tab.get_last_order_id(AssetTabs.PENDING_ORDER, wait=True)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    ios.trade_screen.asset_tab.verify_item_data(trade_object, AssetTabs.PENDING_ORDER, wait=False)

    logger.info(f"Step 3: Modify order with SL and TP")
    ios.trade_screen.asset_tab.modify_order(trade_object, sl_type=SLTPType.random_values(), tp_type=SLTPType.random_values(), confirm=True)

    logger.info("Step 4: Select Pending Order tab")
    ios.trade_screen.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info(f"Verify item details after update")
    ios.trade_screen.asset_tab.verify_item_data(trade_object)

    logger.info(f"Step 5: Get placed order API data, order_id: {trade_object.order_id!r}")
    api_data = APIClient().order.get_orders_details(
        symbol=trade_object.symbol, order_id=trade_object.order_id, order_type=trade_object.order_type
    )

    logger.info("Verify against API data")
    ios.trade_screen.verify_placed_order_data(trade_object, api_data)