import pytest

from src.data.enums import OrderType
from src.data.objects.trade_obj import ObjTrade


@pytest.fixture
def limit_obj(symbol):
    def _handler(**kwargs):
        trade_object = ObjTrade(order_type=OrderType.LIMIT, symbol=symbol, **kwargs)
        return trade_object

    return _handler