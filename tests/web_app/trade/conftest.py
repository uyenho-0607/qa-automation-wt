import random

import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, Features, OrderType
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.fixture(scope="package", autouse=True)
def setup(login_member_site, web_app, symbol):
    logger.info(f"[Setup] Search and select symbol: {symbol}")
    web_app.home_page.search_and_select_symbol(symbol)


@pytest.fixture(scope="package")
def create_order_data(web_app, get_asset_tab_amount, symbol):
    def _handler(trade_object):
        tab = AssetTabs.get_tab(trade_object.order_type)
        current_amount = get_asset_tab_amount(trade_object.order_type)

        logger.info(f"- POST {trade_object.trade_type.upper()} {trade_object.order_type.upper()} order")
        res = APIClient().trade.post_order(trade_object)

        web_app.trade_page.asset_tab.select_tab(tab.HISTORY)
        web_app.trade_page.asset_tab.select_tab(tab)

        # Loading new created data
        web_app.trade_page.asset_tab.wait_for_tab_amount(tab, expected_amount=current_amount + 1)

        return res, current_amount + 1

    return _handler


@pytest.fixture(scope="package")
def swap_to_volume(web_app):
    logger.info("[Setup] Send API to use volume")
    APIClient().user.patch_swap_volume_units()


@pytest.fixture(scope="package")
def swap_to_units():
    logger.info("[Setup] Send API to use units")
    APIClient().user.patch_swap_volume_units(use_volume=False)


@pytest.fixture
def setup_bulk_test(web_app, symbol):
    def _handler(order_type: OrderType = OrderType.MARKET):

        asset_tab = AssetTabs.get_tab(order_type)
        create_amount = random.randint(1, 10)
        order_ids = APIClient().order.get_order_id_list(symbol, order_type)

        if not order_ids:
            logger.info(f"- Place {create_amount} {order_type.upper()} orders")
            for _ in range(create_amount):
                APIClient().trade.post_order(ObjTrade(order_type=order_type, symbol=symbol), update_price=False)

        web_app.trade_page.navigate_to(Features.HOME)
        web_app.home_page.navigate_to(Features.TRADE)
        web_app.trade_page.asset_tab.wait_for_tab_amount(asset_tab, expected_amount=create_amount)

        order_ids = APIClient().order.get_order_id_list(symbol, order_type)

        return order_ids

    return _handler
