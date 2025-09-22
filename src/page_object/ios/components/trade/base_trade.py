from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import SHORT_WAIT, QUICK_WAIT
from src.data.enums import TradeType, OrderType
from src.data.objects.trade_obj import ObjTrade
from src.page_object.ios.base_screen import BaseScreen
from src.utils.common_utils import cook_element
from src.utils.logging_utils import logger


class BaseTrade(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __live_price = (AppiumBy.ACCESSIBILITY_ID, "trade-live-{}-price")  # buy or sell market price
    __oct_live_price = (AppiumBy.ACCESSIBILITY_ID, "trade-button-oct-order-{}")
    __oct_confirm_btn = (AppiumBy.ACCESSIBILITY_ID, "oct-modal-button-confirm")
    __cot_cancel_btn = (AppiumBy.ACCESSIBILITY_ID, "oct-modal-button-cancel")
    __btn_confirm_trade = (AppiumBy.ACCESSIBILITY_ID, "trade-confirmation-button-confirm")
    __btn_cancel_trade = (AppiumBy.ACCESSIBILITY_ID, "trade-confirmation-button-close")

    # ------------------------ ACTIONS ------------------------ #
    def get_live_price(self, trade_type: TradeType, oct_mode=False, trade_object: ObjTrade = None) -> str:
        """Get the current live price for a given trade type.
        The price is displayed in the trading interface and is used for various trading operations.
        """
        btn_price = self.__oct_live_price if oct_mode else self.__live_price
        price = self.actions.get_attribute(cook_element(btn_price, trade_type.lower()), "label")
        price = price.split(" ")[-1] or 0

        if trade_object:
            trade_object.current_price = price

        return price

    def get_current_price(self, trade_object: ObjTrade, timeout=SHORT_WAIT, oct_mode=False):
        """Get the current price for a placed order (reverse for order_type = Market).
        """
        btn_price = self.__oct_live_price if oct_mode else self.__live_price
        trade_type = trade_object.trade_type

        # reverse for order MARKET
        if trade_object.order_type == OrderType.MARKET:
            trade_type = TradeType.BUY if trade_object.trade_type == TradeType.SELL else TradeType.SELL

        current_price = self.actions.get_attribute(
            cook_element(btn_price, trade_type.lower()), "label", timeout=timeout, raise_exception=False, show_log=False
        )

        trade_object.current_price = current_price

    def confirm_oct(self, confirm=True):
        logger.debug(f"- Confirm enable OCT: {confirm!r}")
        self.actions.click(self.__oct_confirm_btn if confirm else self.__cot_cancel_btn)

    def confirm_trade(self, confirm=True):
        logger.debug(f"- Confirm place order: {confirm!r}")
        self.actions.click(self.__btn_confirm_trade if confirm else self.__btn_cancel_trade)
