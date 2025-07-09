from src.core.actions.mobile_actions import MobileActions
from src.page_object.android.components.trade.base_trade import BaseTrade


class Chart(BaseTrade):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    # ------------------------ ACTIONS ------------------------ #
    # ------------------------ VERIFY ------------------------ #
