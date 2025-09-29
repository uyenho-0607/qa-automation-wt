import pytest

from src.apis.api_client import APIClient
from src.data.enums import Features, WatchListTab
from src.data.objects.symbol_obj import ObjSymbol
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

    logger.info(f"Step 4: Select symbol {select_symbol} from watchlist tab: {tab.title()!r}")
    web_app.markets_page.watch_list.select_symbol(select_symbol)

    logger.info(f"Verify symbol {select_symbol} is selected in chart")
    web_app.trade_page.verify_symbol_overview_id(select_symbol)


@pytest.fixture(autouse=True)
def mark_star_symbol(tab, web_app):
    if tab == WatchListTab.FAVOURITES:

        logger.info(f"{'=' * 10} Setup Test - Start {'=' * 10}")
        logger.info("- Prepare starred symbols")

        for star_symbol in ObjSymbol().all_symbols[:3]:
            logger.info(f"> Mark star symbol: {star_symbol!r}")
            APIClient().market.post_starred_symbol(star_symbol)

        logger.info(f"{'=' * 10} Setup Test - Done {'=' * 10}")

    yield

    logger.info("[Cleanup] Navigate back to Market Screen")
    web_app.home_page.navigate_to(Features.MARKETS)

    if tab == WatchListTab.FAVOURITES:
        logger.info(f"[Cleanup] Delete all star symbols")
        APIClient().market.delete_starred_symbols()
