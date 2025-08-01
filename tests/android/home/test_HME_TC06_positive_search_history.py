import random

import pytest

from src.data.consts import get_symbols
from src.utils.logging_utils import logger


def test(android):
    symbol_list = random.sample(get_symbols(), k=2)

    for index, symbol_name in enumerate(symbol_list):
        logger.info(f"Step {index + 1}: Search and select symbol: {symbol_name!r}")
        android.home_screen.search_and_select_symbol(symbol_name)

    logger.info("Verify search history contains all searched symbols")
    android.home_screen.verify_search_history_items(symbol_list)

    logger.info("Step 4: Delete search history")
    android.home_screen.delete_search_history()

    logger.info("Verify search history is empty")
    android.home_screen.verify_search_history_deleted()


@pytest.fixture(autouse=True)
def clear_search_history(android):
    logger.info("- Delete existing search history")
    android.home_screen.delete_search_history()

    yield

    logger.info("- Close search box")
    android.home_screen.cancel_search()
