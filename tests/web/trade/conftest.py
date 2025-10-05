import random

import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, OrderType, SLTPType
from src.data.enums import Features
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.fixture(scope="package", autouse=True)
def setup_trade_test(login_member_site, web, symbol):
    logger.info(f"{'=' * 10} Setup Trade Package - Start {'=' * 10}")

    logger.info("- Navigate to Trade Page", setup=True)
    web.home_page.navigate_to(Features.TRADE)

    logger.info(f"- Search and select symbol: {symbol}", setup=True)
    web.home_page.search_and_select_symbol(symbol)

    logger.info(f"{'=' * 10} Setup Trade Package - Done {'=' * 10}")


@pytest.fixture
def market_obj(symbol):
    def _handler(**kwargs):
        trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol, **kwargs)
        return trade_object

    return _handler


@pytest.fixture
def limit_obj(symbol):
    def _handler(**kwargs):
        trade_object = ObjTrade(order_type=OrderType.LIMIT, symbol=symbol, **kwargs)
        return trade_object

    return _handler


@pytest.fixture
def stop_obj(symbol):
    def _handler(**kwargs):
        trade_object = ObjTrade(order_type=OrderType.STOP, symbol=symbol, **kwargs)
        return trade_object

    return _handler


@pytest.fixture
def stop_limit_obj(symbol):
    def _handler(**kwargs):
        trade_object = ObjTrade(order_type=OrderType.STOP_LIMIT, symbol=symbol, **kwargs)
        return trade_object

    return _handler


@pytest.fixture(name="order_data")
def prepare_place_order(web):
    def handler(trade_object, sl_type=SLTPType.PRICE, tp_type=SLTPType.PRICE, confirm=True, close_banner=True):
        web.trade_page.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type, submit=confirm)

        # clear noti banner
        if close_banner:
            web.home_page.notifications.close_noti_banner()

    return handler


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
