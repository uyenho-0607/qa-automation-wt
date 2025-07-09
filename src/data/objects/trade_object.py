from src.data.enums import TradeType, OrderType, Expiry, FillPolicy, AssetTabs
from src.data.objects.base_object import BaseObject
from src.data.project_info import ProjectConfig
from src.utils.format_utils import format_prices, remove_commas


class ObjectTrade(BaseObject):
    """A class representing a trade order with basic information.
    Attributes:
        - trade_type: TradeType (BUY, SELL, default is BUY)
        - order_type: OrderType (MARKET, LIMIT, STOP, STOP_LIMIT, default is MARKET)
        - symbol: str (symbol name)
    """

    # API Mapping dictionaries
    expiry_map = {
        Expiry.GOOD_TILL_DAY: "GTD",
        Expiry.GOOD_TILL_CANCELLED: "GTC",
        Expiry.SPECIFIED_DATE: "SPECIFIED_DAY",
        Expiry.SPECIFIED_DATE_TIME: "SPECIFIED_TIMESTAMP"
    }

    fill_policy_map = {
        FillPolicy.FILL_OR_KILL: 0,
        FillPolicy.IMMEDIATE_OR_CANCEL: 1,
        FillPolicy.RETURN: 2
    }

    order_type_map = {
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

    POINT_STEP = None
    CONTRACT_SIZE = None
    DECIMAL = None

    def __init__(
            self,
            trade_type: TradeType | str = TradeType.sample_values(),
            order_type: OrderType | str = OrderType.sample_values(),
            symbol: object = "",
            **kwargs
    ) -> None:
        super().__init__(**kwargs)

        # required/ basic attributes
        self.trade_type = trade_type
        self.order_type = order_type
        self.symbol = symbol

        # other additional attributes
        self.expiry = kwargs.get("expiry", Expiry.sample_values(self.order_type))
        self.fill_policy = kwargs.get("fill_policy", FillPolicy.sample_values(self.order_type))

        self._update_attributes(**kwargs)

    def __format_prices(self):

        entry_price, stop_loss, take_profit = self.get("entry_price"), self.get("stop_loss"), self.get("take_profit")
        format_num = self.POINT_STEP
        entry_price, stop_loss, take_profit = format_prices([entry_price, stop_loss, take_profit], self.DECIMAL)

        return entry_price, stop_loss, take_profit

    def trade_confirm_details(self):
        # format prices
        _, stop_loss, take_profit = self.__format_prices()

        order_type = self.trade_type.upper()
        if not self.order_type == OrderType.MARKET:
            order_type += f" {self.order_type.upper()}"

        expected = {
            "order_type": order_type,
            "symbol": self.symbol,
            "volume": self.get("volume"),
            "units": self.get("units"),
            "stop_loss": stop_loss or "--",
            "take_profit": take_profit or "--",
            "fill_policy": self.get("fill_policy"),
            "expiry": self.get("expiry")
        }

        return {k: v for k, v in expected.items() if v}

    def trade_edit_confirm_details(self):
        _, stop_loss, take_profit = self.__format_prices()

        expected = {
            "order_no": f"Order No. : {self.get('order_id', 0)}",
            "order_type": self.trade_type.upper() + (
                f" {self.order_type.upper()}" if self.order_type != OrderType.MARKET else ""),
            "symbol": self.symbol,
            "volume": self.get("volume"),
            "units": self.get("units"),
            "stop_loss": stop_loss or "--",
            "take_profit": take_profit or "--",
            "fill_policy": self.get("fill_policy"),
            "expiry": self.get("expiry")
        }

        return {k: v for k, v in expected.items() if v}

    def asset_item_data(self, tab: AssetTabs = None):
        # OPEN_POSITIONS: check: entry_price, order_type (BUY or SELL), stop_loss, take_profit, units, volume
        # PENDING_ORDER: check: entry_price, order_type (BUY or SELL), stop_loss, take_profit, units, volume, expiry
        # HISTORY: check: entry_price, order_type (BUY or SELL), stop_loss, take_profit, units, volume, status

        tab = tab or AssetTabs.get_tab(self.order_type)
        entry_price, stop_loss, take_profit = self.__format_prices()

        expected = {
            "trade_type": self.trade_type.upper(),
            "order_type": self.order_type.upper(),
            "volume": self.get("volume"),
            "units": self.get("units"),
            "expiry": self.get("expiry"),
            "entry_price": entry_price,
            "stop_loss": stop_loss or "--",
            "take_profit": take_profit or "--"
        }

        expected["order_type"] = expected.pop("trade_type", None)

        if tab == AssetTabs.PENDING_ORDER:
            expected["order_type"] = f"{self.trade_type.upper()} {self.order_type.upper()}"
            expected["fill_policy"] = self.get("fill_policy")

        if tab in [AssetTabs.HISTORY, AssetTabs.POSITIONS_HISTORY]:
            expected |= {"remarks": "--"}
            if not ProjectConfig.is_mt5():
                expected |= {"status": "CLOSED"}

        return {k: v for k, v in expected.items() if v}

    def api_data_format(self):
        actual = {
            'orderType': self.order_type_map.get((self.order_type, self.trade_type), None),
            'symbol': self.symbol,
            'tradeExpiry': self.expiry_map.get(self.expiry, None),
            'fillPolicy': self.fill_policy_map.get(self.fill_policy, 0),
            'volume': float(self.volume),
            'units': remove_commas(self.units, to_float=True),
            'stopLoss': remove_commas(self.stop_loss, to_float=True),
            'takeProfit': remove_commas(self.take_profit, to_float=True),
            'orderId': self.order_id
        }

        if self.order_type == OrderType.MARKET:
            actual["openPrice"] = remove_commas(self.entry_price, to_float=True)

        else:
            actual["price"] = remove_commas(self.entry_price, to_float=True)

        if self.order_type == OrderType.STOP_LIMIT:
            actual["priceTrigger"] = remove_commas(self.stop_limit_price, to_float=True)

        if self.stop_loss == "--":
            actual["stopLoss"] = 0

        if self.take_profit == "--":
            actual["takeProfit"] = 0

        return actual