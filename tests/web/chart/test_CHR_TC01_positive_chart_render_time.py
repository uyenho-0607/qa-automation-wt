import random
import time

import pytest

from src.data.enums import ChartTimeframe
from src.data.project_info import RuntimeConfig
from src.utils.logging_utils import logger

pytestmark = [pytest.mark.critical]

# Expected render time (seconds)
EXP_TIME = RuntimeConfig.charttime
SYMBOLS = ["BTCUSD", "ETHUSD"]


@pytest.mark.parametrize("symbol", ["ETHUSD", ])
def test(web, symbol):
    """
    Runs both:
    1. Default render time for the chart.
    2. Timeframe render times for all ChartTimeframe values.
    """
    # --- Default render ---
    logger.info(f"Step 1: Search and select symbol: {symbol}")
    web.home_page.search_and_select_symbol(symbol)
    web.trade_page.chart.wait_for_symbol_selected(symbol)

    logger.info(f"Step 2: Get default render time")
    elapsed = web.trade_page.chart.get_default_render_time()

    logger.info(f"Verify first render time: {elapsed!r} sec <= {EXP_TIME!r} sec")
    web.trade_page.chart.verify_render_time(elapsed, EXP_TIME)

    # --- Timeframes ---
    for index, timeframe in enumerate(ChartTimeframe.display_list()):
        time.sleep(2)

        logger.info(f"Step {3 + index}: Select and get chart render time for timeframe: {timeframe.value!r}")
        elapsed = web.trade_page.chart.get_timeframe_render_time(timeframe)

        logger.info(f"Verify render time: {elapsed!r} sec <= {EXP_TIME!r} sec")
        web.trade_page.chart.verify_render_time(elapsed, EXP_TIME)


@pytest.mark.parametrize("symbol", random.choices(SYMBOLS))
def test_select_timeframe_repeatedly(web, symbol):
    """
    verifying render times each switch repeatedly 2 times.
    """
    repeat_times = 2

    logger.info(f"Step 1: Search and select symbol: {symbol}")
    web.home_page.search_and_select_symbol(symbol)
    web.trade_page.chart.wait_for_symbol_selected(symbol)

    for round_idx in range(1, repeat_times + 1):
        for timeframe in ChartTimeframe.display_list():
            time.sleep(2)

            logger.info(f"Step: Select timeframe: {timeframe.value!r} - ROUND: {round_idx}")
            elapsed = web.trade_page.chart.get_timeframe_render_time(timeframe)

            logger.info(f"Verify render time: {elapsed!r} sec <= {EXP_TIME!r} sec")
            web.trade_page.chart.verify_render_time(elapsed, EXP_TIME)


@pytest.fixture(autouse=True)
def cleanup_chart(web):
    yield
    web.trade_page.chart.exit_chart_iframe()
