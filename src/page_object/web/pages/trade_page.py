from src.core.actions.web_actions import WebActions
from src.data.enums import URLPaths
from src.data.objects.trade_object import ObjectTrade
from src.page_object.web.base_page import BasePage
from src.page_object.web.components.modals.trading_modals import TradingModals
from src.page_object.web.components.trade.asset_tab import AssetTab
from src.page_object.web.components.trade.chart import Chart
from src.page_object.web.components.trade.place_order_panel import PlaceOrderPanel
from src.page_object.web.components.trade.watch_list import WatchList
from src.utils.assert_utils import soft_assert


class TradePage(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)
        self.watch_list = WatchList(actions)
        self.asset_tab = AssetTab(actions)
        self.place_order_panel = PlaceOrderPanel(actions)
        self.chart = Chart(actions)
        self.modals = TradingModals(actions)

    # ------------------------ LOCATORS ------------------------ #

    # ------------------------ ACTIONS ------------------------ #
    def verify_page_url(self):
        super().verify_page_url(URLPaths.TRADE)

    # ------------------------ VERIFY ------------------------ #

    @staticmethod
    def verify_placed_order_data(trade_object: ObjectTrade, api_data: dict):
        """Verify placed order against API data"""
        # handle actual
        actual = trade_object.api_data_format()

        # handle expected
        expected = {k: v for k, v in api_data.items() if k in actual.keys()}
        expected["volume"] = api_data["lotSize"]

        soft_assert(actual, expected, tolerance=0.01, tolerance_fields=["openPrice"])
