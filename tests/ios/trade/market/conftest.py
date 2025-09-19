import pytest

from src.data.enums import OrderType, SLTPType
from src.data.objects.trade_obj import ObjTrade


@pytest.fixture
def market_obj(symbol):
    def _handler(**kwargs):
        trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol, **kwargs)
        return trade_object

    return _handler


@pytest.fixture(name="order_data")
def prepare_place_order(ios, market_obj):
    def handler(trade_object, sl_type: SLTPType = SLTPType.PRICE, tp_type: SLTPType = SLTPType.PRICE):
        ios.trade_screen.place_order_panel.place_order(trade_object, sl_type, tp_type)

    return handler
