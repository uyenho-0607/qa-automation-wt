from src.data.consts import ISSUE_SYMBOLS
from src.data.enums import WatchListTab


class ObjSymbol:
    all_symbols = None
    symbols_data = None
    symbols_details = {}
    threshold = 100  # prioritize symbols with cheaper price

    def __init__(self):
        self._init_symbols()

    @classmethod
    def _init_symbols(cls):
        """Get symbols data with trading status"""
        from src.apis.api_client import APIClient

        if not ObjSymbol.all_symbols:
            resp = APIClient().market.get_watchlist_items(WatchListTab.ALL, get_symbols=False)
            trading_symbols = [item for item in resp if item["status"] == "TRADING"]

            if not trading_symbols:
                raise RuntimeError("No trading symbols available (all symbols are OFF QUOTE).")


            for symbol_type in [WatchListTab.CRYPTO, WatchListTab.FOREX, WatchListTab.COMMODITIES, WatchListTab.INDEX, WatchListTab.SHARES]:
                symbols = [item for item in trading_symbols if item["type"] == symbol_type.upper()]

                if symbols:
                    break

            cls.all_symbols = [item for item in symbols if item['symbol'] not in ISSUE_SYMBOLS]

            # Filter symbols with small prices (to avoid insufficient balance)
            filtered_price = [item for item in cls.all_symbols if item['ask'] < cls.threshold]
            cls.symbols_data = filtered_price or cls.all_symbols

        return cls.symbols_data

    @classmethod
    def get_symbols(cls, get_all=False):
        res = [item['symbol'] for item in (cls.symbols_data if not get_all else cls.all_symbols)]
        return res


    @classmethod
    def get_symbol_details(cls, symbol):
        if not cls.symbols_details.get(symbol):
            symbol_item = [item for item in cls.all_symbols if item['symbol'] == symbol]

            if symbol_item:
                decimal = symbol_item[0]['decimal']
                point_step = 10 ** -decimal
                cls.symbols_details[symbol] = dict(point_step=point_step, decimal=decimal)
                return cls.symbols_details[symbol]

            else:
                cls.symbols_details[symbol] =  dict(point_step=0, decimal=0)

        return cls.symbols_details[symbol]