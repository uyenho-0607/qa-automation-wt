import pytest

from src.data.enums import Features, WatchListTab
from src.data.ui_messages import UIMessages
from src.utils import DotDict
from src.utils.logging_utils import logger


def test(android, setup_test):
    store_dict = DotDict()
    tab = setup_test

    logger.info("Step 1: Navigate to Market Page")
    android.home_screen.navigate_to(Features.MARKETS)

    logger.info(f"Step 2: Set symbol preference for tab: {tab}")
    android.markets_screen.set_symbol_preference(tab, store_dict=store_dict)

    logger.info("Verify message saved success")
    android.home_screen.notifications.verify_alert_message(UIMessages.ALL_CHANGES_SAVED)

    logger.info("Verify hidden symbols")
    android.markets_screen.verify_symbols_displayed(tab, store_dict.hide, is_display=False)

    logger.info("Verify displayed symbol")
    android.markets_screen.verify_symbols_displayed(tab, store_dict.show)


@pytest.fixture(autouse=True)
def setup_test(android):
    tab = WatchListTab.CRYPTO
    yield tab

    logger.info("- Clean up test")
    android.home_screen.navigate_to(Features.MARKETS)

    logger.info(f"- Set Show All for tab: {tab.capitalize()!r}")
    android.markets_screen.set_symbol_preference(tab, unchecked=False, show_all=True)

    logger.info("Verify message saved success")
    android.home_screen.notifications.verify_alert_message(UIMessages.ALL_CHANGES_SAVED)
