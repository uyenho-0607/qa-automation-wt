import random

import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, OrderType
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@pytest.fixture(scope="package")
def create_order_data(web, get_asset_tab_amount, symbol):
    def _handler(trade_object):
        tab = AssetTabs.get_tab(trade_object.order_type)
        current_amount = get_asset_tab_amount(trade_object.order_type)

        logger.info(f"- POST {trade_object.trade_type.upper()} {trade_object.order_type.upper()} order")
        res = APIClient().trade.post_order(trade_object)

        # Loading new created data
        web.trade_page.asset_tab.wait_for_tab_amount(tab, expected_amount=current_amount + 1)

        return res

    return _handler


@pytest.fixture
def setup_bulk_test(web, symbol):
    def _handler(order_type: OrderType = OrderType.MARKET):

        asset_tab = AssetTabs.get_tab(order_type)
        create_amount = random.randint(1, 10)
        order_ids = APIClient().order.get_order_id_list(symbol, order_type)

        if not order_ids:
            trade_object = ObjectTrade(order_type=order_type, symbol=symbol)

            logger.info(f"- Place {create_amount} {order_type.upper()} orders")
            for _ in range(create_amount):
                APIClient().trade.post_order(trade_object)

            web.trade_page.wait_for_spin_loader()
            web.trade_page.asset_tab.wait_for_tab_amount(asset_tab, expected_amount=create_amount)

        order_ids = APIClient().order.get_order_id_list(symbol, order_type)

        return order_ids

    return _handler
