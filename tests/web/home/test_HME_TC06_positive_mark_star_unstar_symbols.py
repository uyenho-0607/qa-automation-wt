import random
import time

import pytest

from src.apis.api_client import APIClient
from src.data.enums import WatchListTab, Features
from src.utils.logging_utils import logger


def test(web, get_current_symbol):
    current_symbols = get_current_symbol()
    star_symbols = random.sample(current_symbols, k=(5 if len(current_symbols) > 5 else len(current_symbols) - 1))

    logger.info(f"Step 1: Mark star for {star_symbols!r}")
    web.trade_page.watch_list.mark_star_symbols(star_symbols)

    logger.info("Verify symbols displayed in Favourites tab")
    web.trade_page.watch_list.verify_symbols_displayed(WatchListTab.FAVOURITES, star_symbols)

    logger.info("Step 2: Navigate to Market Page")
    web.home_page.navigate_to(Features.MARKETS)

    logger.info("Verify symbols displayed in Favourites tab - Market Page")
    web.markets_page.watch_list.verify_symbols_displayed(WatchListTab.FAVOURITES, star_symbols)

    logger.info(f"Step 3: Navigate to Trade Page & remove mark star for symbols: {star_symbols!r}")
    web.home_page.navigate_to(Features.TRADE)
    web.trade_page.watch_list.mark_unstar_symbols(star_symbols)
    web.trade_page.watch_list.select_tab(WatchListTab.ALL)

    logger.info("Verify No items available message from trade page")
    web.trade_page.watch_list.select_tab(WatchListTab.FAVOURITES)
    web.trade_page.watch_list.verify_empty_message()

    logger.info("Verify symbols no longer displayed in tab")
    web.trade_page.watch_list.verify_symbols_displayed(symbols=star_symbols, is_display=False)

    logger.info("Step 4: Navigate to Market Page")
    web.home_page.navigate_to(Features.MARKETS)

    logger.info("Verify No items available message from market page")
    web.markets_page.watch_list.select_tab(WatchListTab.FAVOURITES)
    web.markets_page.watch_list.verify_empty_message()

    logger.info("Verify symbols no longer displayed in Favourites tab - Market Page")
    web.markets_page.watch_list.verify_symbols_displayed(symbols=star_symbols, is_display=False)


@pytest.fixture(autouse=True)
def remove_starred_symbols(web):
    yield
    logger.info("- Remove stars all symbols")
    APIClient().market.delete_starred_symbols()
