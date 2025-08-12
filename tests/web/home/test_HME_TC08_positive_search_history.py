import random

import pytest

from src.data.objects.symbol_obj import ObjSymbol
from src.data.ui_messages import UIMessages
from src.utils.logging_utils import logger


def test(web):
    symbol_list = random.sample(ObjSymbol().get_symbols(), k=2)

    for index, symbol_name in enumerate(symbol_list):
        logger.info(f"Step {index + 1}: Search and select symbol: {symbol_name!r}")
        web.home_page.search_symbol(symbol_name)
        web.home_page.select_item_from_search_result(symbol_name)

    logger.info("Verify search history contains all searched symbols")
    web.home_page.clear_search_field()
    web.home_page.verify_search_history_items(symbol_list)

    logger.info("Step 5: Delete search history")
    web.home_page.delete_search_history(check_displayed=False)

    logger.info(f"Verify message {UIMessages.TYPE_SOMETHING_TO_SEARCH!r} message")
    web.home_page.verify_search_history_empty_message()

    logger.info("Verify search history items is empty")
    web.home_page.verify_search_result_deleted()


@pytest.fixture(autouse=True)
def clear_search_history(web):
    logger.info("- Delete existing search history")
    web.home_page.delete_search_history()
