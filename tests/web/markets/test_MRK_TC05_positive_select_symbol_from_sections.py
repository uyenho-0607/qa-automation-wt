import random

import pytest

from src.data.enums import Features, MarketsSection, WatchListTab
from src.utils.logging_utils import logger

SECTION_LIST = [MarketsSection.TOP_PICKS, MarketsSection.TOP_GAINER]

@pytest.mark.parametrize("section", SECTION_LIST)
def test_watchlist(setup_test, section, web):
    symbols = setup_test[section]
    if not symbols:
        pytest.skip("No symbol to test")

    select_symbol = random.choice(symbols)

    logger.info(f"Step 1: Navigate to Market Page")
    web.home_page.navigate_to(Features.MARKETS)

    logger.info(f"Step 2: Select symbol from section: {section}")
    web.markets_page.select_symbol(section, select_symbol)

    logger.info("Verify tab is selected")
    web.home_page.watch_list.verify_tab_selected(WatchListTab(section))

    logger.info("Verify symbol is selected in tab")
    web.home_page.watch_list.verify_symbol_selected(select_symbol)

    logger.info("Verify symbol is selected in chart")
    web.trade_page.chart.verify_symbol_selected(select_symbol)


def test_signal(web):

    logger.info("Step 1: Navigate to Markets Page")
    web.home_page.navigate_to(Features.MARKETS, wait=True)

    logger.info("Step 2: Select symbol from Signal")
    select_symbol = web.markets_page.select_symbol(MarketsSection.SIGNAL)

    logger.info("Verify Page is redirected to Sinal Page")
    web.signal_page.verify_page_url()

    logger.info("Verify symbol is selected in signal list")
    web.signal_page.verify_symbol_starred(select_symbol)

    logger.info("Verify symbol is selected in chart")
    web.trade_page.chart.verify_symbol_selected(select_symbol)


def test_news(web):
    logger.info("Step 1: Navigate to Market Page")
    web.home_page.navigate_to(Features.MARKETS)

    logger.info("Step 2: Select News content")
    web.markets_page.select_news_content()

    logger.info("Verify Redirected to News Page")
    web.news_page.verify_page_url()


@pytest.fixture(scope="module")
def setup_test(web):

    symbols = {}

    logger.info("- Navigate to Markets Page")
    web.home_page.navigate_to(Features.MARKETS, wait=True)

    for section in SECTION_LIST:
        logger.info(f"- Get current symbol from {section!r}")
        symbols[section] = web.markets_page.get_symbols(section)

    yield symbols
