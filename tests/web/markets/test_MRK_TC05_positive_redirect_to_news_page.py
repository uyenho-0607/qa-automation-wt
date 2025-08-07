import pytest

from src.data.enums import Features
from src.utils.logging_utils import logger


@pytest.mark.skip
def test(web):
    logger.info("Step 1: Navigate to Market Page")
    web.home_page.navigate_to(Features.MARKETS)

    logger.info("Step 2: Select News content")
    web.markets_page.select_news_content()

    logger.info("Verify Redirected to News Page")
    web.news_page.verify_page_url()
