import random

import pytest

from src.data.consts import SYMBOLS
from src.data.project_info import ProjectConfig
from src.utils.logging_utils import logger


def test(android):
    symbol_list = random.sample(SYMBOLS[ProjectConfig.server], k=3)

    for index, symbol_name in enumerate(symbol_list):
        logger.info(f"Step {index + 1}: Search and select symbol: {symbol_name!r}")
        android.home_screen.select_symbol_from_search(symbol_name)

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