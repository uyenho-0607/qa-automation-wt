from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.objects.trade_obj import ObjTrade
from src.page_object.web_app.base_page import BasePage
from src.page_object.web_app.components.modals.trading_modals import TradingModals
from src.page_object.web_app.components.trade.asset_tab import AssetTab
from src.page_object.web_app.components.trade.chart import Chart
from src.page_object.web_app.components.trade.place_order_panel import PlaceOrderPanel
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import data_testid


class TradePage(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)
        self.asset_tab = AssetTab(actions)
        self.place_order_panel = PlaceOrderPanel(actions)
        self.modals = TradingModals(actions)
        self.chart = Chart(actions)

    # ------------------------ LOCATORS ------------------------ #
    __symbol_overview_id = (By.CSS_SELECTOR, data_testid('symbol-overview-id'))

    # ------------------------ ACTIONS ------------------------ #
    # ------------------------ VERIFY ------------------------ #

    def verify_symbol_overview_id(self, symbol):
        actual_symbol = self.actions.get_text(self.__symbol_overview_id)
        soft_assert(actual_symbol, symbol)

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

