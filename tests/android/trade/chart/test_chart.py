import pytest

from src.utils.logging_utils import logger


@pytest.mark.parametrize(
    "timeframe", [
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
    ]
)
def _test(android, timeframe):

    logger.info(f"Step 1: Select {timeframe} timeframe")
    android.trade_screen.chart.select_candle_stick(timeframe)

    logger.info(f"Step 2: Verify chart load time")
    android.trade_screen.chart.verify_chart_load_time()



def test_table(android, ):
    logger.info("Verify all chart load time")
    android.trade_screen.chart.verify_all_chart_load_time()