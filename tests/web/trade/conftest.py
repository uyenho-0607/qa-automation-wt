import random

import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, OrderType
from src.data.enums import Features
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.fixture(scope="package", autouse=True)
def setup(login_member_site, web, symbol, disable_OCT):
    logger.info(f"{'=' * 10} Setup Trade Package - Start {'=' * 10}")

    logger.info("- Navigate to Trade Page")
    web.home_page.navigate_to(Features.TRADE)

    logger.info(f"- Search and select symbol: {symbol}")
    web.home_page.search_and_select_symbol(symbol)

    logger.info(f"{'=' * 10} Setup Trade Package - Done {'=' * 10}")


@pytest.fixture(scope="package")
def create_order_data(web, get_asset_tab_amount, symbol):
    def _handler(trade_object, update_price=True):

        tab = AssetTabs.get_tab(trade_object.order_type)

        logger.info(f"- Select tab: {tab.value.title()}")
        web.trade_page.asset_tab.select_tab(tab)

        logger.info("- Get tab amount")
        tab_amount = web.trade_page.asset_tab.get_tab_amount(tab)

        logger.info(f"- Send API to place {trade_object.trade_type.upper()} {trade_object.order_type.upper()} order (tab_amount:{tab_amount})")
        res = APIClient().trade.post_order(trade_object, update_price=update_price)

        # wait for loading new created data
        web.trade_page.asset_tab.wait_for_tab_amount(tab, expected_amount=tab_amount + 1)

        return res, tab_amount

    return _handler


@pytest.fixture
def setup_bulk_test(web, symbol):
    def _handler(order_type: OrderType = OrderType.MARKET):

        asset_tab = AssetTabs.get_tab(order_type)
        create_amount = random.randint(1, 10)
        order_ids = APIClient().order.get_order_id_list(symbol, order_type)

        if not order_ids:
            trade_object = ObjTrade(order_type=order_type, symbol=symbol)

            logger.info(f"- Place {create_amount} {order_type.upper()} orders")
            for _ in range(create_amount):
                APIClient().trade.post_order(trade_object, update_price=False)

            web.trade_page.wait_for_spin_loader()
            web.trade_page.asset_tab.wait_for_tab_amount(asset_tab, expected_amount=create_amount)

        order_ids = APIClient().order.get_order_id_list(symbol, order_type)

        return order_ids

    return _handler
