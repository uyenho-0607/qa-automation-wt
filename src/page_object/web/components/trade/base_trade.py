from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import QUICK_WAIT
from src.data.enums import TradeType, BulkCloseOpts
from src.page_object.web.base_page import BasePage
from src.utils import DotDict
from src.utils.common_utils import data_testid, cook_element
from src.utils.format_utils import locator_format


class BaseTrade(BasePage):
    """Base class for trade-related components providing common trading functionality.
    
    This class extends BasePage to provide additional functionality specific to trading operations.
    It serves as the foundation for all trading-related components in the application.
    """

    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __live_price = (By.CSS_SELECTOR, data_testid('trade-live-{}-price'))  # buy or sell market price
    __oct_live_price = (
        By.XPATH, "//div[@data-testid='trade-button-oct-order-{}']/div[2]"
    )
    ##### One Click Trading Modal #####
    __btn_oct_confirm = (By.CSS_SELECTOR, data_testid('oct-modal-button-confirm'))

    ##### Trade Confirmation Modal #####
    __btn_trade_confirm = (By.CSS_SELECTOR, data_testid('trade-confirmation-button-confirm'))

    ##### Asset Tab #####
    __btn_confirm_delete_order = (By.CSS_SELECTOR, data_testid('confirmation-modal-button-submit'))  # delete order
    __btn_confirm_close_order = (By.CSS_SELECTOR, data_testid('close-order-button-submit'))
    __btn_cancel_close_order = (By.CSS_SELECTOR, data_testid('close-order-button-cancel'))
    __btn_cancel_delete_order = (By.CSS_SELECTOR, data_testid('confirmation-modal-button-cancel'))

    __btn_bulk_delete_confirm = (By.CSS_SELECTOR, data_testid('bulk-delete-modal-button-submit'))
    __btn_bulk_close_confirm = (By.CSS_SELECTOR, data_testid('bulk-close-modal-button-submit-{}'))
    __btn_bulk_close_cancel = (By.CSS_SELECTOR, data_testid('bulk-close-modal-button-cancel-all'))
    __btn_bulk_delete_cancel = (By.CSS_SELECTOR, data_testid('bulk-delete-modal-button-cancel'))

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

    # Asset tab relates
    def confirm_delete_order(self):
        self.actions.click(self.__btn_confirm_delete_order)

    def confirm_bulk_delete(self):
        """Confirm bulk delete action."""
        self.actions.click(self.__btn_bulk_delete_confirm)

    def confirm_close_order(self, force=False):
        """Confirm close order action."""
        if force:
            self.actions.click_by_offset(self.__btn_cancel_close_order, 100, 0)
            return

        self.actions.click(self.__btn_confirm_close_order)

    def confirm_bulk_close(self, option: BulkCloseOpts = BulkCloseOpts.ALL):
        """Click the bulk close confirm button."""
        self.actions.click(cook_element(self.__btn_bulk_close_confirm, locator_format(option)))

    def cancel_bulk_delete(self, timeout=QUICK_WAIT):
        self.actions.click(self.__btn_bulk_delete_cancel, timeout=timeout, raise_exception=False)

    def cancel_delete_order(self, timeout=QUICK_WAIT):
        self.actions.click(self.__btn_cancel_delete_order, timeout=timeout, raise_exception=False)

    def cancel_bulk_close(self, timeout=QUICK_WAIT):
        self.actions.click(self.__btn_bulk_close_cancel, timeout=timeout, raise_exception=False)

    def cancel_close_order(self, timeout=QUICK_WAIT):
        self.actions.click(self.__btn_cancel_close_order, timeout=timeout, raise_exception=False)
