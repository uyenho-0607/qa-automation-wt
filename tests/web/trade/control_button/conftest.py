import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, OrderType
from src.data.objects.trade_obj import ObjTrade
from src.utils import DotDict
from src.utils.logging_utils import logger


@pytest.fixture
def setup_close_position_test(web, get_asset_tab_amount, symbol):
    tab_amount = get_asset_tab_amount(OrderType.MARKET)
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)

    logger.info("- Get Min volume value")
    min_vol = web.trade_page.place_order_panel.get_min_volume()

    if not tab_amount:
        logger.info("- Place new order")
        APIClient().trade.post_order(trade_object, update_price=False)

        logger.info("- Wait for asset tab amount increase")
        web.trade_page.asset_tab.wait_for_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    web.trade_page.asset_tab.get_item_data(AssetTabs.OPEN_POSITION, trade_object=trade_object)
    max_vol = trade_object.get("volume", 0)
    order_id = trade_object.get("order_id", 0)

    yield DotDict(
        tab_amount=tab_amount or 1,
        min_vol=min_vol,
        max_vol=max_vol,
        order_id=order_id
    )
