import random
import time

import pytest

from src.apis.api_client import APIClient
from src.data.enums import Features, WatchListTab
from src.data.objects.symbol_obj import ObjSymbol
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(android):
    """Test symbol selection from each available watchlist subtab."""
    tabs = [WatchListTab.FAVOURITES] + WatchListTab.sub_tabs() + [WatchListTab.ALL]

    logger.info("Step 1: Navigate to Markets Screen")
    android.home_screen.navigate_to(Features.MARKETS)

    for i, subtab in enumerate(tabs):

        logger.info(f"Step {i + 1}: Select tab {subtab}")
        android.markets_screen.select_tab(subtab)
        time.sleep(2)  # wait a bit for loading symbols

        logger.info(f"Step {i + 2}: Get random displaying symbol")
        select_symbol = android.markets_screen.watch_list.get_current_symbols(random_symbol=True)

        logger.info(f"Step {i + 3}: Select symbol {select_symbol} from watchlist: {subtab.title()!r}")
        android.markets_screen.watch_list.select_symbol(select_symbol)

        logger.info(f"Verify symbol {select_symbol} is selected")
        android.trade_screen.watch_list.verify_symbol_selected(select_symbol)

        if subtab != tabs[-1]:
            logger.info(f"Step {i + 4}: Navigate to Markets Screen")
            android.home_screen.navigate_to(Features.MARKETS)


@pytest.fixture(autouse=True)
def mark_symbol():
    star_symbol = random.choice(ObjSymbol().get_symbols(get_all=True))
    logger.info(f"- Mark star symbol: {star_symbol!r}")
    APIClient().market.post_starred_symbol(star_symbol)

    yield

    logger.info(f"- Delete all star symbols")
    APIClient().market.delete_starred_symbols()
