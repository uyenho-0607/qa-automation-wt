import random

import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, Features, OrderType, WatchListTab
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.fixture(scope="package", autouse=True)
def setup_trade_test(login_member_site, web_app, symbol):
    logger.info(f"- Select symbol: {symbol!r}")
    web_app.home_page.watch_list.select_tab(WatchListTab.CRYPTO)
    web_app.home_page.watch_list.select_symbol(symbol)


@pytest.fixture
def create_order_data(web_app):
    def _handler(trade_object):
        tab_amount = web_app.trade_page.asset_tab.get_tab_amount(AssetTabs.get_tab(trade_object.order_type))

        logger.info(f"- POST {trade_object.trade_type.upper()} {trade_object.order_type.upper()} order")
        res = APIClient().trade.post_order(trade_object)

        logger.info("- Wait for tab amount to increase")
        web_app.trade_page.asset_tab.wait_for_tab_amount(AssetTabs.get_tab(trade_object.order_type), tab_amount + 1)

        return res

    return _handler


@pytest.fixture(scope="package")
def enabl_OCT(web_app):
    logger.info("- Send API to enable OCT")
    APIClient().user.patch_oct()


@pytest.fixture(scope="package")
def disable_OCT(web_app):
    logger.info("- Send API to disable OCT")
    APIClient().user.patch_oct(enable=False)


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


@pytest.fixture
def close_edit_confirmation(web_app):
    yield
    web_app.trade_page.modals.close_edit_confirm_modal()
