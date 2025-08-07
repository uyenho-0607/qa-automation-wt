import pytest

from src.apis.api_client import APIClient
from src.data.enums import WatchListTab
from src.utils.logging_utils import logger


def test(web):
    logger.info("Step 1: Refresh Page")
    web.home_page.refresh_page()

    logger.info(f"Verify {WatchListTab.TOP_GAINER.title()} is pre-selected by default")
    web.home_page.watch_list.verify_tab_selected(WatchListTab.TOP_GAINER)

    logger.info("Step 2: Mark Star symbol")
    web.home_page.watch_list.mark_star_symbols()
    web.home_page.refresh_page()

    logger.info(f"Verify {WatchListTab.FAVOURITES.title()} is pre-selected when having starred symbols")
    web.home_page.watch_list.verify_tab_selected(WatchListTab.FAVOURITES)

    logger.info("Step 3: Mark Unstar symbol in Favourites")
    web.home_page.watch_list.mark_unstar_symbols()
    web.home_page.refresh_page()

    logger.info(f"Verify pre-selected tab is {WatchListTab.TOP_GAINER.title()}")
    web.home_page.watch_list.verify_tab_selected(WatchListTab.TOP_GAINER)


@pytest.fixture(autouse=True)
def setup_test():
    logger.info("- Mark unstar all items if any")
    APIClient().market.delete_starred_symbols()
