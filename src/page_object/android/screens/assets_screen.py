from src.core.actions.mobile_actions import MobileActions
from src.page_object.android.base_screen import BaseScreen
from src.page_object.android.components.modals.trading_modals import TradingModals
from src.page_object.android.components.trade.asset_tab import AssetTab


class AssetsScreen(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)
        self.asset_tab = AssetTab(actions)
        self.trading_modals = TradingModals(actions)

    # ------------------------ LOCATORS ------------------------ #

    # ------------------------ ACTIONS ------------------------ #

    # ------------------------ VERIFY ------------------------ #
