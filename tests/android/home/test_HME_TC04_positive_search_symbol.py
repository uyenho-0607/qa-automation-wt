import random

import pytest

from src.utils.logging_utils import logger


def test(android, symbol):
    wildcard = symbol[:random.randint(2, len(symbol) - 1)]

    logger.info(f"Step 1: Search with text: {symbol!r}")
    android.home_screen.search_symbol(symbol)

    logger.info(f"Verify search result matches {symbol!r}")
    android.home_screen.verify_search_result(symbol)

    logger.info(f"Step 2: Search with wild card: {wildcard!r}")
    android.home_screen.search_symbol(wildcard)

    logger.info(f"Verify search result matches: {wildcard!r}")
    android.home_screen.verify_wildcard_search_result(wildcard)


@pytest.fixture(autouse=True)
def clear_search_history(android):
    logger.info("- Delete existing search history")
    android.home_screen.delete_search_history()