import time

import pytest

from src.data.project_info import RuntimeConfig
from src.utils.assert_utils import soft_assert
from src.utils.logging_utils import logger

SYMBOL = "BTCUSD"
EXP_TIME = RuntimeConfig.charttime

pytestmark = [pytest.mark.critical]


def test_first_render(web):
    logger.info(f"Step 1: Search and select symbol: {SYMBOL!r}")
    web.home_page.search_and_select_symbol(SYMBOL)

    logger.info("Step 2: Get default render time")
    elapsed = web.trade_page.chart.get_first_render_time()

    logger.info(f"Verify default render time: {elapsed!r} sec is LESS than / EQUAL to: {EXP_TIME!r} sec")
    soft_assert(elapsed <= EXP_TIME, True, error_message=f"Actual render time: {elapsed!r} sec, EXP: {EXP_TIME!r} sec")


@pytest.mark.parametrize("timeframe", [
    "1min",
    "5min",
    "15min",
    "30min",
    "1H",
    "4H",
    "1D",
    "1W",
    "1M"
])
def test(web, timeframe, setup_test):
    time.sleep(2)

    logger.info(f"Step 1: Select and get chart render time for timeframe: {timeframe!r}")
    elapsed = web.trade_page.chart.get_timeframe_render_time(timeframe)

    logger.info(f"Verify render time: {elapsed!r} sec is LESS than / EQUAL to: {EXP_TIME!r} sec")
    soft_assert(elapsed <= EXP_TIME, True, error_message=f"Actual render time: {elapsed!r} sec, EXP: {EXP_TIME!r} sec")


@pytest.fixture(autouse=True)
def exit_chart(web):
    yield
    web.trade_page.chart.exit_chart_iframe()


@pytest.fixture(scope="module")
def setup_test(web):
    logger.info(f"- Check if {SYMBOL} is being selected")
    is_selected = web.trade_page.chart.is_symbol_selected(SYMBOL)

    if not is_selected:
        logger.info(f"- Search and select symbol: {SYMBOL}")
        web.home_page.search_and_select_symbol(SYMBOL)

    yield
    web.trade_page.chart.exit_chart_iframe()
