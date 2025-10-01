import pytest

from src.data.enums import ChartTimeframe, Server
from src.data.project_info import RuntimeConfig
from src.utils.logging_utils import logger

# SYMBOLS = "AAPL"  # market closed
SYMBOLS = "HK"
EXP_TIME = RuntimeConfig.charttime
pytestmark = [pytest.mark.critical]

timeframe_list = {
    Server.MT5: [
        ChartTimeframe.one_min,
        ChartTimeframe.one_day,
        ChartTimeframe.five_min,
        ChartTimeframe.three_hour,
        ChartTimeframe.fifteen_min,
        ChartTimeframe.four_hour,
        ChartTimeframe.twenty_min,
        ChartTimeframe.six_hour,
        ChartTimeframe.two_hour,
        ChartTimeframe.one_month,
        ChartTimeframe.thirty_min,
        ChartTimeframe.one_week,
        ChartTimeframe.one_hour,
        ChartTimeframe.ten_min,
    ],
    Server.MT4: ChartTimeframe.mt4_list()
}


def test_default_time(ios):
    logger.info(f"Step 1: Search and select symbol: {SYMBOLS!r}")
    ios.home_screen.search_and_select_symbol(SYMBOLS)

    logger.info(f"Step 2: Get default render time")
    elapsed = ios.trade_screen.chart.get_default_render_time()

    logger.info(f"Verify first render time: {elapsed!r} sec <= {EXP_TIME!r} sec")
    ios.trade_screen.chart.verify_render_time(elapsed, EXP_TIME)


@pytest.mark.parametrize("timeframe", timeframe_list[RuntimeConfig.server])
def test_timeframe(ios, timeframe, setup_test):
    logger.info(f"Step 1: Select and get chart render time for timeframe: {timeframe.value!r}")
    elapsed = ios.trade_screen.chart.get_timeframe_render_time(timeframe)

    logger.info(f"Verify render time: {elapsed!r} sec <= {EXP_TIME!r} sec")
    ios.trade_screen.chart.verify_render_time(elapsed, EXP_TIME)


@pytest.mark.parametrize("timeframe", timeframe_list[RuntimeConfig.server])
def test_select_timeframe_repeatedly(ios, timeframe, setup_test):
    logger.info(f"Step: Continue select and get chart render time for timeframe: {timeframe.value!r}")
    elapsed = ios.trade_screen.chart.get_timeframe_render_time(timeframe)

    logger.info(f"Verify render time: {elapsed!r} sec <= {EXP_TIME!r} sec")
    ios.trade_screen.chart.verify_render_time(elapsed, EXP_TIME)


@pytest.fixture(scope="module", autouse=True)
def setup_test(ios):
    if not ios.trade_screen.chart.is_symbol_selected(SYMBOLS):
        logger.info(f"- Search and select symbol: {SYMBOLS!r}")
        ios.home_screen.search_and_select_symbol(SYMBOLS)

    yield
