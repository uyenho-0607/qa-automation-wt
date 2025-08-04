import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs
from src.data.enums import SLTPType, OrderType, Expiry
from src.utils.logging_utils import logger


@pytest.mark.order(2)
@pytest.mark.critical
def test(web, limit_obj, close_edit_confirm_modal, create_order_data):
    trade_object = limit_obj()

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    create_order_data(trade_object)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    web.trade_page.asset_tab.verify_item_displayed(AssetTabs.PENDING_ORDER, trade_object.order_id)
    
    logger.info(f"Step 2: Modify order with SL and TP")
    web.trade_page.asset_tab.modify_order(trade_object, sl_type=SLTPType.random_values(), tp_type=SLTPType.random_values(), expiry=Expiry.sample_values(OrderType.LIMIT), confirm=True)

    logger.info(f"Verify item details after update")
    web.trade_page.asset_tab.verify_item_data(trade_object, wait=True)

    logger.info(f"Step 3: Get placed order API data, order_id: {trade_object.order_id!r}")
    api_data = APIClient().order.get_orders_details(
        symbol=trade_object["symbol"], order_id=trade_object["order_id"], order_type=trade_object["order_type"]
    )

    logger.info("Verify against API data")
    web.trade_page.verify_placed_order_data(trade_object, api_data)
