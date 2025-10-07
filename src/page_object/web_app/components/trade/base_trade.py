import time

from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import QUICK_WAIT
from src.data.enums import TradeType, OrderType
from src.data.objects.trade_obj import ObjTrade
from src.page_object.web_app.base_page import BasePage
from src.utils.common_utils import cook_element, data_testid
from src.utils.logging_utils import logger


class BaseTrade(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __live_price = (By.CSS_SELECTOR, data_testid('trade-live-{}-price'))  # buy or sell market price
    __oct_live_price = (By.XPATH, "//div[@data-testid='trade-button-oct-order-{}']/div[2]")
    __btn_oct_confirm = (By.CSS_SELECTOR, data_testid('oct-modal-button-confirm'))
    __btn_oct_cancel = (By.CSS_SELECTOR, data_testid('oct-modal-button-cancel'))

    ##### Trade Confirmation Modal #####
    __btn_trade_confirm = (By.CSS_SELECTOR, data_testid('trade-confirmation-button-confirm'))
    __btn_trade_close = (By.CSS_SELECTOR, data_testid('trade-confirmation-button-close'))  # cancel trade btn
    __btn_confirm_close_delete = (By.CSS_SELECTOR, data_testid('close-order-button-submit'))
    __btn_cancel_close_delete = (By.CSS_SELECTOR, data_testid('close-order-button-cancel'))

    # ------------------------ ACTIONS ------------------------ #
    def get_live_price(self, trade_type: TradeType, oct_mode=False) -> str:
        """Get the current live price for a given trade type.
        The price is displayed in the trading interface and is used for various trading operations.
        """
        btn_price = self.__oct_live_price if oct_mode else self.__live_price
        live_price = self.actions.get_text(cook_element(btn_price, trade_type.lower()), timeout=QUICK_WAIT)
        return live_price if live_price else 0

    def get_current_price(self, trade_object: ObjTrade, oct_mode=False, timeout=QUICK_WAIT):
        """Get the current price for a placed order (reverse for order_type = Market).
        """
        trade_type = trade_object.trade_type
        if trade_object.order_type == OrderType.MARKET:
            trade_type = TradeType.BUY if trade_type == TradeType.SELL else TradeType.SELL

        current_price = self.actions.get_text(
            cook_element(self.__live_price if not oct_mode else self.__oct_live_price, trade_type.lower()),
            timeout=timeout, raise_exception=False, show_log=False
        )
        trade_object.current_price = current_price

    # One Click Trading Modal Actions
    def confirm_oct(self, confirm=True):
        """Confirm enable OCT or not"""
        time.sleep(0.5)
        logger.debug(f"- Confirm enable OCT: {confirm!r}")
        self.actions.click(self.__btn_oct_confirm if confirm else self.__btn_oct_cancel)

    # Trade Confirmation Modal Actions
    def confirm_trade(self, confirm=True):
        """
        Confirm the trade in the trade confirmation modal.
        In case of canceling placing order -> set confirm = False
        """
        logger.debug(f"- Confirm place order: {confirm!r}")
        self.actions.click(self.__btn_trade_confirm if confirm else self.__btn_trade_close)

    def confirm_close_order(self, confirm=True):
        """Confirm close order action."""
        logger.debug(f"- Confirm close/ delete order: {confirm}")
        self.actions.click(self.__btn_confirm_close_delete if confirm else self.__btn_cancel_close_delete)

    confirm_delete_order = confirm_close_order
