import random
from enum import Enum


class BaseEnum(str, Enum):
    """Base enum class that provides string representation functionality."""

    def __str__(self):
        return self.value

    @classmethod
    def list_values(cls, except_val=None):
        except_val = except_val if isinstance(except_val, list) else [except_val]
        return [item for item in cls if item not in except_val]

    @classmethod
    def sample_values(cls, amount=1, except_val=None):
        res = random.sample(cls.list_values(except_val), k=amount)
        return res[0] if amount == 1 else res

    @classmethod
    def random_values(cls, amount=1, except_val=None):
        res = random.choices(cls.list_values(except_val), k=amount)
        return res[0] if amount == 1 else res


class URLSites(BaseEnum):
    """Enum representing different site types in the application."""
    MEMBER_SITE = "base"
    ADMIN_PORTAL = "bo"
    ROOT_ADMIN = "root"


class URLPaths(BaseEnum):
    """Enum representing different URL paths in the application."""
    LOGIN = "login"
    HOME = "home"
    TRADE = ""
    ASSETS = "assets"
    SIGNAL = "signal"
    MARKETS = "market"
    CALENDAR = "calendar"
    NEWS = "news"
    COPY_TRADE = "copytrade"
    EDUCATION = "education"


class Client(BaseEnum):
    """Enum representing different client platforms."""
    LIRUNEX = "lirunex"
    TRANSACT_CLOUD = "transactCloud"
    DECODE = "dcodemarkets"


class Server(BaseEnum):
    """Enum representing different trading servers."""
    MT4 = "mt4"
    MT5 = "mt5"


class NotificationTab(BaseEnum):
    """Enum representing different notification tabs"""
    ORDER = "Order"
    SYSTEM = "System"
    INFORMATION = "Information"
