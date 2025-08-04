import pytest

from src.utils import random_utils
from src.utils.logging_utils import logger


@pytest.mark.parametrize("search_text", (
    random_utils.random_username(),
    random_utils.random_number_by_length(),
))

def test(android, search_text):

    logger.info(f"Step 1: Search with text: {search_text!r}")
    android.home_screen.search_symbol(search_text)

    logger.info(f"Verify search result empty with {search_text!r}")
    android.home_screen.verify_empty_search_result()
