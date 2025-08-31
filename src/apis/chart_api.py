from src.apis.api_base import BaseAPI
from src.data.enums import ChartTimeframe
from src.utils.logging_utils import logger


class ChartAPI(BaseAPI):
    _candlestick_endpoint = "/chart/v1/candlestick"

    def get_candlestick(
            self, symbol: str, timeframe: ChartTimeframe, from_time=None, to=None, **kwargs
    ):
        params = {"symbol": symbol, "period": timeframe.get_timeframe(), "from": from_time, "to": to}
        logger.debug("[API] Get chart candle sticks")
        resp = self.get(self._candlestick_endpoint, params, **kwargs)
        return resp
