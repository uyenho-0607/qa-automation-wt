import time

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import QUICK_WAIT
from src.data.enums import SLTPType, TradeType, OrderType, FillPolicy, Expiry
from src.page_object.ios.components.trade.base_trade import BaseTrade
from src.utils.common_utils import cook_element
from src.utils.format_utils import locator_format
from src.utils.logging_utils import logger


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
    __btn_pre_trade_details = (AppiumBy.ACCESSIBILITY_ID, "trade-button-pre-trade-details")

    __btn_trade_type = (AppiumBy.ACCESSIBILITY_ID, "trade-button-order-{}")  # buy / sell
    __drp_order_type = (AppiumBy.ACCESSIBILITY_ID, "trade-dropdown-order-type")
    __opt_order_type = (AppiumBy.ACCESSIBILITY_ID, "trade-dropdown-order-type-{}")  # market/ limit/ stop/ stop-limit
    __drp_fill_policy = (AppiumBy.ACCESSIBILITY_ID, "trade-dropdown-fill-policy")
    __opt_fill_policy = (AppiumBy.ACCESSIBILITY_ID, "trade-dropdown-fill-policy-{}")
    __drp_expiry = (AppiumBy.ACCESSIBILITY_ID, "trade-dropdown-expiry")
    __opt_expiry = (AppiumBy.ACCESSIBILITY_ID, "trade-dropdown-expiry-{}")
    __expiry_date = (AppiumBy.ACCESSIBILITY_ID, "trade-input-expiry-date")

    __txt_volume = (AppiumBy.ACCESSIBILITY_ID, "trade-input-volume")
    __lbl_units_volume = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeOther[`name BEGINSWITH 'Units'`]") # value of units/ volume (NOT the input value)
    __txt_price = (AppiumBy.ACCESSIBILITY_ID, "trade-input-price")
    __txt_stop_limit_price = (AppiumBy.ACCESSIBILITY_ID, "trade-input-stop-limit-price")
    __txt_sl = (AppiumBy.ACCESSIBILITY_ID, "trade-input-stoploss-{}")  # points or price
    __txt_tp = (AppiumBy.ACCESSIBILITY_ID, "trade-input-takeprofit-{}")
    __btn_place_order = (AppiumBy.ACCESSIBILITY_ID, "trade-button-order")
    __btn_cancel_order = (AppiumBy.ACCESSIBILITY_ID, "trade-button-cancel")

    # ------------------------ HELPER METHODS ------------------------ #
    def _get_input_sl(self):
        locator = cook_element(self.__txt_sl, SLTPType.PRICE.lower())
        self.actions.click(locator)
        time.sleep(0.5)
        value = self.actions.get_attribute(locator, "value")
        logger.debug(f"- Input SL as Price: {value!r}")
        return value

    def _get_input_tp(self):
        locator = cook_element(self.__txt_tp, SLTPType.PRICE.lower())
        self.actions.click(locator)
        time.sleep(0.5)
        value = self.actions.get_attribute(locator, "value")
        logger.debug(f"- Input TP as Price: {value!r}")
        return value

    def _get_vol_info_value(self):
        value = self.actions.get_attribute(self.__lbl_units_volume, "label").split(" ")[-1]
        logger.debug(f"- Units is: {value!r}")
        return value

    # ------------------------ ACTIONS ------------------------ #
    def toggle_oct(self, enable=True, submit=True):
        # Check current OCT state
        is_enabled = self.actions.is_element_displayed(self.__toggle_oct_checked, timeout=QUICK_WAIT)
        if is_enabled != enable:
            self.actions.click(self.__toggle_oct if enable else self.__toggle_oct_checked)

            if enable:
                self.confirm_oct(submit)

    def open_pre_trade_details(self):
        logger.debug("- Open pre-trade details")
        self.actions.click(self.__btn_pre_trade_details)

    def _select_trade_type(self, trade_type: TradeType):
        logger.debug(f"- Select trade type: {trade_type.value.title()!r}")
        self.actions.click(cook_element(self.__btn_trade_type, trade_type.lower()))

    def _select_order_type(self, order_type: OrderType, retries=3):
        # check current selected order_type
        if retries <= 0:
            logger.warning(f"- Failed to select order type: {order_type.value.title()} after retries")
            return

        cur_order_type = self.actions.get_attribute(self.__drp_order_type, "label")
        cur_order_type = " ".join(cur_order_type.split(" ")[:-1])  # handle unexpected icon
        is_select = order_type.lower() == cur_order_type.lower()

        if is_select:
            logger.debug(f"- Order Type: {order_type.value.title()!r} selected")
            return

        logger.info(f"- Selecting order type: {order_type.value.title()!r}")
        self.actions.click(self.__drp_order_type)
        self.actions.click(cook_element(self.__opt_order_type, locator_format(order_type)))

        return self._select_order_type(order_type, retries - 1)

    def _select_fill_policy(self, fill_policy: FillPolicy, retries=3):
        # check current fill policy
        if retries <= 0:
            logger.warning(f"- Failed to select fill policy: {fill_policy.value.title()!r} after retries")
            return

        cur_fp = self.actions.get_attribute(self.__drp_fill_policy, "label")
        cur_fp = " ".join(cur_fp.split(" ")[:-1])
        is_select = fill_policy.lower() == cur_fp

        if is_select:
            logger.debug(f"- Fill Policy: {fill_policy.value.title()!r} selected")
            return

        logger.info(f"- Selecting fill policy: {fill_policy.value.title()!r}")
        self.actions.click(self.__drp_fill_policy)
        self.actions.click(cook_element(self.__opt_fill_policy, locator_format(fill_policy)))
        return self._select_fill_policy(fill_policy, retries - 1)

    def _select_expiry(self, expiry: Expiry, retries=3):
        # check current selected expiry
        if retries <= 0:
            logger.warning(f"- Failed to select expiry: {expiry.value.title()!r} after retries")
            return

        cur_expiry = self.actions.get_attribute(self.__drp_expiry, "label")
        cur_expiry = " ".join(cur_expiry.split(" ")[:-1])
        is_select = cur_expiry.lower() == expiry.lower()

        if is_select:
            logger.debug(f"- Expiry: {expiry.value.title()!r} selected")
            return

        logger.info(f"- Selecting expiry: {expiry.value.title()!r}")
        self.actions.click(self.__drp_expiry)
        self.actions.click(cook_element(self.__opt_expiry, locator_format(expiry)))

        return self._select_expiry(expiry, retries - 1)

    def _click_place_order_btn(self):
        logger.debug("- Click place order button")
        self.actions.click(self.__btn_place_order)

    def _click_cancel_order_btn(self):
        logger.debug("- Click cancel order button")
        self.actions.click(self.__btn_cancel_order)

    def _input_sl(self, value, sl_type: SLTPType):
        locator = cook_element(self.__txt_sl, sl_type.lower())
        logger.debug(f"- Input SL - {sl_type.value}: {value!r}")
        self.actions.send_keys(locator, value)

    def _input_tp(self, value, tp_type: SLTPType):
        locator = cook_element(self.__txt_tp, tp_type.lower())
        logger.debug(f"- Input TP - {tp_type.value}: {value!r}")
        self.actions.send_keys(locator, value)

    def _input_volume(self, value):
        logger.debug(f"- Input Volume: {value!r}")
        self.actions.send_keys(self.__txt_volume, value)

    def _input_price(self, value):
        logger.debug(f"- Input Price: {value!r}")
        self.actions.send_keys(self.__txt_price, value)

    def _input_stop_limit_price(self, value):
        logger.debug(f"- Input Stop Limit Price: {value!r}")
        self.actions.send_keys(self.__txt_stop_limit_price, value)

    def place_order(self):
        ...

    def place_oct_order(self):
        ...

    # ------------------------ VERIFY ------------------------ #

    def verify_oct_mode(self, enable=True):
        ...
