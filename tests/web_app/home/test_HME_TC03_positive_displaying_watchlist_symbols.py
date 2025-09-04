import random

import pytest

from src.apis.api_client import APIClient
from src.data.enums import WatchListTab, Features
from src.data.objects.symbol_obj import ObjSymbol
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize("tab", WatchListTab.list_values(except_val=WatchListTab.ALL))
def test(web_app, tab, setup_test):
    exp_symbols = setup_test(tab)

    if not exp_symbols:
        pytest.skip("No symbols to test")

    logger.info("Step 1: Navigate to Home Page")
    web_app.trade_page.navigate_to(Features.HOME, wait=True)

    logger.info(f"Step 2: Select tab: {tab.value.title()}")
    web_app.home_page.watch_list.select_tab(tab, wait=True)

    logger.info(f"Verify current tab displays {len(exp_symbols)} symbols: {', '.join(exp_symbols)}")
    web_app.home_page.watch_list.verify_symbols_list(exp_symbols)

    logger.info("Step 3: Get random displaying symbol")
    select_symbol = web_app.home_page.watch_list.get_random_symbol()

    logger.info(f"Step 4: Select {select_symbol!r}")
    web_app.home_page.watch_list.select_symbol(select_symbol)

    logger.info("Verify symbol is selected")
    web_app.trade_page.verify_symbol_overview_id(select_symbol)


@pytest.fixture
def setup_test(web_app):
    def _handler(tab):

        logger.info(f"{'=' * 10} Setup Test - Start {'=' * 10}")

        if tab != WatchListTab.FAVOURITES:
            logger.info(f"- Get symbols should be displayed in tab: {tab}")
            symbols = APIClient().market.get_watchlist_items(tab, get_symbols=True)

            # Filter and sample symbols to avoid excessive scrolling
            if symbols and len(symbols) > 10:
                # filter out symbols placed at the end of the list
                filtered_symbol = [sym for sym in symbols if not any(sym.startswith(letter) for letter in ['U', 'V', 'W', 'X', 'Y', 'Z'])]
                if filtered_symbol:
                    symbols = filtered_symbol

            symbols = random.sample(symbols, 10) if len(symbols) >= 10 else symbols

        else:

            logger.info(f"- Prepare starred symbols for checking tab {WatchListTab.FAVOURITES.value!r}")
            symbols = ObjSymbol().get_symbols(get_all=True)
            _list_symbol = random.sample(symbols, 10) if len(symbols) >= 10 else symbols

            for symbol in _list_symbol:
                logger.info(f"- Mark star symbol: {symbol!r}")
                APIClient().market.post_starred_symbol(symbol)

            symbols = _list_symbol
            web_app.home_page.refresh_page()

        logger.info(f">> Setup Summary: List symbols should be displayed in tab: {tab.value!r} - {', '.join(symbols)!r}")
        logger.info(f"{'=' * 10} Setup Test - Done {'=' * 10}")

        return symbols

    return _handler


@pytest.fixture(autouse=True)
def cleanup(tab):
    yield
    if tab == WatchListTab.FAVOURITES:
        logger.info(f"[Cleanup] Delete all star symbols")
        APIClient().market.delete_starred_symbols()
