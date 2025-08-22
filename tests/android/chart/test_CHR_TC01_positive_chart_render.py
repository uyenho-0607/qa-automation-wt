import time

import pytest

from src.data.enums import ChartTimeframe
from src.data.project_info import RuntimeConfig
from src.utils.logging_utils import logger

pytestmark = [pytest.mark.critical]

# Expected render time (seconds)
EXP_TIME = RuntimeConfig.charttime
SYMBOLS = "XAGUSD"


def test_default(android):
    logger.info(f"Step 1: Get default render time")
    elapsed = android.trade_screen.chart.get_default_render_time()

    logger.info(f"Verify first render time: {elapsed!r} sec <= {EXP_TIME!r} sec")
    android.trade_screen.chart.verify_render_time(elapsed, EXP_TIME)


@pytest.mark.parametrize("timeframe", ChartTimeframe.list_values())
def test_timeframe(android, timeframe):
    logger.info(f"Step 1: Select and get chart render time for timeframe: {timeframe.value!r}")
    elapsed = android.trade_screen.chart.get_timeframe_render_time(timeframe)

    logger.info(f"Verify render time: {elapsed!r} sec <= {EXP_TIME!r} sec")
    android.trade_screen.chart.verify_render_time(elapsed, EXP_TIME)


def test_select_timeframe_repeatedly(android, ):
    repeat_times = 1

    for round_idx in range(1, repeat_times + 1):
        for timeframe in ChartTimeframe.list_values():
            time.sleep(1)

            logger.info(f"Step: Continue select timeframe: {timeframe.value!r}")
            elapsed = android.trade_screen.chart.get_timeframe_render_time(timeframe)

            logger.info(f"Verify render time: {elapsed!r} sec <= {EXP_TIME!r} sec")
            android.trade_screen.chart.verify_render_time(elapsed, EXP_TIME)


@pytest.fixture(scope="module", autouse=True)
def setup_test(android):
    logger.info(f"- Search and select symbol: {SYMBOLS}")
    android.home_screen.search_and_select_symbol(SYMBOLS)
