import builtins

from src.core.actions.web_actions import WebActions
from src.page_object.web_app.pages.assets_page import AssetsPage
from src.page_object.web_app.pages.home_page import HomePage
from src.page_object.web_app.pages.login_page import LoginPage
from src.page_object.web_app.pages.markets_page import MarketsPage
from src.page_object.web_app.pages.signal_page import SignalPage
from src.page_object.web_app.pages.trade_page import TradePage


class WebAppContainer:
    def __init__(self, actions: WebActions = None):
        # If no actions object is provided, try to create one from the global driver.
        if actions is None and getattr(builtins, "web_driver", None):
            actions = WebActions(builtins.web_driver)

        if actions is None:
            raise ValueError(
                "WebAppContainer requires an 'actions' object or a global 'web_driver' to be available."
            )

        self.login_page = LoginPage(actions)
        self.home_page = HomePage(actions)
        self.trade_page = TradePage(actions)
        self.markets_page = MarketsPage(actions)
        self.assets_page = AssetsPage(actions)
        self.signal_page = SignalPage(actions)
