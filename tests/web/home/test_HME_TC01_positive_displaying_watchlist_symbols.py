import time

import pytest

from src.apis.api_client import APIClient
from src.data.consts import SYMBOLS
from src.data.enums import WatchListTab
from src.data.project_info import ProjectConfig
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize("tab", WatchListTab.list_values())
def test(web, tab, setup_test):
    exp_symbols = setup_test(tab)

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

    logger.info(f"Verify current tab displays {len(exp_symbols)} symbols")
    web.trade_page.watch_list.verify_symbols_list(tab, exp_symbols)


@pytest.fixture
def setup_test():
    def _handler(tab):

        logger.info(f"- Get symbols should be displayed in tab: {tab}")
        symbols = APIClient().market.get_watchlist_items(tab, get_symbols=True)

        if not symbols and tab == WatchListTab.FAVOURITES:
            for symbol in SYMBOLS[ProjectConfig.client][:3]:
                APIClient().market.post_starred_symbol(symbol)
            symbols = SYMBOLS[ProjectConfig.client][:3]

        return symbols

    return _handler


@pytest.fixture(autouse=True)
def cleanup(tab):
    yield
    if tab == WatchListTab.FAVOURITES:
        APIClient().market.delete_starred_symbols()
