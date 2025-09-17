from src.data.consts import ISSUE_SYMBOLS
from src.data.enums import WatchListTab, OrderType
from src.utils.logging_utils import logger


class ObjSymbol:
    all_symbols = None
    symbols_data = None
    disabled_symbols = None
    symbols_details = {}
    threshold = 500  # prioritize symbols with cheaper price

    def __init__(self):
        self._get_disabled_symbols()
        self._init_symbols()

    @classmethod
    def _get_disabled_symbols(cls):
        if ObjSymbol.disabled_symbols is None:
            cls.get_disabled_symbols()

    @classmethod
    def _init_symbols(cls):
        """Get symbols data with trading status"""
        from src.apis.api_client import APIClient

        # get all available symbols
        if not ObjSymbol.all_symbols:
            resp = APIClient().market.get_watchlist_items(WatchListTab.ALL, get_symbols=False)

            # filter symbol with TRADING status
            trading_symbols = [item for item in resp if item["status"] == "TRADING"]

            if not trading_symbols:
                # no TRADING -> stop !
                raise RuntimeError("No trading symbols available (all symbols are OFF QUOTE).")


            # filter out symbols to be used, CRYPTO is most prioritized
            for symbol_type in [WatchListTab.CRYPTO, WatchListTab.FOREX, WatchListTab.COMMODITIES, WatchListTab.INDEX, WatchListTab.SHARES]:
                symbols = [item for item in trading_symbols if item["type"] == symbol_type.upper()]

                if symbols:
                    break

            # filter disabled symbols
            cls.all_symbols = [item for item in symbols if item['symbol'] not in ObjSymbol.disabled_symbols]

            # Lastly, filter symbols with low price
            filtered_price = [item for item in cls.all_symbols if item['ask'] < cls.threshold]
            cls.symbols_data = filtered_price or cls.all_symbols

        return cls.symbols_data

    @classmethod
    def get_symbols(cls, get_all=False):
        res = [item['symbol'] for item in (cls.symbols_data if not get_all else cls.all_symbols)]
        return res

    @classmethod
    def get_disabled_symbols(cls):
        """Get list of symbols being disabled to avoid broken tests"""
        from src.apis.api_client import APIClient
        logger.info("- Filter disabled symbols by getting all placed orders")
        # check market orders
        market_orders = APIClient().order.get_orders_details(order_type=OrderType.MARKET)

        # check pending orders
        pending_orders = APIClient().order.get_orders_details(order_type=OrderType.STOP)

        disabled_symbols = [item["symbol"] for item in market_orders + pending_orders if not item["isEnable"]]
        ObjSymbol.disabled_symbols = disabled_symbols

        return list(set(disabled_symbols))


    @classmethod
    def get_symbol_details(cls, symbol):
        from src.apis.api_client import APIClient

        if not cls.symbols_details.get(symbol):

            logger.info("- Update symbols details for later usage")
            symbol_detail = APIClient().market.get_symbol_details(symbol)
            contract_size = symbol_detail.get('contractSize')

            symbol_item = [item for item in cls.all_symbols if item['symbol'] == symbol]

            if symbol_item:
                decimal = symbol_item[0]['decimal']
                point_step = 10 ** -decimal
                cls.symbols_details[symbol] = dict(point_step=point_step, decimal=decimal, contract_size=contract_size)
                return cls.symbols_details[symbol]
            else:
                cls.symbols_details[symbol] = dict(point_step=0, decimal=0, contract_size=0)

        return cls.symbols_details[symbol]
