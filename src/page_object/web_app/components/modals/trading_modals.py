import time

from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import QUICK_WAIT, SHORT_WAIT
from src.data.enums import OrderType, SLTPType, Expiry
from src.data.objects.trade_obj import ObjTrade
from src.page_object.web_app.components.trade.base_trade import BaseTrade
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element, data_testid
from src.utils.format_utils import locator_format, format_dict_to_string
from src.utils.logging_utils import logger


class TradingModals(BaseTrade):
    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------------------------------ LOCATORS ------------------------------------------------ #

    ##### Trade Confirmation Modal #####
    __confirm_order_type = (By.CSS_SELECTOR, data_testid('trade-confirmation-order-type'))
    __confirm_symbol = (By.CSS_SELECTOR, data_testid('trade-confirmation-symbol'))
    __confirm_labels = (By.CSS_SELECTOR, data_testid('trade-confirmation-label'))
    __confirm_values = (By.CSS_SELECTOR, data_testid('trade-confirmation-value'))
    __btn_cancel_trade_confirm = (By.CSS_SELECTOR, data_testid('trade-confirmation-button-close'))

    ##### Edit Confirmation Modal #####
    __btn_update_order = (By.CSS_SELECTOR, data_testid('edit-button-order'))
    __txt_edit_sl = (By.CSS_SELECTOR, data_testid('edit-input-stoploss-{}'))  # price or points
    __txt_edit_tp = (By.CSS_SELECTOR, data_testid('edit-input-takeprofit-{}'))  # price or points
    __txt_edit_price = (By.CSS_SELECTOR, data_testid('edit-input-price'))
    __txt_edit_stp_price = (By.CSS_SELECTOR, data_testid('edit-input-stop-limit-price'))

    __drp_edit_expiry = (By.CSS_SELECTOR, data_testid('edit-dropdown-expiry'))
    __opt_edit_expiry = (By.CSS_SELECTOR, data_testid('edit-dropdown-expiry-{}'))
    __edit_expiry_date = (By.CSS_SELECTOR, data_testid('edit-input-expiry-date'))
    __edit_wheel_expiry_date = (By.CSS_SELECTOR, "div[class='datepicker-wheel']")

    __edit_symbol_price = (By.CSS_SELECTOR, data_testid('edit-symbol-price'))
    __edit_confirm_order_id = (By.CSS_SELECTOR, data_testid('edit-confirmation-order-id'))
    __edit_confirm_order_type = (By.CSS_SELECTOR, data_testid('edit-confirmation-order-type'))
    __edit_confirm_symbol = (By.CSS_SELECTOR, data_testid('edit-confirmation-symbol'))
    __edit_confirm_labels = (By.CSS_SELECTOR, data_testid('edit-confirmation-label'))
    __edit_confirm_values = (By.CSS_SELECTOR, data_testid('edit-confirmation-value'))

    __btn_confirm_update_order = (By.CSS_SELECTOR, data_testid('edit-confirmation-button-confirm'))
    __btn_cancel_update_order = (By.CSS_SELECTOR, data_testid('edit-confirmation-button-close'))

    ##### Asset Items #####
    __btn_cancel_sheet = (By.CSS_SELECTOR, data_testid('action-sheet-cancel-button'))

    # ------------------------------------------------ ACTIONS ------------------------------------------------ #
    def close_trade_confirm_modal(self, timeout=QUICK_WAIT):
        self.actions.click(self.__btn_cancel_trade_confirm, timeout=timeout, raise_exception=False, show_log=False)

    def is_edit_confirm_modal_displayed(self):
        return self.actions.is_element_displayed(self.__edit_confirm_symbol, timeout=SHORT_WAIT)

    def get_edit_price(self, order_type: OrderType = OrderType.MARKET):
        """Return current price of the symbol"""
        time.sleep(0.5)
        if not order_type or order_type == OrderType.MARKET:
            return self.actions.get_text(self.__edit_symbol_price)

        return self.actions.get_text(self.__txt_edit_price)

    def get_edit_sl(self):
        """Get input sl price"""
        locator = cook_element(self.__txt_edit_sl, SLTPType.PRICE.lower())
        self.actions.click(locator)
        res = self.actions.get_value(locator, retry=True)
        logger.debug(f"- Edit SL: {res!r}")
        return res

    def get_edit_tp(self):
        """Get input tp price"""
        locator = cook_element(self.__txt_edit_tp, SLTPType.PRICE.lower())
        self.actions.click(locator)
        res = self.actions.get_value(locator, retry=True)
        logger.debug(f"- Edit TP: {res!r}")
        return res

    def input_edit_sl(self, value, sl_type: SLTPType = SLTPType.PRICE):
        logger.debug(f"- Input SL: {value!r}, type: {sl_type.value.capitalize()!r}")
        locator = cook_element(self.__txt_edit_sl, sl_type.lower())
        self.actions.send_keys(locator, value)

    def input_edit_tp(self, value, tp_type: SLTPType = SLTPType.PRICE):
        logger.debug(f"- Input TP: {value!r}, type: {tp_type.value.capitalize()!r}")
        locator = cook_element(self.__txt_edit_tp, tp_type.lower())
        self.actions.send_keys(locator, value)

    def input_edit_price(self, value):
        logger.debug(f"- Input price: {value!r}")
        self.actions.send_keys(self.__txt_edit_price, value)

    def input_edit_stop_price(self, value):
        logger.debug(f"- Input stop limit price: {value!r}")
        self.actions.send_keys(self.__txt_edit_stp_price, value)

    def select_expiry(self, expiry: Expiry):
        self.actions.click(self.__drp_edit_expiry)

        locator = locator_format(expiry)
        # handle special locator
        if expiry == Expiry.SPECIFIED_DATE:
            locator = "_".join(item.lower() for item in expiry.split(" "))

        self.actions.click(cook_element(self.__opt_edit_expiry, locator))

        if expiry in [Expiry.SPECIFIED_DATE, Expiry.SPECIFIED_DATE_TIME]:
            logger.debug(f"- Select expiry date")
            self.actions.click(self.__edit_expiry_date)
            self.actions.scroll_picker_down(self.__edit_wheel_expiry_date)
            self.click_confirm_btn()

    def click_update_order_btn(self):
        self.actions.click(self.__btn_update_order, timeout=SHORT_WAIT, raise_exception=False)

    def confirm_update_order(self):
        self.actions.click(self.__btn_confirm_update_order)

    def _get_trade_confirmation(self):
        labels = self.actions.get_text_elements(self.__confirm_labels)
        values = self.actions.get_text_elements(self.__confirm_values)

        actual = {k.lower().replace(" ", "_"): v for k, v in zip(labels, values)}
        actual["symbol"] = self.actions.get_text(self.__confirm_symbol)
        actual["order_type"] = self.actions.get_text(self.__confirm_order_type)
        if "size" in actual:
            actual["volume"] = actual.pop("size")

        logger.debug(f"- Actual: {format_dict_to_string(actual)}")
        return actual

    def _get_edit_trade_confirmation(self):
        labels = self.actions.get_text_elements(self.__edit_confirm_labels)
        values = self.actions.get_text_elements(self.__edit_confirm_values)

        actual = {k.lower().replace(" ", "_"): v for k, v in zip(labels, values)}

        actual['symbol'] = self.actions.get_text(self.__edit_confirm_symbol)
        actual['order_type'] = self.actions.get_text(self.__edit_confirm_order_type)
        actual['order_no'] = self.actions.get_text(self.__edit_confirm_order_id)

        if "size" in actual:
            actual["volume"] = actual.pop("size")

        logger.debug(f"- Actual: {format_dict_to_string(actual)}")
        return actual

    # ------------------------------------------------ VERIFY ------------------------------------------------ #
    def verify_trade_confirmation(self, trade_object: ObjTrade):
        """Verify the trade confirmation information."""
        expected = trade_object.trade_confirm_details()
        if not trade_object.order_type.is_market():
            expected["price"] = expected.pop("entry_price", None)

        actual = self._get_trade_confirmation()
        actual = {k: v for k, v in actual.items() if k in expected}
        soft_assert(actual, expected, tolerance=1, tolerance_fields=trade_object.tolerance_fields())

    def verify_edit_trade_confirmation(self, trade_object: ObjTrade):
        expected = trade_object.trade_edit_confirm_details()
        actual = self._get_edit_trade_confirmation()
        actual = {k: v for k, v in actual.items() if k in expected}
        soft_assert(actual, expected, tolerance=1, tolerance_fields=trade_object.tolerance_fields())
