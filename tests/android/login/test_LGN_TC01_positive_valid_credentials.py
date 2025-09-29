import random

import pytest

from src.apis.api_client import APIClient
from src.data.enums import WatchListTab
from src.data.objects.symbol_obj import ObjSymbol
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(android, setup_pre_selected_tab):
    selected_tab, symbols = setup_pre_selected_tab

    logger.info("Step 1: Login with valid userid and password")
    android.login_screen.login()
    android.home_screen.feature_anm_modal.got_it()

    logger.info("Verify account info is displayed")
    android.home_screen.verify_account_info_displayed()

    logger.info(f"Verify pre-selected tab is {selected_tab.value!r}")
    android.home_screen.watch_list.verify_symbols_list(symbols)

    logger.info("Step 2: User tries to logout")
    android.home_screen.settings.logout()

    logger.info("Verify login account tabs is displayed")
    android.login_screen.verify_account_tab_is_displayed()


@pytest.fixture(autouse=True)
def setup_pre_selected_tab():
    mark_star = bool(random.randint(0, 1))
    pre_select_tab = WatchListTab.FAVOURITES if mark_star else WatchListTab.TOP_GAINER

    logger.info(f"- Mark star: {mark_star!r}")
    if mark_star:
        logger.info("- Mark star symbol")
        APIClient().market.post_starred_symbol(random.choice(ObjSymbol().all_symbols))

    else:
        logger.info("- Delete all stared symbols")
        APIClient().market.delete_starred_symbols()

    display_symbols = APIClient().market.get_watchlist_items(pre_select_tab, get_symbols=True)
    yield pre_select_tab, display_symbols
