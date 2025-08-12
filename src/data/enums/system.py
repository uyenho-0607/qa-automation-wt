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


class URLSites(BaseEnum):
    """Enum representing different site types in the application."""
    MEMBER_SITE = "base"
    ADMIN_PORTAL = "bo"
    ROOT_ADMIN = "root"


class Client(BaseEnum):
    """Enum representing different client platforms."""
    LIRUNEX = "lirunex"
    TRANSACT_CLOUD = "transactCloud"


class Server(BaseEnum):
    """Enum representing different trading servers."""
    MT4 = "mt4"
    MT5 = "mt5"
