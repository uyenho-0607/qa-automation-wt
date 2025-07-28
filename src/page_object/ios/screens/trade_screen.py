from src.core.actions.mobile_actions import MobileActions
from src.page_object.ios.base_screen import BaseScreen
from src.page_object.ios.components.modals.trading_modals import TradingModals
from src.page_object.ios.components.trade.asset_tab import AssetTab
from src.page_object.ios.components.trade.chart import Chart
from src.page_object.ios.components.trade.place_order_panel import PlaceOrderPanel
from src.page_object.ios.components.trade.watch_list import WatchList


class TradeScreen(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)
        self.watch_list = WatchList(actions)
        self.asset_tab = AssetTab(actions)
        self.place_order_panel = PlaceOrderPanel(actions)
        self.chart = Chart(actions)
        self.modals = TradingModals(actions)

    # ------------------------ LOCATORS ------------------------ #
    # ------------------------ ACTIONS ------------------------ #
    # ------------------------ VERIFY ------------------------ #
