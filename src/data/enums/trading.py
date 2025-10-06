import random
from typing import Optional

from src.data.enums import BaseEnum
from src.data.project_info import RuntimeConfig


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
        if RuntimeConfig.is_non_oms():
            list_val.append(cls.STOP_LIMIT)

        return random.choice(list_val)

    def is_market(self):
        return self == self.MARKET

    def is_stp_limit(self):
        return self == self.STOP_LIMIT

    @classmethod
    def pending(cls):
        pending_orders = [cls.LIMIT, cls.STOP]
        if RuntimeConfig.is_non_oms():
            pending_orders += [cls.STOP_LIMIT]
        return pending_orders


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
        if RuntimeConfig.is_non_oms():
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
        if RuntimeConfig.is_mt4():
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
    one_min = "1-minute"
    five_min = "5-minute"
    ten_min = "10-minute"
    fifteen_min = "15-minute"
    twenty_min = "20-minute"
    thirty_min = "30-minute"
    one_hour = "1-hour"
    two_hour = "2-hour"
    three_hour = "3-hour"
    four_hour = "4-hour"
    six_hour = "6-hour"
    one_day = "1-day"
    one_week = "1-week"
    one_month = "1-month"

    @classmethod
    def list_values(cls, except_val=None):
        if RuntimeConfig.is_mt4():
            return cls.mt4_list()

        except_val = except_val if isinstance(except_val, list) else [except_val]
        return [item for item in ChartTimeframe if item not in except_val]

    @classmethod
    def mt4_list(cls):
        display_list = [
            cls.one_month,
            cls.fifteen_min,
            cls.one_hour,
            cls.thirty_min,
            cls.one_week,
            cls.one_min,
            cls.four_hour,
            cls.five_min,
            cls.one_day,
        ]
        return display_list

    @classmethod
    def crit_list(cls):
        return [cls.one_min, cls.five_min, cls.fifteen_min, cls.one_hour, cls.four_hour]

    def locator_map(self):
        if RuntimeConfig.is_web():
            map_dict = {
                self.one_min: "1min",
                self.five_min: "5min",
                self.ten_min: "10 minutes",
                self.fifteen_min: "15min",
                self.twenty_min: "20 minutes",
                self.thirty_min: "30min",
                self.one_hour: "1H",
                self.two_hour: "2 hours",
                self.three_hour: "3 hours",
                self.four_hour: "4H",
                self.six_hour: "6 hours",
                self.one_day: "1D",
                self.one_week: "1W",
                self.one_month: "1M"
            }
        else:
            map_dict = {
                self.one_min: "1m",
                self.five_min: "5m",
                self.ten_min: "10m",
                self.fifteen_min: "15m",
                self.twenty_min: "20m",
                self.thirty_min: "30m",
                self.one_hour: "1H",
                self.two_hour: "2H",
                self.three_hour: "3H",
                self.four_hour: "4H",
                self.six_hour: "6H",
                self.one_day: "1D",
                self.one_week: "1W",
                self.one_month: "1M"
            }
        return map_dict.get(self, self)

    def get_timeframe(self):
        timeframe_map = {
            ChartTimeframe.one_min: "PERIOD_M1",
            ChartTimeframe.five_min: "PERIOD_M5",
            ChartTimeframe.ten_min: "PERIOD_M10",
            ChartTimeframe.fifteen_min: "PERIOD_M15",
            ChartTimeframe.twenty_min: "PERIOD_M20",
            ChartTimeframe.thirty_min: "PERIOD_M30",
            ChartTimeframe.one_hour: "PERIOD_H1",
            ChartTimeframe.two_hour: "PERIOD_H2",
            ChartTimeframe.three_hour: "PERIOD_H3",
            ChartTimeframe.four_hour: "PERIOD_H4",
            ChartTimeframe.six_hour: "PERIOD_H6",
            ChartTimeframe.one_day: "PERIOD_D1",
            ChartTimeframe.one_week: "PERIOD_W1",
            ChartTimeframe.one_month: "PERIOD_MN1"
        }
        return timeframe_map[self]
