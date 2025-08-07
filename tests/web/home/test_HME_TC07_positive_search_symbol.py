import random

import pytest

from src.utils.logging_utils import logger


def test(web, symbol):
    wildcard = symbol[:random.randint(2, len(symbol) - 1)]

    logger.info(f"Step 1: Search with text: {symbol!r}")
    web.home_page.search_symbol(symbol)

    logger.info(f"Verify search result matches {symbol!r}")
    web.home_page.verify_search_result(symbol)

    logger.info(f"Step 2: Search with wild card: {wildcard!r}")
    web.home_page.search_symbol(wildcard)

    logger.info(f"Verify search result matches: {wildcard!r}")
    web.home_page.verify_wildcard_search_result(wildcard)


@pytest.fixture(autouse=True)
def clear_search_history(web):
    logger.info("- Delete existing search history")
    web.home_page.delete_search_history()
