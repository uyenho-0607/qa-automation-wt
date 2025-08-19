from src.core.actions.mobile_actions import MobileActions
from src.page_object.ios.components.trade.base_trade import BaseTrade


class WatchList(BaseTrade):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    # ------------------------ ACTIONS ------------------------ 
    # ------------------------ VERIFY ------------------------ #
