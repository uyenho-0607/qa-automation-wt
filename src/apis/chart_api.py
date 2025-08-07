from src.apis.api_base import BaseAPI
from src.data.enums import ChartTimeframe


class ChartAPI(BaseAPI):
    _candlestick_endpoint = "/chart/v1/candlestick"

    def get_candlestick(
            self, symbol: str, timeframe: ChartTimeframe, from_time=None, to=None
    ):
        params = {"symbol": symbol, "period": timeframe.get_timeframe(), "from": from_time, "to": to}
        resp = self.get(self._candlestick_endpoint, params)
        return resp
