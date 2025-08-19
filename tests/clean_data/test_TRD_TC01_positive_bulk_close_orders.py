import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, OrderType
from src.utils.logging_utils import logger


@pytest.mark.parametrize(
    "tab, order_type",
    [
        (AssetTabs.OPEN_POSITION, OrderType.MARKET),
        (AssetTabs.PENDING_ORDER, OrderType.LIMIT),
    ]
)
def test_bulk_action(web, get_order_list, tab, order_type):
    logger.info(f"Step 1: Navigate to {tab.name} tab")
    web.trade_page.asset_tab.select_tab(tab=tab)

    while True:
        try:
            logger.info("Step 2: Retrieve the Order Details")
            orders = get_order_list(order_type=order_type)

            if not orders:  # stops the loop if orders is empty
                logger.info("No more orders left to process. Exiting loop.")
                break

            logger.info(f"Step 3: Perform bulk {'close' if tab == AssetTabs.OPEN_POSITION else 'delete'}")
            APIClient().trade.bulk_close_orders(orders, tab=tab)

        except Exception as e:
            logger.exception(f"An error occurred during bulk action: {e}")
            break
