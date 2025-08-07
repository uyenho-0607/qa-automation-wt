import pytest

from src.data.enums import OrderType, AssetTabs
from src.data.objects.trade_obj import ObjTrade


@pytest.fixture
def stop_limit_obj(symbol):
    def _handler(**kwargs):
        trade_object = ObjTrade(order_type=OrderType.STOP_LIMIT, symbol=symbol, **kwargs)
        return trade_object

    return _handler

@pytest.fixture(autouse=True, scope="package")
def select_tab(web):
    web.trade_page.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

