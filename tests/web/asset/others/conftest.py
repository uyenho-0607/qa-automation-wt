import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, OrderType
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@pytest.fixture
def pre_setup_order(symbol, web):
    order_type = OrderType.sample_values()
    tab = AssetTabs.get_tab(order_type)

    tab_amount = APIClient().order.get_counts(order_type=order_type)
    trade_object = ObjectTrade(order_type=order_type, symbol=symbol)

    if not tab_amount:
        logger.info("- Place new order")
        web.trade_page.place_order_panel.place_order(trade_object, submit=True)

        logger.info("- Wait for asset tab amount increase")
        web.trade_page.asset_tab.wait_for_tab_amount(tab, tab_amount + 1)

    yield tab
