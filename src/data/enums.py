from enum import Enum


class BaseEnum(str, Enum):
    """Base enum class that provides string representation functionality."""

    def __str__(self):
        return self.value

    @classmethod
    def list_values(cls, except_val=None):
        except_val = except_val if isinstance(except_val, list) else [except_val]
        return [item for item in cls if item not in except_val]


class AccountType(BaseEnum):
    LIVE = "live"
    DEMO = "demo"
    CRM = "crm"


class Client(BaseEnum):
    """Enum representing different client platforms."""
    LIRUNEX = "lirunex"
    TRANSACT_CLOUD = "transactCloud"


class Server(BaseEnum):
    """Enum representing different trading servers."""
    MT4 = "mt4"
    MT5 = "mt5"


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