import random

import pytest

from src.data.enums import WatchListTab, Features
from src.utils.logging_utils import logger


def test(web, get_current_symbol):
    current_symbols = get_current_symbol()
    star_symbols = random.choices(current_symbols, k=4)

    logger.info(f"Step 1: Mark star for {star_symbols!r} from Markets Page")
    web.markets_page.watch_list.mark_star_symbols(star_symbols)

    logger.info("Verify symbols displayed in Favourites tab")
    web.markets_page.watch_list.verify_symbols_displayed(WatchListTab.FAVOURITES, star_symbols)

    logger.info("Step 2: Navigate to Trade Page")
    web.home_page.navigate_to(Features.TRADE)

    logger.info("Verify symbols displayed in Favourites tab - Market Page")
    web.trade_page.watch_list.verify_symbols_displayed(WatchListTab.FAVOURITES, star_symbols)

    logger.info(f"Step 3: Navigate to Markets Page & remove mark star for symbols: {star_symbols!r}")
    web.home_page.navigate_to(Features.MARKETS, wait=True)
    web.markets_page.watch_list.select_tab(WatchListTab.FAVOURITES)
    web.markets_page.watch_list.mark_unstar_symbols(star_symbols)

    logger.info("Verify symbols no longer displayed in tab")
    web.markets_page.watch_list.verify_symbols_displayed(WatchListTab.FAVOURITES, star_symbols, is_display=False)

    logger.info("Step 4: Navigate to Trade Page")
    web.home_page.navigate_to(Features.TRADE)

    logger.info("Verify symbols no longer displayed in Favourites tab - Market Page")
    web.trade_page.watch_list.verify_symbols_displayed(WatchListTab.FAVOURITES, star_symbols, is_display=False)


@pytest.fixture(autouse=True)
def setup_teardown(web):
    logger.info("- Navigate to Market Page")
    web.home_page.navigate_to(Features.MARKETS)

    logger.info("- Select Tab ALL")
    web.markets_page.watch_list.select_tab(WatchListTab.ALL)

    yield
    logger.info("- Navigate to Trade Page and remove stars all symbols")
    web.home_page.navigate_to(Features.TRADE)
    web.trade_page.watch_list.select_tab(WatchListTab.FAVOURITES)
    web.trade_page.watch_list.mark_unstar_symbols(all_symbols=True)
