import random

import pytest

from src.data.enums import SignalTab
from src.utils.logging_utils import logger


def test(web, get_current_symbol):
    current_symbols = get_current_symbol()
    amount = 5 if len(current_symbols) > 5 else round(len(current_symbols) / 2)
    star_symbols = random.choices(current_symbols, k=amount)

    logger.info(f"Step 1: Mark star for {star_symbols!r}")
    web.signal_page.mark_star_symbols(star_symbols)

    logger.info("Verify symbols displayed in Favourites tab")
    web.signal_page.verify_symbol_displayed_in_tab(SignalTab.FAVOURITE, star_symbols)

    logger.info(f"Step 2: Remove mark star for symbols: {star_symbols!r}")
    web.signal_page.mark_unstar_symbols(star_symbols)

    logger.info("Verify symbols no longer displayed in tab")
    web.signal_page.verify_symbol_displayed_in_tab(SignalTab.FAVOURITE, star_symbols, is_display=False)


@pytest.fixture(autouse=True)
def cleanup(web):
    yield
    logger.info("- Remove stars all symbols")
    web.signal_page.select_tab(SignalTab.FAVOURITE)
    web.signal_page.mark_unstar_symbols(all_symbols=True)
