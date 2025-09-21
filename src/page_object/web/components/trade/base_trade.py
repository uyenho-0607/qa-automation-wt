from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import QUICK_WAIT, SHORT_WAIT
from src.data.enums import TradeType, BulkCloseOpts, OrderType
from src.data.objects.trade_obj import ObjTrade
from src.page_object.web.base_page import BasePage
from src.utils.common_utils import data_testid, cook_element
from src.utils.format_utils import locator_format
from src.utils.logging_utils import logger


class BaseTrade(BasePage):
    """Base class for trade-related components providing common trading functionality.
    
    This class extends BasePage to provide additional functionality specific to trading operations.
    It serves as the foundation for all trading-related components in the application.
    """

    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __live_price = (By.CSS_SELECTOR, data_testid('trade-live-{}-price'))  # buy or sell market price
    __oct_live_price = (By.XPATH, "//div[@data-testid='trade-button-oct-order-{}']/div[2]")
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
            self, trade_type: TradeType, oct=False, timeout=QUICK_WAIT
    ) -> str:
        """Get the current live price for a given trade type.
        The price is displayed in the trading interface and is used for various trading operations.
        """
        btn_price = self.__oct_live_price if oct else self.__live_price
        live_price = self.actions.get_text(cook_element(btn_price, trade_type.lower()), timeout=timeout)
        return live_price if live_price else 0

    def get_current_price(self, trade_type: TradeType, order_type: OrderType, timeout=SHORT_WAIT, oct_mode=False):
        """Get the current price for a placed order (reverse for order_type = Market).
        """
        btn_price = self.__oct_live_price if oct_mode else self.__live_price

        # reverse for order MARKET
        if order_type == OrderType.MARKET:
            trade_type = TradeType.BUY if trade_type == TradeType.SELL else TradeType.SELL

        current_price = self.actions.get_text(cook_element(btn_price, trade_type.lower()), timeout=timeout, show_log=False)
        return current_price

    # One Click Trading Modal Actions
    def agree_and_continue(self):
        """Confirm the one-click trading action."""
        logger.debug("- Click agree and continue button")
        self.actions.click(self.__btn_oct_confirm)

    # Trade Confirmation Modal Actions
    def confirm_trade(self):
        """Confirm the trade in the trade confirmation modal, give trade_object to update the current price for more precise"""
        if self.actions.is_element_displayed(self.__btn_trade_confirm):
            logger.debug("- Click confirm button")
            self.actions.click(self.__btn_trade_confirm)

    # Asset tab relates
    def confirm_delete_order(self):
        self.actions.click(self.__btn_confirm_delete_order)

    def confirm_bulk_delete(self):
        """Confirm bulk delete action."""
        self.actions.click(self.__btn_bulk_delete_confirm)

    def confirm_close_order(self, force=False):
        """Confirm close order action."""
        logger.debug("- Confirm close order")
        if force:
            self.actions.click_by_offset(self.__btn_cancel_close_order, 100, 0)
            return

        self.actions.click(self.__btn_confirm_close_order)

    def confirm_bulk_close(self, option: BulkCloseOpts = BulkCloseOpts.ALL):
        """Click the bulk close confirm button."""
        logger.debug("- Confirm bulk close order")
        self.actions.click(cook_element(self.__btn_bulk_close_confirm, locator_format(option)))

    def cancel_bulk_delete(self, timeout=QUICK_WAIT):
        self.actions.click(self.__btn_bulk_delete_cancel, timeout=timeout, raise_exception=False, show_log=False)

    def cancel_delete_order(self, timeout=QUICK_WAIT):
        self.actions.click(self.__btn_cancel_delete_order, timeout=timeout, raise_exception=False, show_log=False)

    def cancel_bulk_close(self, timeout=QUICK_WAIT):
        self.actions.click(self.__btn_bulk_close_cancel, timeout=timeout, raise_exception=False, show_log=False)

    def cancel_close_order(self, timeout=QUICK_WAIT):
        self.actions.click(self.__btn_cancel_close_order, timeout=timeout, raise_exception=False, show_log=False)
