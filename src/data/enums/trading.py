import random
from typing import Optional

from src.data.enums import BaseEnum
from src.data.project_info import ProjectConfig


class TradeType(BaseEnum):
    """Enum representing trade direction types."""
    BUY = "BUY"
    SELL = "SELL"


class TradeTab(BaseEnum):
    """Enum representing different trading tabs in the UI."""
    TRADE = "trade"
    OCT = "one-click-trading"
    SPECIFICATIONS = "specification"


class SLTPType(BaseEnum):
    """Enum representing Stop Loss/Take Profit calculation types."""
    PRICE = "price"
    POINTS = "points"


class OrderType(BaseEnum):
    """Enum representing different types of trading orders."""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop limit"  # MT5 only

    @classmethod
    def sample_values(cls):
        list_val = [cls.MARKET, cls.LIMIT, cls.STOP]
        if ProjectConfig.is_non_oms():
            list_val.append(cls.STOP_LIMIT)

        return random.choice(list_val)

    def is_market(self):
        return self == self.MARKET

    def is_stp_limit(self):
        return self == self.STOP_LIMIT


class Expiry(BaseEnum):
    """Enum representing order expiry types."""
    GOOD_TILL_CANCELLED = "Good Till Cancelled"
    GOOD_TILL_DAY = "Good Till Day"
    SPECIFIED_DATE = "Specified Date"  # MT5 only
    SPECIFIED_DATE_TIME = "Specified Date and Time"  # MT5 only

    @classmethod
    def sample_values(cls, order_type: OrderType) -> Optional[str]:
        """
        Get a random expiry type based on order type and server configuration.
        """
        if order_type == OrderType.MARKET:
            return None

        list_val = [cls.GOOD_TILL_CANCELLED, cls.GOOD_TILL_DAY]
        if ProjectConfig.is_non_oms():
            list_val = cls.list_values()

        return random.choice(list_val)


class FillPolicy(BaseEnum):
    """Enum representing order fill policies (MT5 only)."""
    FILL_OR_KILL = "Fill or Kill"
    IMMEDIATE_OR_CANCEL = "Immediate or Cancel"
    RETURN = "Return"

    @classmethod
    def sample_values(cls, order_type: OrderType) -> Optional[str]:
        """
        Get a random fill policy based on order type and server configuration.
        """
        if ProjectConfig.is_mt4():
            return None

        if order_type == OrderType.MARKET:
            return random.choice([cls.FILL_OR_KILL.value, cls.IMMEDIATE_OR_CANCEL.value])

        return cls.RETURN.value

    @classmethod
    def default_value(cls, order_type: OrderType):
        if order_type == OrderType.MARKET:
            return cls.FILL_OR_KILL

        return cls.RETURN

class ChartTimeframe(BaseEnum):
    one_min = "1min"
    five_min = "5min"
    fifteen_min = "15min"
    thirty_min = "30min"
    one_hour = "1h"
    four_hour = "4h"
    one_day = "1d"
    one_week = "1w"
    one_month = "1M"

    def get_timeframe(self):
        timeframe_map = {
            ChartTimeframe.one_min: "PERIOD_M1",
            ChartTimeframe.five_min: "PERIOD_M5",
            ChartTimeframe.fifteen_min: "PERIOD_M15",
            ChartTimeframe.thirty_min: "PERIOD_M30",
            ChartTimeframe.one_hour: "PERIOD_H1",
            ChartTimeframe.four_hour: "PERIOD_H4",
            ChartTimeframe.one_day: "PERIOD_D1",
            ChartTimeframe.one_week: "PERIOD_W1",
            ChartTimeframe.one_month: "PERIOD_MN1"
        }
        return timeframe_map[self]
