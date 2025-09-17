from contextlib import suppress

import pytest

from src.data.consts import SHORT_WAIT
from src.data.enums import OrderType, SLTPType, Expiry
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.fixture(scope="package", autouse=True)
def setup_trade_test(login_wt_app, symbol, ios):
    logger.info(f"- Search and select symbol: {symbol!r}", setup=True)
    ios.home_screen.search_and_select_symbol(symbol)


@pytest.fixture
def market_obj(symbol):
    def _handler(**kwargs):
        trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol, **kwargs)
        return trade_object

    return _handler


@pytest.fixture
def limit_obj(symbol):
    def _handler(**kwargs):
        expiry = kwargs.pop('expiry', Expiry.random_values(except_val=[Expiry.SPECIFIED_DATE, Expiry.SPECIFIED_DATE_TIME]))
        trade_object = ObjTrade(order_type=OrderType.LIMIT, symbol=symbol, expiry=expiry, **kwargs)
        return trade_object

    return _handler


@pytest.fixture
def stop_obj(symbol):
    def _handler(**kwargs):
        expiry = kwargs.pop('expiry', Expiry.random_values(except_val=[Expiry.SPECIFIED_DATE, Expiry.SPECIFIED_DATE_TIME]))
        trade_object = ObjTrade(order_type=OrderType.STOP, symbol=symbol, expiry=expiry, **kwargs)
        return trade_object

    return _handler


@pytest.fixture
def stop_limit_obj(symbol):
    def _handler(**kwargs):
        expiry = kwargs.pop('expiry', Expiry.random_values(except_val=[Expiry.SPECIFIED_DATE, Expiry.SPECIFIED_DATE_TIME]))
        trade_object = ObjTrade(order_type=OrderType.STOP_LIMIT, symbol=symbol, expiry=expiry, **kwargs)
        return trade_object

    return _handler

@pytest.fixture(name="order_data")
def prepare_place_order(ios, market_obj):
    def handler(trade_object, sl_type: SLTPType = SLTPType.PRICE, tp_type: SLTPType = SLTPType.PRICE):
        ios.trade_screen.place_order_panel.place_order(trade_object, sl_type, tp_type)

    return handler


@pytest.fixture
def cancel_all(ios):
    yield
    logger.info("[Cleanup] Click cancel button (if any)", teardown=True)
    with suppress(Exception):
        ios.trade_screen.click_cancel_btn(timeout=SHORT_WAIT)
