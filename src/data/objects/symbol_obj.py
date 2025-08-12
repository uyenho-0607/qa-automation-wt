from src.data.enums import WatchListTab
from src.utils.logging_utils import logger


class ObjSymbol:
    all_symbols = None
    symbols_data = None
    symbols_details = {}
    threshold = 100 # prioritize symbols with cheaper price

    def __init__(self):
        self._init_symbols()

    @classmethod
    def _init_symbols(cls):
        """Get symbols data with trading status"""
        from src.apis.api_client import APIClient

        if not ObjSymbol.all_symbols:
            logger.info("- Getting Symbols data")
            resp = APIClient().market.get_watchlist_items(WatchListTab.CRYPTO, get_symbols=False)

            ObjSymbol.all_symbols = [
                item for item in resp if item['type'] == WatchListTab.CRYPTO.upper() and item['status'] == 'TRADING'
            ]
            filtered_price = [item for item in cls.all_symbols if item['ask'] < cls.threshold]

            cls.symbols_data = filtered_price or cls.all_symbols

        return cls.symbols_data

    @classmethod
    def get_symbols(cls, get_all=False):
        return [item['symbol'] for item in cls.symbols_data] if not get_all else cls.all_symbols

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
                raise ValueError(f"Symbol: {symbol!r} not found !!!")

        return cls.symbols_details[symbol]
