from enum import Enum

class AccountType(Enum):
    LIVE = 0
    DEMO = 1
    LIVE_CMS = 2


__all__ = ['AccountType']