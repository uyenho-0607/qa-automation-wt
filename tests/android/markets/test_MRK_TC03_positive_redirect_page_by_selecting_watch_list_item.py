import pytest

from src.apis.api_client import APIClient
from src.data.enums import Features, WatchListTab
from src.data.objects.symbol_obj import ObjSymbol
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize("tab", [WatchListTab.FAVOURITES, WatchListTab.ALL] + WatchListTab.sub_tabs())
def test(android, tab):
    logger.info("Step 1: Navigate to Markets Screen")
    android.home_screen.navigate_to(Features.MARKETS)

    logger.info(f"Step 2: Select tab {tab}")
    android.markets_screen.select_tab(tab, wait=True)
    select_symbol = android.markets_screen.watch_list.get_random_symbol()

    logger.info(f"Step 3: Select symbol {select_symbol} from watchlist tab: {tab.title()!r}")
    android.markets_screen.watch_list.select_symbol(select_symbol)

    logger.info(f"Verify symbol {select_symbol} is selected in chart")
    android.trade_screen.chart.verify_symbol_selected(select_symbol)
    
@pytest.fixture(autouse=True)
def mark_star_symbol(tab, android):
    if tab == WatchListTab.FAVOURITES:

        logger.info(f"{'=' * 10} Setup Test - Start {'=' * 10}")
        logger.info("- Prepare starred symbols")
        for star_symbol in ObjSymbol().all_symbols[:3]:
            logger.info(f"[Setup] Mark star symbol: {star_symbol!r}", setup=True)
            APIClient().market.post_starred_symbol(star_symbol)

        logger.info(f"{'=' * 10} Setup Test - Done {'=' * 10}")

    yield

    logger.info("[Cleanup] Navigate back to Market Screen", teardown=True)
    android.home_screen.navigate_to(Features.MARKETS)

    if tab == WatchListTab.FAVOURITES:
        logger.info(f"[Cleanup] Delete all star symbols", teardown=True)
        APIClient().market.delete_starred_symbols()
