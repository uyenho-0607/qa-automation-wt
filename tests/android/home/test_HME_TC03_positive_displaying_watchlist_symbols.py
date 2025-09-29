import pytest

from src.apis.api_client import APIClient
from src.data.enums import WatchListTab, Features
from src.data.objects.symbol_obj import ObjSymbol
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize("tab", WatchListTab.list_values(except_val=WatchListTab.ALL))
def test(android, tab, setup_test):
    exp_symbols = setup_test(tab)

    logger.info(f"Step 1: Select tab {tab.value}")
    android.trade_screen.watch_list.select_tab(tab)

    logger.info(f"Verify current tab displays {len(exp_symbols)} symbols")
    android.trade_screen.watch_list.verify_symbols_list(symbols=exp_symbols)

    logger.info("Step 2: Get random symbol to select")
    select_symbol = android.trade_screen.watch_list.get_current_symbols(random_symbol=True)

    logger.info(f"Step 3: Select {select_symbol!r}")
    android.trade_screen.watch_list.select_symbol(select_symbol)

    logger.info("Verify symbol is selected")
    android.trade_screen.watch_list.verify_symbol_selected(select_symbol)


@pytest.fixture
def setup_test():
    def _handler(tab):

        logger.info(f"- Get symbols should be displayed in tab: {tab}")
        symbols = APIClient().market.get_watchlist_items(tab, get_symbols=True)

        if not symbols and tab == WatchListTab.FAVOURITES:
            _list_symbol = ObjSymbol().all_symbols[:3]

            for symbol in _list_symbol:
                logger.info(f"- Mark star symbol: {symbol!r}")
                APIClient().market.post_starred_symbol(symbol)

            symbols = _list_symbol

        return symbols

    return _handler


@pytest.fixture(autouse=True)
def cleanup(tab, android):
    yield

    logger.info("- Navigate back to Home Screen")
    android.trade_screen.navigate_to(Features.HOME)

    if tab == WatchListTab.FAVOURITES:
        logger.info(f"- Delete all star symbols")
        APIClient().market.delete_starred_symbols()
