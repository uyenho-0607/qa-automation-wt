import random
from typing import Dict, Any, Optional, Tuple

from src.data.consts import get_symbols, get_symbol_details
from src.data.enums import SLTPType
from src.data.enums import TradeType, OrderType, Expiry, FillPolicy, AssetTabs
from src.data.objects.base_obj import BaseObj
from src.data.project_info import RuntimeConfig
from src.utils.format_utils import format_str_prices, remove_comma, get_decimal, is_integer


class ObjTrade(BaseObj):
    """A class representing a trade order with basic information.
    
    Attributes:
        - trade_type: TradeType (BUY, SELL, default is BUY)
        - order_type: OrderType (MARKET, LIMIT, STOP, STOP_LIMIT, default is MARKET)
        - symbol: str (symbol name)
    """

    POINT_STEP = None
    CONTRACT_SIZE = None
    DECIMAL = None
    STOP_LEVEL = 10

    def __init__(
            self,
            trade_type: TradeType | str = TradeType.sample_values(),
            order_type: OrderType | str = OrderType.sample_values(),
            symbol: str = "",
            expiry: Expiry | str = None,
            fill_policy: FillPolicy | str = None,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)

        self.trade_type = trade_type
        self.order_type = order_type
        self.symbol = symbol or random.choice(get_symbols())
        self.expiry = expiry or Expiry.sample_values(self.order_type)
        self.fill_policy = fill_policy or FillPolicy.sample_values(self.order_type)
        self._update_symbol_details(self.symbol)
        self._update_attributes(**kwargs)

    @staticmethod
    def _update_symbol_details(symbol):
        symbol_details = get_symbol_details(symbol)
        ObjTrade.POINT_STEP = symbol_details["point_step"]
        ObjTrade.DECIMAL = symbol_details["decimal"]

    @classmethod
    def get_expiry_map(cls, expiry: Expiry | str) -> str:
        """Get expiry mapping for API calls."""
        map_dict = {
            Expiry.GOOD_TILL_DAY: "GTD",
            Expiry.GOOD_TILL_CANCELLED: "GTC",
            Expiry.SPECIFIED_DATE: "SPECIFIED_DAY",
            Expiry.SPECIFIED_DATE_TIME: "SPECIFIED_TIMESTAMP"
        }

        return map_dict.get(expiry, None)

    @classmethod
    def get_fill_policy_map(cls, fill_policy: FillPolicy | str) -> int:
        """Get fill policy mapping for API calls."""
        map_dict = {
            FillPolicy.FILL_OR_KILL: 0,
            FillPolicy.IMMEDIATE_OR_CANCEL: 1,
            FillPolicy.RETURN: 2
        }
        return map_dict.get(fill_policy, 0)

    @classmethod
    def get_order_type_map(cls, order_type: OrderType | str, trade_type: TradeType | str) -> int:
        """Get order type mapping for API calls."""
        map_dict = {
            # Market orders
            (OrderType.MARKET, TradeType.BUY): 0,
            (OrderType.MARKET, TradeType.SELL): 1,
            # Limit orders
            (OrderType.LIMIT, TradeType.BUY): 2,
            (OrderType.LIMIT, TradeType.SELL): 3,
            # Stop orders
            (OrderType.STOP, TradeType.BUY): 4,
            (OrderType.STOP, TradeType.SELL): 5,
            # Stop Limit orders
            (OrderType.STOP_LIMIT, TradeType.BUY): 8,
            (OrderType.STOP_LIMIT, TradeType.SELL): 9
        }
        return map_dict.get((order_type, trade_type), 0)

    def _get_order_type(self) -> str:
        """Return order type in correct format for UI display."""
        return self.trade_type.upper() + (f" {self.order_type.upper()}" if self.order_type != OrderType.MARKET else "")

    def _format_prices(self) -> Tuple[str, str, str, str]:
        """Format all price values to string format with proper decimal places and commas."""
        prices = [self.get("stop_limit_price"), self.get("entry_price"), self.get("stop_loss"), self.get("take_profit")]
        return format_str_prices(prices, self.DECIMAL)

    def _format_volume_units(self) -> None:
        """Format volume and units to correct string format."""
        vol_decimal = 0
        units_decimal = 0

        if not is_integer(self.units) or int(self.units) < float(self.units):
            # remain volume unchanged as volume is float value
            units_decimal = get_decimal(self.units)

        if not is_integer(self.volume) or int(self.volume) < float(self.volume):
            # remain volume unchanged as volume is float value
            vol_decimal = get_decimal(self.volume)

        units = format_str_prices(self.units, units_decimal)
        volume = format_str_prices(self.volume, vol_decimal)

        self._update_attributes(units=units, volume=volume)

    def tolerance_fields(self, api_format=False) -> list:
        """Get fields that require tolerance checking."""
        tolerance_fields = ["open_date", "close_date", "close_price", "current_price"]
        if self.get("sl_type") == SLTPType.POINTS:
            tolerance_fields += ["stop_loss" if not api_format else "stopLoss"]

        if self.get("tp_type") == SLTPType.POINTS:
            tolerance_fields += ["take_profit" if not api_format else "takeProfit"]

        if self.order_type == OrderType.MARKET:
            tolerance_fields += ["entry_price"]

        return tolerance_fields

    def _build_base_details(self, include_order_id: bool = False) -> Dict[str, Any]:
        """Build base details dictionary for various trade confirmations."""
        # Format prices and volume
        stp_limit_price, entry_price, stop_loss, take_profit = self._format_prices()
        self._format_volume_units()
        details = {}

        # Add order ID if requested
        if include_order_id:
            details["order_no"] = f"Order No. : {self.get('order_id', 0)}"

        details |= {
            "order_type": self._get_order_type(),
            "symbol": self.symbol,
            "volume": self.volume,
            "units": self.units,
            "stop_loss": stop_loss or "--",
            "take_profit": take_profit or "--",
            "fill_policy": self.fill_policy,
            "expiry": self.expiry
        }

        return {k: v for k, v in details.items() if v}

    def trade_confirm_details(self) -> Dict[str, Any]:
        """Get trade confirmation details for UI verification."""
        stp_limit_price, entry_price, stop_loss, take_profit = self._format_prices()
        details = self._build_base_details()
        # Add entry price for non-market orders
        if not self.order_type == OrderType.MARKET:
            details["entry_price"] = entry_price

        # Add stop limit price for stop limit orders
        if self.order_type.is_stp_limit():
            details["stop_limit_price"] = stp_limit_price

        return details

    def trade_edit_confirm_details(self) -> Dict[str, Any]:
        """Get trade edit confirmation details for UI verification."""
        return self._build_base_details(include_order_id=True)

    def asset_item_data(self, tab: Optional[AssetTabs] = None) -> Dict[str, Any]:
        """Get asset item data for different tabs."""
        stp_limit_price, entry_price, stop_loss, take_profit = self._format_prices()
        self._format_volume_units()
        tab = tab or AssetTabs.get_tab(self.order_type)

        details = {
            "open_date": self.get("open_date"),
            "close_date": self.get("close_date") if tab.is_history() else None,
            "order_type": self._get_order_type(),
            "volume": self.volume if RuntimeConfig.is_mt4() or tab != AssetTabs.PENDING_ORDER else f"{self.volume} / 0",
            "units": self.units,
            "current_price": self.get("current_price"),
            "entry_price": entry_price,
            "stop_loss": stop_loss or "--",
            "take_profit": take_profit or "--",
            "expiry": self.expiry,
            "remarks": "--" if tab.is_history() else None,
            "status": "CLOSED" if tab.is_history() and RuntimeConfig.is_mt4() else None
        }

        # Add tab-specific details
        if tab == AssetTabs.PENDING_ORDER:
            details["pending_price" if RuntimeConfig.is_web() else "stop_limit_price"] = (
                None if RuntimeConfig.is_mt4() else (stp_limit_price if self.order_type.is_stp_limit() else "--")
            )

            # todo: re-check with QA: mobile trade confirm does not display fill_policy
            if RuntimeConfig.is_web():
                details["fill_policy"] = self.fill_policy

        if tab.is_history():
            details["close_price"] = details.pop("current_price", None)

        return {k: v for k, v in details.items() if v}

    def api_data_format(self) -> Dict[str, Any]:
        """Format trade data for API calls."""
        api_data = {
            'orderType': self.get_order_type_map(self.order_type, self.trade_type),
            'symbol': self.symbol,
            'tradeExpiry': self.get_expiry_map(self.expiry),
            'fillPolicy': self.get_fill_policy_map(self.fill_policy),
            'volume': float(str(self.volume).split(" / ")[0]),
            'units': remove_comma(self.units),
            'stopLoss': remove_comma(self.stop_loss),
            'takeProfit': remove_comma(self.take_profit),
            'orderId': self.order_id
        }

        # Add price based on order type
        api_data |= {"openPrice" if self.order_type == OrderType.MARKET else "price": remove_comma(self.entry_price)}

        # Add stop limit price for stop limit orders
        if self.order_type == OrderType.STOP_LIMIT:
            api_data["priceTrigger"] = remove_comma(self.get("stop_limit_price", self.get("pending_price")))

        return api_data
