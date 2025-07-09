import pytest

from src.utils import random_utils
from src.utils.logging_utils import logger


@pytest.mark.parametrize("search_text", (
        random_utils.random_username(),
        random_utils.random_number_by_length(),
))
def test(web, search_text):
    logger.info(f"Step 1: Search with text: {search_text!r}")
    web.home_page.search_symbol(search_text)
    web.home_page.wait_for_spin_loader()

    logger.info(f"Verify search result empty with {search_text!r}")
    web.home_page.verify_not_found_search_message()
