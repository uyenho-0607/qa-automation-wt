import random
from functools import cached_property
from typing import Any, List, Dict, Set

from src.data.consts import FAILED_ICON_COLOR
from src.data.enums import WatchListTab, OrderType
from src.utils.logging_utils import logger


class ObjSymbol:
    """
    Manages symbol data:
    - Loads and caches symbol info from APIs once per process lifetime.
    - Provides selection of tradable symbols with optional issue filtering.
    """

    PRICE_THRESHOLD = 500  # limit price for saving money
    TYPE_PRIORITY = ["CRYPTO", "INDEX", "SHARE", "FOREX", "COM"]

    # class-level caches (shared across all instances)
    ALL: List[Dict[str, Any]] = []
    TRADING: List[Dict[str, Any]] = []  # symbols with status == TRADING
    TYPE_SPECIFIC: Dict[str, List[Dict[str, Any]]] = {}  # symbols mapping by TYPE_PRIORITY
    DETAILS: Dict[str, Dict[str, Any]] = {}
    ISSUED: Set[str] = set()

    _initialized = False
    _issue_loaded = False

    def __init__(self, amount=1, s_type="", filter_issue=True):
        self.amount = amount
        self.s_type = s_type or "CRYPTO"
        self.filter_issue = filter_issue

        # init symbol data
        if not self._initialized:
            self._init_data()

        # load issue symbols
        if self.filter_issue and not self._issue_loaded:
            self._get_disabled_symbols()

    # ============ PROPERTY ============
    @cached_property
    def all_symbols(self) -> List[str]:
        """List of all symbols displaying in watch list (all)"""
        return [item.get("symbol") for item in self.ALL]

    @cached_property
    def symbols_by_type(self) -> List[str]:
        """List of symbol by input s_type attribute"""
        return [item.get("symbol") for item in self.TYPE_SPECIFIC.get(self.s_type, [])]

    # ============ PUBLIC INTERFACE ============
    def get_symbol(self):
        """Get TRADABLE symbols with full validation, return symbols as type string | list based on input amount"""
        return self._select_symbols()

    @classmethod
    def get_details(cls, symbol=""):
        """Get details of input symbol"""
        if symbol not in cls.DETAILS:
            cls.DETAILS[symbol] = cls._get_symbol_details(symbol)
        return cls.DETAILS[symbol]

    # ============ CACHE MANAGEMENT ============
    @classmethod
    def _get_disabled_symbols(cls) -> None:
        """Get issue symbols with all current placed orders with isEnable, editable, closable = False"""
        orders = cls._get_all_orders()
        cls.ISSUED = {item["symbol"] for item in orders if not item["isEnable"] or not item["editable"] or not item["closable"]}
        cls._issue_loaded = True

        if cls.ISSUED:
            logger.warning(f"- List symbols with disabled issue: {ObjSymbol.ISSUED}")

    @classmethod
    def _init_data(cls) -> None:
        """Init symbol data through API watch list"""
        # 1. Load all symbols
        cls.ALL = cls._get_all_symbols()
        if not cls.ALL:
            raise RuntimeError(f"No symbols found ! {FAILED_ICON_COLOR}")

        # 2. Filter symbol with TRADING status
        cls.TRADING = [s for s in cls.ALL if s.get("status").lower() == "trading"]
        if not cls.TRADING:
            raise RuntimeError(f"No symbols with TRADING status found ! {FAILED_ICON_COLOR}")

        # 3. Build TYPE_SPECIFIC mapping
        for t in cls.TYPE_PRIORITY:
            cls.TYPE_SPECIFIC[t] = [s for s in cls.TRADING if s.get("type").lower() == t.lower()]

        cls._initialized = True
        logger.info("ObjSymbol: basic symbol data initialized")

    # ============ SYMBOL SELECTION ============
    def _select_symbols(self) -> str | list:
        """Return a list of tradable symbols based on input amount"""
        # get list of symbol with input priority
        s_list = self._select_symbol_current_type(self.s_type)

        if not s_list:
            logger.warning(f"- No symbols with type: {self.s_type} is tradable, fall back to other type")
            for t in self.TYPE_PRIORITY:
                s_list = self._select_symbol_current_type(t)
                # stop if any symbols found based on TYPE_PRIORITY
                if s_list:
                    break

        if self.filter_issue:
            # apply issue filter
            s_list = [s for s in s_list if s not in ObjSymbol.ISSUED]

        # Check s_list after all type selection, issue filter -> raise error if no symbols found
        if not s_list:
            raise RuntimeError(f"No tradable symbols ! {FAILED_ICON_COLOR}")

        selected = []
        remaining_amount = self.amount

        while len(selected) < self.amount and s_list:
            # define random function
            random_func = random.sample if len(s_list) >= remaining_amount else random.choices
            # randomly select symbol
            batch = random_func(s_list, k=remaining_amount)
            # only take tradable symbols
            selected.extend([s for s in batch if self._is_tradable(s)])
            # check if selected symbols match input amount after filtering
            remaining_amount = self.amount - len(selected)
            # remove selected symbols out of original list
            s_list = [s for s in s_list if s not in batch]

        if not selected:
            raise RuntimeError(f"No tradable symbols found ! {FAILED_ICON_COLOR}")

        return selected[0] if self.amount == 1 else selected

    @classmethod
    def _select_symbol_current_type(cls, s_type) -> List[str]:
        """Get all symbols with specific symbol type"""
        s_list = [s.get("symbol") for s in cls.TYPE_SPECIFIC.get(s_type, [])]
        return s_list

    # ============ VALIDATION ============
    @classmethod
    def _is_tradable(cls, symbol) -> bool:
        """Check if input symbol is valid for trading"""
        symbol_details = cls.DETAILS.get(symbol)
        if not symbol_details:
            symbol_details = cls._get_symbol_details(symbol)
            cls.DETAILS[symbol] = symbol_details

        is_tradable = bool(symbol_details["enable"] and symbol_details["tradable"] and symbol_details["tradableExeMode"] and not symbol_details["holiday"])
        return is_tradable

    # ============ API INTEGRATION ============
    @classmethod
    def _get_all_symbols(cls):
        """Get all current available symbols, including all status"""
        from src.apis.api_client import APIClient
        resp = APIClient().market.get_watchlist_items(WatchListTab.ALL, get_symbols=False)
        return resp

    @classmethod
    def _get_symbol_details(cls, symbol):
        from src.apis.api_client import APIClient
        symbol_detail = APIClient().market.get_symbol_details(symbol)
        return symbol_detail

    @classmethod
    def _get_all_orders(cls):
        """Get all current market and pending orders for filter disabled symbols"""
        from src.apis.api_client import APIClient
        market_orders = APIClient().order.get_orders_details(order_type=OrderType.MARKET)
        pending_orders = APIClient().order.get_orders_details(order_type=OrderType.LIMIT)
        return market_orders + pending_orders

