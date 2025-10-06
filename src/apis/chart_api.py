from src.apis.api_base import BaseAPI
from src.data.enums import ChartTimeframe


class ChartAPI(BaseAPI):
    _candlestick_endpoint = "/chart/v4/candlestick"
    _latest = "/chart/v2/candlestick/latest"

    def get_candlestick(
            self, symbol: str, timeframe: ChartTimeframe, from_time=None, to=None
    ):
        params = {"symbol": symbol, "period": timeframe.get_timeframe(), "from": from_time, "to": to}
        resp = self.get(self._candlestick_endpoint, params)
        return resp


    def get_chart_latest(self, symbol: str, timeframe: ChartTimeframe, to=None):

        params = {"symbol": symbol, "period": timeframe.get_timeframe()}
        if to:
            params |= {"to": to}
        resp = self.get(self._latest, params=params)
        return resp
