import time

import pytest

from src.apis.api_client import APIClient
from src.data.enums import OrderType, Features
from src.data.objects.symbol_obj import ObjSymbol
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(android, setup_order_data):
    symbols = setup_order_data

    logger.info("Step 1: Navigate to Asset Screen")
    android.home_screen.navigate_to(Features.ASSETS)

    logger.info(f"Verify symbols list displayed in My Trade are: {symbols[::-1]}")
    android.assets_screen.verify_my_trade_list(symbols[::-1])

    logger.info(f"Step 2: Place Pending Order for symbol: {symbols[-1]}")
    android.assets_screen.watch_list.select_last_symbol(tab=None)

    trade_obj = ObjTrade(symbol=symbols[-1], order_type=OrderType.LIMIT)
    android.trade_screen.place_order_panel.place_order(trade_obj, confirm=True, sl_type=None, tp_type=None)

    logger.info("Step 3: Navigate to Asset Screen")
    android.home_screen.navigate_to(Features.ASSETS, wait=True)

    logger.info("Verify displaying symbols are not changed")
    android.assets_screen.verify_my_trade_list(symbols[::-1])


@pytest.fixture
def setup_order_data(android):
    symbols = ObjSymbol(amount=5).get_symbol()
    logger.info(f"[Setup] Place 5 order for list symbol: {symbols}", setup=True)
    for _symbol in symbols:
        trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=_symbol)
        APIClient().trade.post_order(trade_object, update_price=False)
        time.sleep(1)

    logger.info(f"[Setup] Navigate to Home Page, last 5 symbols {', '.join(symbols[::-1])}", setup=True)
    android.assets_screen.navigate_to(Features.HOME)

    yield symbols
