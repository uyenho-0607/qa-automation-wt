import builtins

from src.core.actions.mobile_actions import MobileActions
from src.page_object.android.screens.assets_screen import AssetsScreen
from src.page_object.android.screens.home_screen import HomeScreen
from src.page_object.android.screens.login_screen import LoginScreen
from src.page_object.android.screens.markets_screen import MarketsScreen
from src.page_object.android.screens.news_screen import NewsScreen
from src.page_object.android.screens.signal_screen import SignalScreen
from src.page_object.android.screens.trade_screen import TradeScreen


class AndroidContainer:
    def __init__(self, actions: MobileActions = None):
        # If no actions object is provided, try to create one from the global driver.
        if actions is None and getattr(builtins, "android_driver", None):
            actions = MobileActions(builtins.android_driver)

        if actions is None:
            raise ValueError(
                "AndroidContainer requires an 'actions' object or a global 'android_driver' to be available."
            )

        self.login_screen = LoginScreen(actions)
        self.home_screen = HomeScreen(actions)
        self.trade_screen = TradeScreen(actions)
        self.markets_screen = MarketsScreen(actions)
        self.assets_screen = AssetsScreen(actions)
        self.signal_screen = SignalScreen(actions)
        self.news_screen = NewsScreen(actions)
