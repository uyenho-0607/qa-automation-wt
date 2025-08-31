from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import QUICK_WAIT
from src.data.enums import TradeType, OrderType
from src.data.objects.trade_obj import ObjTrade
from src.page_object.web_app.base_page import BasePage
from src.utils.common_utils import resource_id, cook_element, data_testid


class BaseTrade(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __live_price = (By.CSS_SELECTOR, data_testid('trade-live-{}-price'))  # buy or sell market price
    __oct_live_price = (By.XPATH, "//div[@data-testid='trade-button-oct-order-{}']/div[2]")
    __btn_oct_confirm = (By.CSS_SELECTOR, data_testid('oct-modal-button-confirm'))

    ##### Trade Confirmation Modal #####
    __btn_trade_confirm = (By.CSS_SELECTOR, data_testid('trade-confirmation-button-confirm'))
    __btn_trade_close = (AppiumBy.XPATH, resource_id('trade-confirmation-button-close'))  # cancel trade btn
    __btn_confirm_close_delete_order = (By.CSS_SELECTOR, data_testid('close-order-button-submit'))

    # ------------------------ ACTIONS ------------------------ #
    def get_live_price(self, trade_type: TradeType, oct=False) -> str:
        """Get the current live price for a given trade type.
        The price is displayed in the trading interface and is used for various trading operations.
        """
        btn_price = self.__oct_live_price if oct else self.__live_price
        live_price = self.actions.get_text(cook_element(btn_price, trade_type.lower()), timeout=QUICK_WAIT)
        return live_price if live_price else 0

    def get_current_price(self, trade_object: ObjTrade, timeout=QUICK_WAIT):
        """Get the current price for a placed order (reverse for order_type = Market).
        """
        trade_type, order_type = trade_object.trade_type, trade_object.order_type
        if order_type == OrderType.MARKET:
            trade_type = TradeType.BUY if trade_type == TradeType.SELL else TradeType.SELL

        current_price = self.actions.get_text(cook_element(self.__live_price, trade_type.lower()), timeout=timeout, raise_exception=False, show_log=False)
        trade_object.current_price = current_price

    # One Click Trading Modal Actions
    def agree_and_continue(self):
        """Confirm the one-click trading action."""
        self.actions.click(self.__btn_oct_confirm)

    # Trade Confirmation Modal Actions
    def confirm_trade(self):
        """Confirm the trade in the trade confirmation modal, give trade_object to update the current price for more precise"""
        self.actions.click(self.__btn_trade_confirm)

    def close_trade_confirm_modal(self):
        self.click_cancel_btn()

    def confirm_close_order(self):
        """Confirm close order action."""
        self.actions.click(self.__btn_confirm_close_delete_order)

    confirm_delete_order = confirm_close_order
