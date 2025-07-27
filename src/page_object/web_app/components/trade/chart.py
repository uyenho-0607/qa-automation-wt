from src.core.actions.web_actions import WebActions
from src.page_object.web_app.components.trade.base_trade import BaseTrade


class Chart(BaseTrade):
    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    # ------------------------ ACTIONS ------------------------ #
    # ------------------------ VERIFY ------------------------ #
