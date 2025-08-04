import pytest

from src.data.enums import Features, WatchListTab
from src.utils import DotDict
from src.utils.logging_utils import logger


def test(web_app, setup_test):
    watchlist_symbol = setup_test
    all, fav, top_picks, top_gainer, top_loser = WatchListTab.parent_tabs()

    logger.info(f"Step 1: Select symbol from watchlist: {all.title()!r}")
    web_app.markets_page.watch_list.select_last_symbol(all)

    logger.info(f"Verify symbol {watchlist_symbol[all]} is displayed in Trade screen")
    web_app.trade_page.watch_list.verify_symbol_selected(watchlist_symbol[all])

    logger.info(f"Step 2: Select symbol from watchlist: {fav.title()!r}")
    web_app.home_page.navigate_to(Features.HOME)
    web_app.markets_page.watch_list.select_last_symbol(fav)

    logger.info(f"Verify symbol {watchlist_symbol[fav]} is displayed in Trade screen")
    web_app.trade_page.watch_list.verify_symbol_selected(watchlist_symbol[fav])

    logger.info(f"Step 3: Select symbol from watchlist: {top_picks.title()!r}")
    web_app.home_page.navigate_to(Features.HOME)
    web_app.markets_page.watch_list.select_last_symbol(top_picks)

    logger.info(f"Verify symbol {watchlist_symbol[top_picks]} is displayed in Trade screen")
    web_app.trade_page.watch_list.verify_symbol_selected(watchlist_symbol[top_picks])

    logger.info(f"Step 4: Select symbol from watchlist: {top_gainer.title()!r}")
    web_app.home_page.navigate_to(Features.HOME)
    web_app.markets_page.watch_list.select_last_symbol(top_gainer)

    logger.info(f"Verify symbol {watchlist_symbol[top_gainer]} is displayed in Trade screen")
    web_app.trade_page.watch_list.verify_symbol_selected(watchlist_symbol[top_gainer])

    logger.info(f"Step 5: Select symbol from watchlist: {top_loser.title()!r}")
    web_app.home_page.navigate_to(Features.HOME)
    web_app.markets_page.watch_list.select_last_symbol(top_loser)

    logger.info(f"Verify symbol {watchlist_symbol[top_loser]} is displayed in Trade screen")
    web_app.trade_page.watch_list.verify_symbol_selected(watchlist_symbol[top_loser])


@pytest.fixture
def setup_test(web_app):
    
    watchlist_tabs = WatchListTab.parent_tabs()

    watchlist_symbol = DotDict()

    logger.info("- Get watchlist symbol for each tab")
    web_app.markets_page.watch_list.get_last_symbol(watchlist_tabs, store_data=watchlist_symbol)

    yield watchlist_symbol

