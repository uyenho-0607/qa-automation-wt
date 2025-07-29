import random
import time

import pytest

from src.apis.api_client import APIClient
from src.data.consts import get_symbols
from src.data.enums import WatchListTab
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize("tab", WatchListTab.list_values(except_val=WatchListTab.ALL))
def test(web, tab, setup_test):
    exp_symbols = setup_test(tab)
    if not exp_symbols:
        pytest.skip("No symbols to test")

    logger.info("Step 1: Get random displaying symbol")
    web.trade_page.watch_list.select_tab(tab)
    time.sleep(2)
    select_symbol = web.trade_page.watch_list.get_random_symbol()

    logger.info(f"Step 2: Select {select_symbol!r}")
    web.trade_page.watch_list.select_symbol(select_symbol)

    logger.info("Verify symbol is selected")
    web.trade_page.watch_list.verify_symbol_selected(select_symbol)

    logger.info("Verify symbol displayed in chart")
    web.trade_page.chart.verify_symbol_selected(select_symbol)

    logger.info(f"Verify current tab displays {len(exp_symbols)} symbols: {', '.join(exp_symbols)}")
    web.trade_page.watch_list.verify_symbols_list(tab, exp_symbols)


@pytest.fixture
def setup_test():
    def _handler(tab):

        logger.info(f"- Get symbols should be displayed in tab: {tab}")
        symbols = APIClient().market.get_watchlist_items(tab, get_symbols=True)
        symbols = random.sample(symbols, 10) if len(symbols) >= 10 else symbols

        if not symbols and tab == WatchListTab.FAVOURITES:
            _list_symbol = get_symbols()[:3]
            for symbol in _list_symbol:
                logger.info(f"- Mark star symbol: {symbol!r}")
                APIClient().market.post_starred_symbol(symbol)

            symbols = _list_symbol

        return symbols

    return _handler


@pytest.fixture(autouse=True)
def cleanup(tab):
    yield
    if tab == WatchListTab.FAVOURITES:
        logger.info(f"- Delete all star symbols")
        APIClient().market.delete_starred_symbols()
