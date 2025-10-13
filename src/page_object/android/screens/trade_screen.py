from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.objects.trade_obj import ObjTrade
from src.page_object.android.base_screen import BaseScreen
from src.page_object.android.components.modals.trading_modals import TradingModals
from src.page_object.android.components.trade.asset_tab import AssetTab
from src.page_object.android.components.trade.chart import Chart
from src.page_object.android.components.trade.place_order_panel import PlaceOrderPanel
from src.page_object.android.components.trade.watch_list import WatchList
from src.utils.assert_utils import soft_assert


class TradeScreen(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)
        self.watch_list = WatchList(actions)
        self.asset_tab = AssetTab(actions)
        self.place_order_panel = PlaceOrderPanel(actions)
        self.chart = Chart(actions)
        self.modals = TradingModals(actions)

    # ------------------------ LOCATORS ------------------------ #
    __symbol_overview_id = (AppiumBy.ID, "symbol-overview-id")

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
