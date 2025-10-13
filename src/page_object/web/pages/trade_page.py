from src.core.actions.web_actions import WebActions
from src.data.enums import URLPaths
from src.data.objects.trade_obj import ObjTrade
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
    def verify_placed_order_data(trade_object: ObjTrade, api_data: dict):
        """Verify placed order against API data"""

        if not api_data:
            soft_assert(False, True, error_message="API order data is empty!")
            return

        actual = trade_object.api_data_format()
        expected = {k: v for k, v in api_data.items() if k in actual.keys()}

        # Round floats and handle volume mapping
        for key, value in expected.items():
            if isinstance(value, float):
                expected[key] = round(value, ndigits=ObjTrade.DECIMAL)
        expected["volume"] = api_data.get("lotSize")

        soft_assert(
            actual,
            expected,
            tolerance=0.5,
            tolerance_fields=trade_object.tolerance_fields(api_format=True) + ["openPrice"]
        )
