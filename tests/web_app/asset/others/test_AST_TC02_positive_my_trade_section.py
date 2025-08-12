import random
import time

import pytest

from src.apis.api_client import APIClient
from src.data.enums import OrderType, Features
from src.data.objects.symbol_obj import ObjSymbol
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web_app, setup_order_data):

    symbols = setup_order_data

    logger.info("Step 1: Navigate to Asset Screen")
    web_app.home_page.navigate_to(Features.ASSETS, wait=True)

    logger.info(f"Verify symbols list displayed in My Trade are: {symbols[::-1]}")
    web_app.assets_page.verify_mytrade_items(symbols[::-1])

    logger.info(f"Step 3: Select symbol {symbols[-1]!r}")
    web_app.assets_page.watch_list.select_last_symbol()
    trade_obj = ObjTrade(symbol=symbols[-1], order_type=random.choice(OrderType.pending()))

    logger.info(f"Step 4: Place {trade_obj.order_type.upper()!r} Order")
    web_app.trade_page.place_order_panel.place_order(trade_obj, submit=True, sl_type=None, tp_type=None)

    logger.info("Step 5: Navigate to Asset Screen")
    web_app.home_page.navigate_to(Features.ASSETS, wait=True)

    logger.info("Verify displaying symbols are not changed")
    web_app.assets_page.verify_mytrade_items(symbols[::-1])


@pytest.fixture
def setup_order_data(web_app):

    symbols = random.choices(ObjSymbol().get_symbols(get_all=True), k=5)
    logger.info(f"- Place 5 order for list symbol: {symbols}")
    for _symbol in symbols:
        trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=_symbol)
        APIClient().trade.post_order(trade_object, update_price=False)
        time.sleep(1)

    logger.info("- Navigate to Home Page")
    web_app.assets_page.navigate_to(Features.HOME)

    yield symbols