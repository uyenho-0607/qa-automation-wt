import pytest

from src.apis.api_client import APIClient
from src.data.consts import get_symbols
from src.data.enums import Features, WatchListTab
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize("tab", [WatchListTab.FAVOURITES, WatchListTab.ALL] + WatchListTab.sub_tabs())
def test(web_app, tab):
    logger.info("Step 1: Navigate to Markets Screen")
    web_app.home_page.navigate_to(Features.MARKETS)

    logger.info(f"Step 2: Select tab {tab}")
    web_app.markets_page.select_tab(tab, wait=True)

    logger.info(f"Step 3: Get random displaying symbol")
    select_symbol = web_app.markets_page.watch_list.get_random_symbol()

    logger.info(f"Step 4: Select symbol {select_symbol} from watchlist: {tab.title()!r}")
    web_app.markets_page.watch_list.select_symbol(select_symbol)

    logger.info(f"Verify symbol {select_symbol} is selected")
    web_app.trade_page.verify_symbol_overview_id(select_symbol)


@pytest.fixture(autouse=True)
def mark_symbol(tab, web_app):
    if tab == WatchListTab.FAVOURITES:
        for star_symbol in get_symbols():
            logger.info(f"- Mark star symbol: {star_symbol!r}")
            APIClient().market.post_starred_symbol(star_symbol)
    
    yield
    logger.info("- Navigate back to Market Screen")
    web_app.home_page.navigate_to(Features.MARKETS)

    if tab == WatchListTab.FAVOURITES:
        logger.info(f"- Delete all star symbols")
        APIClient().market.delete_starred_symbols()
