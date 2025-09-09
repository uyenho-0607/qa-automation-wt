import pytest

from src.data.enums import OrderType
from src.data.objects.trade_obj import ObjTrade


@pytest.fixture
def market_obj(symbol):
    def _handler(**kwargs):
        trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol, **kwargs)
        return trade_object

    return _handler


@pytest.fixture(scope="package", autouse=True)
def disable_OCT(disable_OCT):
    pass