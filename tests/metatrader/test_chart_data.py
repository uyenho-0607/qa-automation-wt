import pytest

from src.apis.api_client import APIClient
from src.data.enums import ChartTimeframe, Server
from src.data.project_info import RuntimeConfig
from src.utils.logging_utils import logger
from src.utils.metatrader_utils import parse_metatrader_data, compare_chart_data

SYMBOL_LIST = {
    Server.MT4: ["BTCUSD.std"],
    Server.MT5: ["BAKE.USD"]
}

server = RuntimeConfig.server


@pytest.mark.parametrize(
    "symbol, timeframe", [(_symbol, _time) for _symbol in SYMBOL_LIST[server] for _time in ChartTimeframe.list_values()]
)
def test(symbol, timeframe):

    logger.info("Step 1: Parse meta trader data")
    chart_data = parse_metatrader_data(symbol, timeframe)
    chart_data.sort(key=lambda x: x["chartTime"])

    logger.info("Step 2: Get data from chart using API")
    api_resp = APIClient().chart.get_candlestick(
        symbol=symbol, timeframe=timeframe,
        from_time=chart_data[0]["chartTime"],
        to=chart_data[-1]["chartTime"]
    )

    logger.info(f"Verify both dataset together, timeframe: {timeframe.name!r}")
    compare_chart_data(chart_data, api_resp, timeframe, symbol)