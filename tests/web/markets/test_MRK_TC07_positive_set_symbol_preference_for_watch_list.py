import pytest

from src.data.enums import Features, WatchListTab
from src.data.ui_messages import UIMessages
from src.utils import DotDict
from src.utils.logging_utils import logger


def test(web, setup_test):
    store_dict = DotDict()
    tab = setup_test

    logger.info("Step 1: Navigate to Market Page")
    web.home_page.navigate_to(Features.MARKETS)

    logger.info(f"Step 2: Set symbol preference for tab: {tab}")
    web.markets_page.set_symbol_preference(tab, store_dict=store_dict)

    logger.info("Verify message saved success")
    web.home_page.notifications.verify_alert_success_message(UIMessages.ALL_CHANGES_SAVED)

    logger.info("Verify hidden symbols")
    web.markets_page.watch_list.verify_symbols_displayed(store_dict.hide, is_display=False)

    logger.info("Verify displayed symbol")
    web.markets_page.watch_list.verify_symbols_displayed(store_dict.show)


@pytest.fixture(autouse=True)
def setup_test(web):
    # tab = random.choice(WatchListTab.sub_tabs())
    tab = WatchListTab.CRYPTO
    yield tab

    logger.info("- Clean up test")
    web.home_page.navigate_to(Features.MARKETS)

    logger.info(f"- Set Show All for tab: {tab.capitalize()!r}")
    web.markets_page.set_symbol_preference(tab, show_all=True, unchecked=False)
