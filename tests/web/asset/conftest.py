import random

import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, OrderType, Features
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.fixture(scope="package", autouse=True)
def setup(login_member_site):
    pass


@pytest.fixture
def search_symbol(web, symbol):
    logger.info(f"- Search and select symbol: {symbol}")
    web.home_page.search_and_select_symbol(symbol)


@pytest.fixture
def setup_bulk_asset_test(web, symbol):
    def _handler(order_type: OrderType = OrderType.MARKET):

        asset_tab = AssetTabs.get_tab(order_type)
        create_amount = random.randint(1, 5)
        tab_amount = APIClient().order.get_counts(order_type=order_type)

        if not tab_amount:
            trade_object = ObjTrade(order_type=order_type, symbol=symbol)
            logger.info(f"- Place {create_amount} {trade_object.trade_type.upper()} {trade_object.order_type.upper()}")
            for _ in range(create_amount):
                APIClient().trade.post_order(trade_object, update_price=False)

        logger.info("- Navigate to Asset Page")
        web.home_page.navigate_to(Features.ASSETS, wait=True)

        logger.info("- Get order id list")
        web.assets_page.asset_tab.select_tab(asset_tab)
        order_ids = web.trade_page.asset_tab.get_order_ids(asset_tab)

        return tab_amount, order_ids

    return _handler
