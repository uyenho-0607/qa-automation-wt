import random
import time

import pytest

from src.data.enums import ChartTimeframe
from src.data.objects.symbol_obj import ObjSymbol
from src.data.project_info import RuntimeConfig
from src.utils.logging_utils import logger

pytestmark = [pytest.mark.critical]

# Expected render time (seconds)
EXP_TIME = RuntimeConfig.charttime
timeframe_list = ChartTimeframe.crit_list()


def test_default(web_app):
    logger.info(f"Step 1: Get default render time")
    elapsed = web_app.trade_page.chart.get_default_render_time()

    logger.info(f"Verify first render time: {elapsed!r} sec <= {EXP_TIME!r} sec")
    web_app.trade_page.chart.verify_render_time(elapsed, EXP_TIME)


@pytest.mark.parametrize("timeframe", timeframe_list)
def test_timeframe(web_app, timeframe):

    logger.info(f"Step 1: Select and get chart render time for timeframe: {timeframe.value!r}")
    time.sleep(1)
    elapsed = web_app.trade_page.chart.get_timeframe_render_time(timeframe)

    logger.info(f"Verify render time: {elapsed!r} sec <= {EXP_TIME!r} sec")
    web_app.trade_page.chart.verify_render_time(elapsed, EXP_TIME)


@pytest.mark.parametrize("timeframe", timeframe_list)
def test_select_timeframe_repeatedly(web_app, timeframe):

    logger.info(f"Step: Continue select timeframe: {timeframe.value!r}")
    time.sleep(1)
    elapsed = web_app.trade_page.chart.get_timeframe_render_time(timeframe)

    logger.info(f"Verify render time: {elapsed!r} sec <= {EXP_TIME!r} sec")
    web_app.trade_page.chart.verify_render_time(elapsed, EXP_TIME)


@pytest.fixture(autouse=True)
def cleanup_chart(web_app):
    yield
    web_app.trade_page.chart.exit_chart_iframe()


@pytest.fixture(scope="module", autouse=True)
def setup_test(web_app):

    select_symbol = random.choice(ObjSymbol().all_symbols)

    logger.info(f"- Search and select symbol: {select_symbol}")
    web_app.home_page.search_and_select_symbol(select_symbol)

