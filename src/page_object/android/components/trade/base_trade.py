import time
from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import QUICK_WAIT, EXPLICIT_WAIT
from src.data.enums import TradeType
from src.page_object.android.base_screen import BaseScreen
from src.utils import DotDict
from src.utils.common_utils import resource_id, cook_element


class BaseTrade(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __live_price = (AppiumBy.XPATH, resource_id('trade-live-{}-price'))  # buy or sell market price
    __oct_live_price = (
        AppiumBy.XPATH, "//div[@data-testid='trade-button-oct-order-{}']/div[2]"
    )
    ##### One Click Trading Modal #####
    __btn_oct_confirm = (AppiumBy.XPATH, resource_id('oct-modal-button-confirm'))

    ##### Trade Confirmation Modal #####
    __btn_trade_confirm = (AppiumBy.XPATH, resource_id('trade-confirmation-button-confirm'))
    __btn_trade_close = (AppiumBy.XPATH, resource_id('trade-confirmation-button-close'))
    __btn_confirm_close_delete_order = (AppiumBy.XPATH, resource_id('close-order-button-submit'))
    __btn_cancel_trade = (AppiumBy.XPATH, "//android.widget.TextView[@text='Cancel']")

    # ------------------------ ACTIONS ------------------------ #
    def get_live_price(
            self, trade_type: TradeType, reverse=False, oct=False, trade_object: DotDict = None, timeout=QUICK_WAIT
    ) -> str:
        """Get the current live price for a given trade type.
        The price is displayed in the trading interface and is used for various trading operations.
        """

        if reverse:
            trade_type = TradeType.BUY if trade_type == TradeType.SELL else TradeType.SELL

        btn_price = self.__oct_live_price if oct else self.__live_price
        live_price = self.actions.get_text(cook_element(btn_price, trade_type.lower()), timeout=timeout)

        if trade_object:
            trade_object.current_price = live_price

        return live_price if live_price else 0

    # One Click Trading Modal Actions
    def agree_and_continue(self):
        """Confirm the one-click trading action."""
        self.actions.click(self.__btn_oct_confirm)

    # Trade Confirmation Modal Actions
    def confirm_trade(self):
        """Confirm the trade in the trade confirmation modal, give trade_object to update the current price for more precise"""
        self.actions.click(self.__btn_trade_confirm)

    def close_trade_confirm_modal(self, timeout=EXPLICIT_WAIT):
        time.sleep(1)
        self.actions.click(self.__btn_cancel_trade, timeout=timeout, raise_exception=False, show_log=False)


    def confirm_close_order(self):
        """Confirm close order action."""
        self.actions.click(self.__btn_confirm_close_delete_order)

    confirm_delete_order = confirm_close_order
