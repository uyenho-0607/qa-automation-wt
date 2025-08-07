import pytest

from src.utils import random_utils
from src.utils.logging_utils import logger


@pytest.mark.parametrize("search_text", (
    random_utils.random_username(),
    random_utils.random_number_by_length(),
))

def test(web_app, search_text):

    logger.info(f"Step 1: Search with text: {search_text!r}")
    web_app.home_page.search_symbol(search_text)

    logger.info(f"Verify search result empty with {search_text!r}")
    web_app.home_page.verify_empty_search_result()
