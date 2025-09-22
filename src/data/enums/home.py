import random

from src.data.enums import BaseEnum
from src.data.project_info import RuntimeConfig
from src.utils.format_utils import locator_format


class Features(BaseEnum):
    HOME = "Home"  # Mobile
    TRADE = "Trade"
    MARKETS = "Markets"
    ASSETS = "Assets"
    SIGNAL = "Signal"
    CALENDAR = "Calendar"
    NEWS = "News"
    EDUCATION = "Education"

    @classmethod
    def home_nav_list(cls):
        return [cls.SIGNAL, cls.CALENDAR, cls.NEWS, cls.EDUCATION]

    @classmethod
    def side_bar_list(cls):
        return [cls.HOME, cls.MARKETS, cls.TRADE, cls.ASSETS]

class AccSummary(BaseEnum):
    BALANCE = "Account Balance"
    MARGIN_USED = "Margin Used"
    EQUITY = "Equity"
    MARGIN_LEVEL = "Margin Level"
    FREE_MARGIN = "Free Margin"
    STOP_OUT_LEVEL = "Stop Out Level"
    PROFIT_LOSS = "Profit/Loss"
    MARGIN_CALL = "Margin Call Level"

    @classmethod
    def checkbox_list(cls):
        return [cls.BALANCE, cls.MARGIN_USED, cls.EQUITY, cls.MARGIN_LEVEL, cls.FREE_MARGIN, cls.PROFIT_LOSS]

    @classmethod
    def note_list(cls):
        return [cls.MARGIN_CALL, cls.STOP_OUT_LEVEL]


class SettingOptions(BaseEnum):
    LINK_SWITCH_TO_LIVE = "Link Switch To Live"
    LINK_SWITCH_TO_DEMO = "Link Switch To Demo"
    SWITCH_TO_LIVE = "Switch To Live"
    SWITCH_TO_DEMO = "Switch To Demo"
    OPEN_DEMO_ACCOUNT = "Open Demo Account"
    CHANGE_PASSWORD = "Change Password"
    CHANGE_LANGUAGE = "Language"
    LINKED_DEVICES = "Linked Device"
    CONTACT_INFORMATION = "Contact Information"
    LOGOUT = "Logout"
    NOTIFICATION_SETTING = "Notification Setting"

    # mobile only
    ONE_CLICK_TRADING = "oct"
    APPEARANCE = "appearance"


class ThemeOptions(BaseEnum):
    DARK = "dark"
    LIGHT = "light"
    SYSTEM = "system"


class NotiSettingsOpts(BaseEnum):
    MARGIN_CALL = "Margin Call"
    MARGIN_STOP_OUT = "Margin Stop Out"
    NEW_FAVOURITE_SIGNAL = "New Favourite Signal"
    NEW_LOGINS = "New Logins"


class WatchListTab(BaseEnum):
    """Enum representing different watchlist categories."""

    ALL = "All"
    FAVOURITES = "Favourites"
    TOP_PICKS = "Top Picks"
    TOP_GAINER = "Top Gainers"
    TOP_LOSER = "Top Losers"
    COMMODITIES = "Commodities"
    CRYPTO = "Crypto"
    FOREX = "Forex"
    INDEX = "Index"
    SHARES = "Shares"

    @classmethod
    def list_values(cls, except_val=None):
        except_val = except_val if isinstance(except_val, list) else [except_val]
        lis_val = [item for item in cls if item not in except_val]
        if RuntimeConfig.is_non_oms():
            lis_val.remove(cls.SHARES)
        return lis_val

    @classmethod
    def random_values(cls, amount=1, except_val=None):
        lis_val = cls.list_values(except_val=except_val)
        return random.sample(lis_val, k=amount)

    def get_tab(self, page=None):
        """
        Get locator tab
        Note: In case Page is Trade: FAVOURITES = "my-watchlist", Market: "favourites"
        """
        page = page or Features.TRADE

        special_cases = {
            self.FAVOURITES: "my-watchlist" if page != Features.MARKETS else self.lower(),
            self.TOP_PICKS: "popular",
            self.COMMODITIES: "comms",
            self.TOP_GAINER: "top-gainer",
            self.TOP_LOSER: "top-loser"
        }

        return special_cases.get(self, locator_format(self))

    @classmethod
    def parent_tabs(cls):
        return [cls.ALL, cls.FAVOURITES, cls.TOP_PICKS, cls.TOP_GAINER, cls.TOP_LOSER]

    @classmethod
    def sub_tabs(cls):
        if RuntimeConfig.is_non_oms() and RuntimeConfig.env != "prod":
            return [cls.COMMODITIES, cls.CRYPTO, cls.FOREX, cls.INDEX]

        return [cls.SHARES, cls.FOREX, cls.COMMODITIES, cls.INDEX, cls.CRYPTO]

    @classmethod
    def all_tabs(cls):
        return cls.parent_tabs() + cls.sub_tabs()


class MarketsSection(BaseEnum):
    MY_TRADE = "My Trade"
    TOP_PICKS = "Top Picks"
    TOP_GAINER = "Top Gainer"
    SIGNAL = "Signal"
    NEWS = "News"

    def symbol_row(self):
        map_dict = {
            self.MY_TRADE: "portfolio-row",
            self.SIGNAL: "signal-row",
        }
        return map_dict.get(self, self)


class SignalTab(BaseEnum):
    FAVOURITE = "Favourite"
    SIGNAL_LIST = "All"
    FAVOURITE_SIGNAL = "Favourite Signals"
    SIGNAL_LIST_TAB = "Signal List"
