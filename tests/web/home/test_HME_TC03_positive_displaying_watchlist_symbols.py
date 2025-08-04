import random
import time

import pytest

from src.apis.api_client import APIClient
from src.data.enums import WatchListTab
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize("tab", WatchListTab.list_values(except_val=WatchListTab.ALL))
def test(web, tab, setup_test):
    exp_symbols = setup_test(tab)
    if not exp_symbols:
        pytest.skip("No symbols to test")

    logger.info("Step 1: Get random displaying symbol")
    web.home_page.watch_list.select_tab(tab)
    time.sleep(2)
    select_symbol = web.home_page.watch_list.get_random_symbol()

    logger.info(f"Step 2: Select {select_symbol!r}")
    web.home_page.watch_list.select_symbol(select_symbol)

    logger.info("Verify symbol is selected")
    web.home_page.watch_list.verify_symbol_selected(select_symbol)

    logger.info("Verify symbol displayed in chart")
    web.trade_page.chart.verify_symbol_selected(select_symbol)

    logger.info(f"Verify current tab displays {len(exp_symbols)} symbols: {', '.join(exp_symbols)}")
    web.trade_page.watch_list.verify_symbols_list(tab, exp_symbols)


@pytest.fixture
def setup_test():
    def _handler(tab):

        if tab != WatchListTab.FAVOURITES:
            logger.info(f"- Get symbols should be displayed in tab: {tab}")
            symbols = APIClient().market.get_watchlist_items(tab, get_symbols=True)

            # Filter and sample symbols to avoid excessive scrolling
            if symbols and len(symbols) > 50:
                # Filter out symbols starting with letters that are at the end of alphabet to avoid long scrolling times
                problematic_letters = ['U', 'V', 'W', 'X', 'Y', 'Z']
                filtered_symbols = [sym for sym in symbols if not any(sym.startswith(letter) for letter in problematic_letters)]

                # If we have enough filtered symbols, use them; otherwise fall back to original
                if len(filtered_symbols) >= 10:
                    logger.info(f"- Filtered out symbols starting with {problematic_letters} to avoid scrolling issues")
                    symbols = filtered_symbols

                # Sample a reasonable number of symbols for testing (max 15)
                symbols = random.sample(symbols, 10)

        else:
            symbols = APIClient().market.get_watchlist_items(WatchListTab.ALL, get_symbols=True)
            _list_symbol = random.sample(symbols, 10) if len(symbols) >= 10 else symbols
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
