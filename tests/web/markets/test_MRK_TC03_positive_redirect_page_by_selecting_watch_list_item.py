import random

import pytest

from src.apis.api_client import APIClient
from src.data.enums import Features, WatchListTab
from src.utils import DotDict
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize("check_tab", WatchListTab.sub_tabs() + [WatchListTab.ALL, WatchListTab.FAVOURITES])
def test(web, setup_test, check_tab):
    watchlist_symbol = setup_test
    select_symbol = random.choice(watchlist_symbol[check_tab])

    logger.info("Step 1: Navigate to Market Page")
    web.home_page.navigate_to(Features.MARKETS, wait=True)

    logger.info(f"Step 2: Select symbol: {select_symbol!r} from watchlist: {check_tab.title()!r}")
    web.markets_page.watch_list.select_symbol(select_symbol, tab=check_tab)

    logger.info("Verify page is redirected to Trade Page")
    web.trade_page.verify_page_url()

    logger.info(f"Verify Tab ALL on Trade Page is selected")
    web.trade_page.watch_list.verify_tab_selected(WatchListTab.ALL)

    logger.info(f"Verify symbol {select_symbol} is selected")
    web.trade_page.watch_list.verify_symbol_selected(select_symbol)

    logger.info("Verify symbol is displayed on chart")
    web.trade_page.chart.verify_symbol_selected(select_symbol)


@pytest.fixture(scope="module")
def setup_test(web):
    watchlist_tabs = WatchListTab.sub_tabs() + [WatchListTab.ALL, WatchListTab.FAVOURITES]
    watchlist_symbol = DotDict()

    logger.info("- Navigate to Market Page")
    web.home_page.navigate_to(Features.MARKETS, wait=True)

    logger.info("- POST starred symbols")
    symbols = web.markets_page.watch_list.get_current_symbols()
    for _symbol in symbols[:5]:
        APIClient().market.post_starred_symbol(_symbol)

    for tab in watchlist_tabs:
        logger.info(f"- Get watchlist symbol from tab: {tab!r}")
        watchlist_symbol[tab] = web.markets_page.watch_list.get_current_symbols(tab)

    yield watchlist_symbol
