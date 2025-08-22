import time

import pytest

from src.data.enums import ChartTimeframe
from src.data.project_info import RuntimeConfig
from src.utils.logging_utils import logger

SYMBOLS = "BTCUSD"
EXP_TIME = RuntimeConfig.charttime
pytestmark = [pytest.mark.critical]


def test_default_time(ios):

    logger.info("Step 1: Search and select symbol")
    ios.home_screen.search_and_select_symbol(SYMBOLS)

    logger.info(f"Step 2: Get default render time")
    elapsed = ios.trade_screen.chart.get_default_render_time()

    logger.info(f"Verify first render time: {elapsed!r} sec <= {EXP_TIME!r} sec")
    ios.trade_screen.chart.verify_render_time(elapsed, EXP_TIME)


@pytest.mark.parametrize("timeframe", ChartTimeframe.mt4_list())
def test(ios, timeframe, setup_test):

    logger.info(f"Step 1: Select and get chart render time for timeframe: {timeframe.value!r}")
    time.sleep(1)
    elapsed = ios.trade_screen.chart.get_timeframe_render_time(timeframe)

    logger.info(f"Verify render time: {elapsed!r} sec <= {EXP_TIME!r} sec")
    ios.trade_screen.chart.verify_render_time(elapsed, EXP_TIME)


def test_select_timeframe_repeatedly(ios, setup_test):
    """
    verifying render times each switch repeatedly 2 times.
    """
    repeat_times = 1

    for round_idx in range(1, repeat_times + 1):
        for timeframe in ChartTimeframe.mt4_list():

            logger.info(f"Step: Continue select timeframe: {timeframe.value!r}")
            time.sleep(2)
            elapsed = ios.trade_screen.chart.get_timeframe_render_time(timeframe)

            logger.info(f"Verify render time: {elapsed!r} sec <= {EXP_TIME!r} sec")
            ios.trade_screen.chart.verify_render_time(elapsed, EXP_TIME)


@pytest.fixture(scope="module")
def setup_test(ios):

    if ios.trade_screen.chart.is_symbol_selected(SYMBOLS):
        return

    logger.info(f"- Search and select symbol: {SYMBOLS!r}")
    ios.home_screen.search_and_select_symbol(SYMBOLS)
