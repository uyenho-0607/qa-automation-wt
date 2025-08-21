import random
import time

import pytest

from src.data.enums import ChartTimeframe, Features
from src.data.project_info import RuntimeConfig
from src.utils.logging_utils import logger

SYMBOLS = ["XAGUSD"]
EXP_TIME = RuntimeConfig.charttime



@pytest.mark.parametrize("symbol", SYMBOLS)
def test(ios, symbol):
    """
    Runs both:
    1. Default render time for the chart.
    2. Timeframe render times for all ChartTimeframe values.
    """
    # --- Default render ---
    logger.info(f"Step 1: Search and select symbol: {symbol}")
    ios.home_screen.search_and_select_symbol(symbol)

    logger.info(f"Step 2: Get default render time")
    elapsed = ios.trade_screen.chart.get_default_render_time()

    logger.info(f"Verify first render time: {elapsed!r} sec <= {EXP_TIME!r} sec")
    ios.trade_screen.chart.verify_render_time(elapsed, EXP_TIME)

    # --- Timeframes ---
    for index, timeframe in enumerate(ChartTimeframe.list_values()):
        time.sleep(1)

        logger.info(f"Step {3 + index}: Select and get chart render time for timeframe: {timeframe.value!r}")
        elapsed = ios.trade_screen.chart.get_timeframe_render_time(timeframe)

        logger.info(f"Verify render time: {elapsed!r} sec <= {EXP_TIME!r} sec")
        ios.trade_screen.chart.verify_render_time(elapsed, EXP_TIME)


@pytest.mark.parametrize("symbol", random.choices(SYMBOLS))
def test_select_timeframe_repeatedly(ios, symbol):
    """
    verifying render times each switch repeatedly 2 times.
    """
    repeat_times = 2

    logger.info(f"Step 1: Search and select symbol: {symbol}")
    ios.home_screen.search_and_select_symbol(symbol)

    for round_idx in range(1, repeat_times + 1):
        for timeframe in ChartTimeframe.mt4_list():
            time.sleep(1)

            logger.info(f"Step: Select timeframe: {timeframe.value!r} - ROUND: {round_idx}")
            elapsed = ios.trade_screen.chart.get_timeframe_render_time(timeframe)

            logger.info(f"Verify render time: {elapsed!r} sec <= {EXP_TIME!r} sec")
            ios.trade_screen.chart.verify_render_time(elapsed, EXP_TIME)


@pytest.fixture(autouse=True)
def cleanup_chart(ios):
    yield

    logger.info("- Navigate back to Home Page")
    ios.trade_screen.navigate_to(Features.HOME)

