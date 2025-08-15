import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, OrderType
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.fixture
def pre_setup_order(symbol, web):
    order_type = OrderType.sample_values()
    tab = AssetTabs.get_tab(order_type)

    tab_amount = APIClient().order.get_counts(order_type=order_type)
    trade_object = ObjTrade(order_type=order_type, symbol=symbol)

    if not tab_amount:
        logger.info("- Place new order")
        APIClient().trade.post_order(trade_object, update_price=False)

        logger.info("- Wait for asset tab amount increase")
        web.assets_page.asset_tab.wait_for_tab_amount(tab, tab_amount + 1)

    yield tab
