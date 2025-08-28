import random

import pytest

from src.apis.api_client import APIClient
from src.data.enums import WatchListTab
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, setup_pre_selected_tab):
    selected_tab = setup_pre_selected_tab

    logger.info("Step 1: Login with valid userid and password")
    web.login_page.login()
    web.home_page.feature_announcement_modal.got_it()

    logger.info("Verify trade/ home page URL is correct")
    web.home_page.verify_page_url()

    logger.info("Verify account info is displayed")
    web.home_page.verify_account_info_displayed()

    logger.info(f"Verify pre-selected tab is {selected_tab.value!r}")
    web.trade_page.watch_list.verify_tab_selected(selected_tab)

    logger.info("Step 2: Select tab All")
    web.trade_page.watch_list.select_tab(WatchListTab.ALL)

    logger.info("Verify Watch List Tabs displayed in correct order")
    web.trade_page.watch_list.verify_tabs_displayed()


@pytest.fixture
def setup_pre_selected_tab(symbol):
    mark_star = bool(random.randint(0, 1))
    pre_selected_tab = WatchListTab.TOP_GAINER

    logger.info(f"{'=' * 10} Setup Test - Start {'=' * 10}")

    if mark_star:
        logger.info(f"- Send API request to mark star symbol: {symbol!r}")
        APIClient().market.post_starred_symbol(symbol)
        pre_selected_tab = WatchListTab.FAVOURITES

    else:
        logger.info("- Send API request to delete all starred symbols")
        APIClient().market.delete_starred_symbols()

    logger.info(f"- Setup Summary: pre-selected tab: {pre_selected_tab.value!r}")
    logger.info(f"{'=' * 10} Setup Test - Done {'=' * 10}")

    yield pre_selected_tab
