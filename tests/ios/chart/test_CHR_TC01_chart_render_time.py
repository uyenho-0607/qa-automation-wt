import pytest

from src.data.project_info import RuntimeConfig
from src.utils.assert_utils import soft_assert
from src.utils.logging_utils import logger

"""
BTCUSD , AUDCAD , XAGUSD , NVDA 
"""

SYMBOL = "AUDCAD"
EXP_TIME = RuntimeConfig.charttime


def test_first_render(ios):

    # logger.info(f"Step 1: Search and select symbol: {SYMBOL!r}")
    # ios.home_screen.search_and_select_symbol(SYMBOL)

    logger.info("Step 1: Get first time chart render")
    elapsed = ios.trade_screen.chart.get_chart_render_first_time()

    logger.info(f"Verify chart render time - {elapsed!r} sec is LESS than / EQUAL to {EXP_TIME!r} sec")
    soft_assert(elapsed <= EXP_TIME, True, error_message=f"Actual chart time: {elapsed!r} sec, expected: {EXP_TIME!r} sec")


@pytest.mark.parametrize("timeframe", [
    "1m",
    # "5m",
    # "15m",
    # "30m",
    # "1H",
    # "4H",
    # "1D",
    # "1W",
    # "1M",
])
def test_each_timeframe(ios, timeframe):
    logger.info(f"Step 1: Get chart render time for timeframe: {timeframe!r}")
    elapsed = ios.trade_screen.chart.get_chart_render_time(timeframe)

    logger.info(f"Verify chart render time - {elapsed!r} sec is LESS than / EQUAL to {EXP_TIME!r} sec")
    soft_assert(elapsed <= EXP_TIME, True, error_message=f"Actual chart time: {elapsed!r} sec, expected: {EXP_TIME!r} sec")


@pytest.fixture(scope="module", autouse=True)
def setup_test(ios):

    logger.info(f"- Search and select symbol: {SYMBOL!r}")
    ios.home_screen.search_and_select_symbol(SYMBOL)
