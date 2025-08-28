from src.apis.api_base import BaseAPI
from src.data.enums import WatchListTab
from src.utils.logging_utils import logger


class MarketAPI(BaseAPI):
    _symbol_details = "/market/v1/symbol/detail"
    _watchlists = "/market/v1/watchlists"  # for getting symbols
    _watchlist = "/market/v1/watchlist"  # for post/ delete starred symbols
    _all = "/market/v1/symbols/all"

    watchlist_map = {
        WatchListTab.FAVOURITES: "MY_WATCHLIST",
        WatchListTab.TOP_PICKS: "POPULAR",
        WatchListTab.TOP_GAINER: "TOP_GAINER",
        WatchListTab.TOP_LOSER: "TOP_LOSER"
    }

    def __init__(self):
        super().__init__()

    def get_symbol_details(self, symbol: str):
        logger.debug(f"[API] Get symbol details (symbol:{symbol})")
        resp = self.get(endpoint=self._symbol_details, params={"symbol": symbol})
        return resp

    def get_watchlist_items(self, tab: WatchListTab, get_symbols=True):

        _endpoint = self._watchlists
        if tab == WatchListTab.ALL or tab in WatchListTab.sub_tabs():
            _endpoint = self._all

        logger.debug(f"[API] Get watchlist symbols (tab:{tab.value})")
        resp = self.get(_endpoint, params={"code": self.watchlist_map.get(tab)})

        if get_symbols:
            res = [item["symbol"] for item in resp]

            if tab in WatchListTab.sub_tabs():
                res = [item["symbol"] for item in resp if item["type"] in tab.name.upper()]

            return res
        return resp

    def delete_starred_symbols(self, symbols: str | list = None):
        if symbols:
            symbols = symbols if isinstance(self, list) else [symbols]
        else:
            # delete all current starred symbols
            symbols = self.get_watchlist_items(WatchListTab.FAVOURITES)

        logger.debug(f"[API] Unstar symbols: {', '.join(symbols)}")
        for symbol in symbols:
            self.delete(self._watchlist, {"symbol": symbol})

    def post_starred_symbol(self, symbol: str):
        payload = {"symbol": symbol}
        logger.debug(f"[API] Mark star symbol: {symbol}")
        resp = self.post(self._watchlist, payload)
        return resp

