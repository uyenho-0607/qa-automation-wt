import pytest

from src.data.enums import Features, WatchListTab
from src.utils import DotDict
from src.utils.logging_utils import logger


def test(web, setup_test):
    watchlist_symbol = setup_test
    shares, forex, commodities, index, crypto, tab_all = WatchListTab.sub_tabs() + [WatchListTab.ALL]

    logger.info(f"Step 1: Select symbol from watchlist: {commodities.title()!r}")
    web.markets_page.watch_list.select_last_symbol(commodities)

    logger.info("Verify All Tab on Trade Page is selected")
    web.trade_page.watch_list.verify_tab_selected()

    logger.info(f"Verify symbol {watchlist_symbol[commodities]} is selected")
    web.trade_page.watch_list.verify_symbol_selected(watchlist_symbol[commodities])

    logger.info(f"Step 2: Select symbol from watchlist: {crypto.title()!r}")
    web.home_page.navigate_to(Features.MARKETS)
    web.markets_page.watch_list.select_last_symbol(crypto)

    logger.info("Verify All Tab on Trade Page is selected")
    web.trade_page.watch_list.verify_tab_selected()

    logger.info(f"Verify symbol {watchlist_symbol[crypto]} is selected")
    web.trade_page.watch_list.verify_symbol_selected(watchlist_symbol[crypto])

    logger.info(f"Step 3: Select symbol from watchlist: {forex.title()!r}")
    web.home_page.navigate_to(Features.MARKETS)
    web.markets_page.watch_list.select_last_symbol(forex)

    logger.info("Verify All Tab on Trade Page is selected")
    web.trade_page.watch_list.verify_tab_selected()

    logger.info(f"Verify symbol {watchlist_symbol[forex]} is selected")
    web.trade_page.watch_list.verify_symbol_selected(watchlist_symbol[forex])

    logger.info(f"Step 4: Select symbol from watchlist: {index.title()!r}")
    web.home_page.navigate_to(Features.MARKETS)
    web.markets_page.watch_list.select_last_symbol(index)

    logger.info("Verify All Tab on Trade Page is selected")
    web.trade_page.watch_list.verify_tab_selected()

    logger.info(f"Verify symbol {watchlist_symbol[index]} is selected")
    web.trade_page.watch_list.verify_symbol_selected(watchlist_symbol[index])

    logger.info(f"Step 5: Select symbol from watchlist: {tab_all.title()!r}")
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
