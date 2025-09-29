import random

import pytest

from src.apis.api_client import APIClient
from src.data.enums import WatchListTab, Features
from src.utils.logging_utils import logger


def test(web):
    current_symbols = web.home_page.watch_list.get_current_symbols(WatchListTab.ALL)
    star_symbols = random.sample(current_symbols, k=(5 if len(current_symbols) > 5 else len(current_symbols) - 1))

    logger.info(f"Step 1: Mark star for {star_symbols!r}")
    web.home_page.watch_list.mark_star_symbols(star_symbols)

    logger.info(f"Step 2: Select tab {WatchListTab.FAVOURITES.value!r}")
    web.home_page.watch_list.select_tab(WatchListTab.FAVOURITES)

    logger.info("Verify symbols displayed in Favourites tab")
    web.home_page.watch_list.verify_symbols_displayed(star_symbols)

    logger.info("Step 3: Navigate to Market Page")
    web.home_page.navigate_to(Features.MARKETS)

    logger.info(f"Step 4: Select tab {WatchListTab.FAVOURITES.value!r}")
    web.markets_page.watch_list.select_tab(WatchListTab.FAVOURITES)

    logger.info("Verify symbols displayed in Favourites tab - Market Page")
    web.markets_page.watch_list.verify_symbols_displayed(star_symbols)

    logger.info(f"Step 5: Navigate to Trade Page & remove star for symbols: {star_symbols!r}")
    web.home_page.navigate_to(Features.TRADE)
    web.home_page.watch_list.mark_unstar_symbols(star_symbols)

    logger.info(f"Step 6: Select tab {WatchListTab.FAVOURITES.value}")
    web.home_page.watch_list.select_tab(WatchListTab.ALL)
    web.home_page.watch_list.select_tab(WatchListTab.FAVOURITES)

    logger.info("Verify No items available message from trade page")
    web.home_page.watch_list.verify_empty_message()

    logger.info("Verify symbols no longer displayed in tab")
    web.home_page.watch_list.verify_symbols_displayed(symbols=star_symbols, is_display=False)

    logger.info(f"Step 7: Navigate to Market Page & select tab {WatchListTab.FAVOURITES.value}")
    web.home_page.navigate_to(Features.MARKETS)
    web.markets_page.watch_list.select_tab(WatchListTab.FAVOURITES)

    logger.info("Verify No items available message from market page")
    web.markets_page.watch_list.verify_empty_message()

    logger.info("Verify symbols no longer displayed in Favourites tab - Market Page")
    web.markets_page.watch_list.verify_symbols_displayed(symbols=star_symbols, is_display=False)


@pytest.fixture(autouse=True)
def remove_starred_symbols(web):
    yield
    logger.info("- Remove stars all symbols")
    APIClient().market.delete_starred_symbols()
