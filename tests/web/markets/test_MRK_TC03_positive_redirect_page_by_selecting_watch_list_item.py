import pytest

from src.data.enums import Features, WatchListTab
from src.utils import DotDict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, setup_test):
    watchlist_symbol = setup_test
    subtabs = WatchListTab.sub_tabs()
    tab_all = WatchListTab.ALL

    # Test each available subtab dynamically
    for i, subtab in enumerate(subtabs, 1):
        logger.info(f"Step {i}: Select symbol from watchlist: {subtab.title()!r}")
        web.markets_page.watch_list.select_last_symbol(subtab)

        logger.info("Verify All Tab on Trade Page is selected")
        web.trade_page.watch_list.verify_tab_selected()

        logger.info(f"Verify symbol {watchlist_symbol[subtab]} is selected")
        web.trade_page.watch_list.verify_symbol_selected(watchlist_symbol[subtab])

        # Navigate back to markets page for next iteration (except for the last one)
        if i < len(subtabs):
            web.home_page.navigate_to(Features.MARKETS)

    # Test the "All" tab
    logger.info(f"Step {len(subtabs) + 1}: Select symbol from watchlist: {tab_all.title()!r}")
    web.home_page.navigate_to(Features.MARKETS)
    web.markets_page.watch_list.select_last_symbol()

    logger.info("Verify All Tab on Trade Page is selected")
    web.trade_page.watch_list.verify_tab_selected()

    logger.info(f"Verify symbol {watchlist_symbol[tab_all]} is selected")
    web.trade_page.watch_list.verify_symbol_selected(watchlist_symbol[tab_all])


@pytest.fixture
def setup_test(web):
    watchlist_tabs = WatchListTab.sub_tabs() + [WatchListTab.ALL]
    watchlist_symbol = DotDict()

    logger.info("- Navigate to Market Page")
    web.home_page.navigate_to(Features.MARKETS)

    logger.info("- Get watchlist symbol for each tab")
    web.markets_page.watch_list.get_last_symbol(watchlist_tabs, store_data=watchlist_symbol)

    yield watchlist_symbol
