import time

import pytest

from src.data.project_info import RuntimeConfig
from src.utils.assert_utils import soft_assert
from src.utils.logging_utils import logger

SYMBOL = "BTCUSD"
EXP_TIME = RuntimeConfig.charttime

pytestmark = [pytest.mark.critical]


def test_first_render(android):

    logger.info("Step 1: Get default render time")
    elapsed = android.trade_screen.chart.get_default_render_time()

    logger.info(f"Verify default render time: {elapsed!r} sec is LESS than / EQUAL to: {EXP_TIME!r} sec")
    soft_assert(elapsed <= EXP_TIME, True, error_message=f"Actual render time: {elapsed!r} sec, EXP: {EXP_TIME!r} sec")


@pytest.mark.parametrize("timeframe", [
    "1m",
    "2m",
    "3m",
    "4m",
    "5m",
    "6m",
    "10m",
    "15m",
    "20m",
    "30m",
    "1H",
    "2H",
    "3H",
    "4H",
    "6H",
    "1D",
    "1W",
    "1M"
])
def test(android, timeframe, setup_test):
    time.sleep(2)

    logger.info(f"Step 1: Select and get chart render time for timeframe: {timeframe!r}")
    elapsed = android.trade_screen.chart.get_timeframe_render_time(timeframe)

    logger.info(f"Verify render time: {elapsed!r} sec is LESS than / EQUAL to: {EXP_TIME!r} sec")
    soft_assert(elapsed <= EXP_TIME, True, error_message=f"Actual render time: {elapsed!r} sec, EXP: {EXP_TIME!r} sec")


@pytest.fixture(scope="module", autouse=True)
def setup_test(android):
    logger.info(f"- Search and select symbol: {SYMBOL}")
    android.home_screen.search_and_select_symbol(SYMBOL)
