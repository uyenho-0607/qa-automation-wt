import random

import pytest

from src.data.consts import get_symbols
from src.utils.logging_utils import logger


def test(web_app):
    symbol_list = random.sample(get_symbols(), k=2)

    for index, symbol_name in enumerate(symbol_list):
        logger.info(f"Step {index + 1}: Search and select symbol: {symbol_name!r}")
        web_app.home_page.search_and_select_symbol(symbol_name)
        web_app.home_page.go_back()

    logger.info("Verify search history contains all searched symbols")
    web_app.home_page.verify_search_history_items(symbol_list)

    logger.info("Step 4: Delete search history")
    web_app.home_page.delete_search_history()

    logger.info("Verify search history is empty")
    web_app.home_page.verify_search_history_deleted()


@pytest.fixture(autouse=True)
def clear_search_history(web_app):
    logger.info("- Delete existing search history")
    web_app.home_page.delete_search_history()

    yield

    logger.info("- Close search box")
    web_app.home_page.cancel_search()
