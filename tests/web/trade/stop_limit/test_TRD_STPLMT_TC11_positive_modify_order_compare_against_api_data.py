import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs
from src.data.enums import SLTPType, OrderType, Expiry
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, stop_limit_obj, close_edit_confirm_modal, order_data):
    trade_object = stop_limit_obj()

    logger.info(f"Step 1: Place order with: {format_display_dict(trade_object)}")
    order_data(trade_object, SLTPType.PRICE, SLTPType.PRICE)
    trade_object.order_id = web.trade_page.asset_tab.get_last_order_id(AssetTabs.PENDING_ORDER) # Get latest orderID

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    web.trade_page.asset_tab.verify_item_data(trade_object, AssetTabs.PENDING_ORDER, False)

    logger.info(f"Step 2: Update placed order with SL and TP")
    web.trade_page.asset_tab.modify_order(trade_object, sl_type=SLTPType.random_values(), tp_type=SLTPType.random_values(), expiry=Expiry.sample_values(OrderType.STOP_LIMIT), confirm=True)

    logger.info(f"Verify item details after update")
    web.trade_page.asset_tab.verify_item_data(trade_object, wait=True)

    logger.info(f"Step 3: Get placed order API data, order_id: {trade_object.order_id!r}")
    api_data = APIClient().order.get_orders_details(
        symbol=trade_object["symbol"], order_id=trade_object["order_id"], order_type=trade_object["order_type"], exclude_issue_symbols=False
    )

    logger.info("Verify against API data")
    web.trade_page.verify_placed_order_data(trade_object, api_data)
