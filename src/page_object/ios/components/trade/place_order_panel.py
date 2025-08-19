from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.page_object.ios.components.trade.base_trade import BaseTrade


class PlaceOrderPanel(BaseTrade):
    """
    A class representing the Place Order Panel in the trading interface.
    Handles all interactions with the order placement UI elements and operations.
    """

    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    # One-Click Trading elements
    __toggle_oct = (AppiumBy.ACCESSIBILITY_ID, 'toggle-oct')
    __toggle_oct_checked = (AppiumBy.ACCESSIBILITY_ID, 'toggle-oct-checked')

    # ------------------------ HELPER METHODS ------------------------ #
    # ------------------------ ACTIONS ------------------------ #
    # ------------------------ VERIFY ------------------------ #
