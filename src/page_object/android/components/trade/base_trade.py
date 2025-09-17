from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import QUICK_WAIT, EXPLICIT_WAIT
from src.data.enums import TradeType, OrderType
from src.data.objects.trade_obj import ObjTrade
from src.page_object.android.base_screen import BaseScreen
from src.utils import DotDict
from src.utils.common_utils import cook_element
from src.utils.logging_utils import logger


class BaseTrade(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __live_price = (AppiumBy.ID, 'trade-live-{}-price')  # buy or sell market price
    __oct_live_price = (AppiumBy.XPATH, "//*[@resource-id='trade-button-oct-order-{}']/android.widget.TextView[2]")
    
    ##### One Click Trading Modal #####
    __btn_oct_confirm = (AppiumBy.ID, 'oct-modal-button-confirm')
    __btn_oct_cancel = (AppiumBy.ID, 'oct-modal-button-cancel')

    ##### Trade Confirmation Modal #####
    __btn_trade_confirm = (AppiumBy.ID, 'trade-confirmation-button-confirm')
    __btn_trade_close = (AppiumBy.ID, 'trade-confirmation-button-close')
    __btn_confirm_close_delete = (AppiumBy.ID, 'close-order-button-submit')
    __btn_cancel_close_delete = (AppiumBy.ID, 'close-order-button-cancel')

    # ------------------------ ACTIONS ------------------------ #
    def get_live_price(self, trade_type: TradeType, oct_mode=False, trade_object: ObjTrade = None) -> str:
        """Get the current live price for a given trade type.
        The price is displayed in the trading interface and is used for various trading operations.
        """
        btn_price = self.__oct_live_price if oct_mode else self.__live_price
        live_price = self.actions.get_text(cook_element(btn_price, trade_type.lower()))

        if trade_object:
            trade_object.current_price = live_price

        return live_price if live_price else 0

    def get_current_price(self, trade_object: DotDict, timeout=QUICK_WAIT):
        """Get the current price for a placed order (reverse for order_type = Market).
        """
        trade_type, order_type = trade_object.trade_type, trade_object.order_type
        if order_type == OrderType.MARKET:
            trade_type = TradeType.BUY if trade_type == TradeType.SELL else TradeType.SELL

        current_price = self.actions.get_text(cook_element(self.__live_price, trade_type.lower()), timeout=timeout, raise_exception=False, show_log=False)
        trade_object.current_price = current_price

    # One Click Trading Modal Actions
    def confirm_oct(self, confirm=True):
        """Confirm enable OCT or not"""
        logger.debug(f"- Confirm enable OCT: {confirm!r}")
        self.actions.click(self.__btn_oct_confirm if confirm else self.__btn_oct_cancel)

    # Trade Confirmation Modal Actions
    def confirm_trade(self, confirm=True, timeout=EXPLICIT_WAIT):
        """
        Confirm the trade in the trade confirmation modal.
        In case of canceling placing order -> set cancel = True
        """
        logger.debug(f"- Confirm place order: {confirm!r}")
        self.actions.click(self.__btn_trade_confirm if confirm else self.__btn_trade_close, timeout=timeout, raise_exception=not confirm, show_log=not confirm)

    def confirm_close_order(self, confirm=True):
        """Confirm close order action."""
        self.actions.click(self.__btn_confirm_close_delete if confirm else self.__btn_cancel_close_delete)

    confirm_delete_order = confirm_close_order
