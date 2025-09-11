import random
import time

from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import QUICK_WAIT, SHORT_WAIT
from src.data.enums import OrderType, SLTPType, Expiry
from src.data.objects.trade_obj import ObjTrade
from src.page_object.web.components.trade.base_trade import BaseTrade
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import data_testid, cook_element
from src.utils.format_utils import locator_format, format_dict_to_string
from src.utils.logging_utils import logger


class TradingModals(BaseTrade):
    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------------------------------ LOCATORS ------------------------------------------------ #
    ##### Trade Confirmation Modal #####
    __btn_cancel_trade = (By.XPATH, "//div[text()='Trade Confirmation']/parent::div/following-sibling::div")
    __confirm_order_type = (By.CSS_SELECTOR, data_testid('trade-confirmation-order-type'))
    __confirm_symbol = (By.CSS_SELECTOR, data_testid('trade-confirmation-symbol'))
    __confirm_labels = (By.CSS_SELECTOR, data_testid('trade-confirmation-label'))
    __confirm_values = (By.CSS_SELECTOR, data_testid('trade-confirmation-value'))

    ##### Edit Confirmation Modal #####
    __btn_edit_order = (By.CSS_SELECTOR, data_testid('edit-button-order'))
    __txt_edit_sl = (By.CSS_SELECTOR, data_testid('edit-input-stoploss-{}'))  # price or points
    __txt_edit_tp = (By.CSS_SELECTOR, data_testid('edit-input-takeprofit-{}'))  # price or points
    __txt_edit_price = (By.CSS_SELECTOR, data_testid('edit-input-price'))
    __txt_edit_stp_price = (By.CSS_SELECTOR, data_testid('edit-input-stop-limit-price'))

    __drp_edit_expiry = (By.CSS_SELECTOR, data_testid('edit-dropdown-expiry'))
    __opt_edit_expiry = (By.CSS_SELECTOR, data_testid('edit-dropdown-expiry-{}'))
    __btn_next_calendar = (By.CSS_SELECTOR, "button[class*='next'][class*='calendar']")
    __txt_edit_expiry_date = (By.CSS_SELECTOR, data_testid('edit-input-expiry-date'))
    __expiry_last_date = (By.XPATH, "(//button[contains(@class, 'month-view')])[last()]")

    __drp_edit_fill_policy = (By.CSS_SELECTOR, data_testid('edit-dropdown-fill-policy'))
    __opt_edit_fill_policy = (By.CSS_SELECTOR, data_testid('edit-dropdown-fill-policy-{}'))

    __btn_confirm_update_order = (By.CSS_SELECTOR, data_testid('edit-confirmation-button-confirm'))
    __edit_symbol_price = (By.CSS_SELECTOR, data_testid('edit-symbol-price'))
    __edit_confirm_order_id = (By.CSS_SELECTOR, data_testid('edit-confirmation-order-id'))
    __edit_confirm_order_type = (By.CSS_SELECTOR, data_testid('edit-confirmation-order-type'))
    __edit_confirm_symbol = (By.CSS_SELECTOR, data_testid('edit-confirmation-symbol'))
    __edit_confirm_labels = (By.CSS_SELECTOR, data_testid('edit-confirmation-label'))
    __edit_confirm_values = (By.CSS_SELECTOR, data_testid('edit-confirmation-value'))

    # control buttons
    __btn_inc_dec_sl = (By.CSS_SELECTOR, data_testid('edit-input-stoploss-{}-{}'))  # price/ points - increase/ decrease
    __btn_inc_dec_tp = (By.CSS_SELECTOR, data_testid('edit-input-takeprofit-{}-{}'))
    __btn_inc_dec_price = (By.CSS_SELECTOR, data_testid('edit-input-price-{}'))
    __btn_inc_dec_stp_price = (By.CSS_SELECTOR, data_testid('edit-input-stop-limit-price-{}'))

    # ------------------------------------------------ ACTIONS ------------------------------------------------ #

    def is_edit_confirm_modal_displayed(self, timeout: int | float = SHORT_WAIT):
        return self.actions.is_element_displayed(self.__edit_confirm_symbol, timeout=timeout)

    def close_trade_confirm_modal(self, timeout=QUICK_WAIT):
        self.actions.click(self.__btn_cancel_trade, timeout=timeout, raise_exception=False, show_log=False)

    # Edit Confirmation Modal Actions
    def close_edit_confirm_modal(self, timeout=QUICK_WAIT):
        self.actions.click_by_offset(self.__edit_confirm_order_id, 173, -12, timeout=timeout, raise_exception=False, show_log=False)
        self.actions.click_by_offset(self.__edit_confirm_order_type, 300, 20, timeout=timeout, raise_exception=False, show_log=False)

    def click_edit_order_btn(self, retries=3, oct_mode=False):
        """Click the edit order button."""
        if oct_mode:
            logger.debug(f"- Click edit order button")
            self.actions.click(self.__btn_edit_order)
            return True

        for attempt in range(1, retries + 1):
            logger.debug(f"- Click edit order button (attempt:{attempt})")
            self.actions.click(self.__btn_edit_order, raise_exception=False, timeout=QUICK_WAIT)

            if self.is_edit_confirm_modal_displayed(timeout=SHORT_WAIT):
                logger.debug("> Confirm edit modal displayed")
                return True
            else:
                logger.warning("> Confirm edit modal is not displayed, retry clicking edit order button")

        logger.warning("- Max retries exceeded for clicking edit order button")
        return False

    def confirm_update_order(self, wait=False):
        """Click the confirm update order button."""
        self.actions.javascript_click(self.__btn_confirm_update_order)
        not wait or self.wait_for_spin_loader()

    def get_edit_price(self, order_type: OrderType | str = None):
        """Return current price of the symbol"""
        time.sleep(0.5)
        if not order_type or order_type == OrderType.MARKET:
            return self.actions.get_text(self.__edit_symbol_price)

        return self.actions.get_value(self.__txt_edit_price)

    def get_edit_stp_price(self):
        return self.actions.get_value(self.__txt_edit_stp_price)

    def get_edit_sl(self):
        locator = cook_element(self.__txt_edit_sl, SLTPType.PRICE.lower())
        self.actions.click(locator)
        res = self.actions.get_value(locator, retry=True)
        logger.debug(f"> Edit SL PRICE: {res!r}")
        return res

    def get_edit_tp(self):
        locator = cook_element(self.__txt_edit_tp, SLTPType.PRICE.lower())
        self.actions.click(locator)
        res = self.actions.get_value(locator, retry=True)
        logger.debug(f"> Edit TP PRICE: {res!r}")
        return res

    def input_edit_sl(self, value, sl_type: SLTPType = SLTPType.PRICE):
        logger.debug(f"- Input edit SL: {value} - type: {sl_type.lower()}")
        locator = cook_element(self.__txt_edit_sl, sl_type.lower())
        self.actions.clear_field(locator)
        # time.sleep(1)
        self.actions.send_keys(locator, value)

    def input_edit_tp(self, value, tp_type: SLTPType = SLTPType.PRICE):
        logger.debug(f"- Input edit TP: {value} - type: {tp_type.lower()}")
        locator = cook_element(self.__txt_edit_tp, tp_type.lower())
        self.actions.clear_field(locator)
        # time.sleep(1)
        self.actions.send_keys(locator, value)

    def input_edit_price(self, value, order_type: OrderType | str = None):
        if not order_type or order_type == OrderType.MARKET:
            return

        logger.debug(f"- Input edit price: {value}")
        self.actions.send_keys(self.__txt_edit_price, value)

    def input_edit_stp_price(self, value, order_type: OrderType | str = None):
        if not order_type or not order_type.is_stp_limit():
            return

        logger.debug(f"- Input edit STP price: {value}")
        self.actions.send_keys(self.__txt_edit_stp_price, value)

    def select_expiry(self, expiry):
        if not expiry:
            return

        logger.debug(f"- Select expiry: {expiry}")
        self.actions.click(self.__drp_edit_expiry)
        self.actions.click(cook_element(self.__opt_edit_expiry, locator_format(expiry)))

        if expiry in [Expiry.SPECIFIED_DATE, Expiry.SPECIFIED_DATE_TIME]:
            logger.debug("> Select expiry date")
            self.actions.click(self.__txt_edit_expiry_date)
            self.actions.click(self.__btn_next_calendar)
            self.actions.click(self.__expiry_last_date)

    # Control buttons
    def control_price(self, order_type: OrderType, stp_price=True, price=True, stop_loss=True, take_profit=True):

        if stp_price and order_type.is_stp_limit():
            for _ in range(random.randint(10, 20)):
                self.actions.click(cook_element(self.__btn_inc_dec_stp_price, "increase"))

            for _ in range(random.randint(1, 10)):
                self.actions.click(cook_element(self.__btn_inc_dec_stp_price, "decrease"))

        if price and order_type != OrderType.MARKET:
            for _ in range(random.randint(10, 20)):
                self.actions.click(cook_element(self.__btn_inc_dec_price, "increase"))

            for _ in range(random.randint(1, 10)):
                self.actions.click(cook_element(self.__btn_inc_dec_price, "decrease"))

        if stop_loss:
            sl_type = SLTPType.sample_values()
            for _ in range(random.randint(10, 20)):
                self.actions.click(cook_element(self.__btn_inc_dec_sl, sl_type.lower(), "increase"))

            for _ in range(random.randint(1, 10)):
                self.actions.click(cook_element(self.__btn_inc_dec_sl, sl_type.lower(), "decrease"))

        if take_profit:
            tp_type = SLTPType.sample_values()
            for _ in range(random.randint(10, 20)):
                self.actions.click(cook_element(self.__btn_inc_dec_tp, tp_type.lower(), "increase"))
            for _ in range(random.randint(1, 10)):
                self.actions.click(cook_element(self.__btn_inc_dec_tp, tp_type.lower(), "decrease"))

    def _get_trade_confirmation(self):
        labels = self.actions.get_text_elements(self.__confirm_labels)
        values = self.actions.get_text_elements(self.__confirm_values)

        actual = {k.lower().replace(" ", "_"): v for k, v in zip(labels, values)}

        actual['symbol'] = self.actions.get_text(self.__confirm_symbol, timeout=QUICK_WAIT)
        actual['order_type'] = self.actions.get_text(self.__confirm_order_type, timeout=QUICK_WAIT)
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
        actual['order_no'] = self.actions.get_text(self.__edit_confirm_order_id).split(": ")[-1].strip()

        if "size" in actual:
            actual["volume"] = actual.pop("size")

        # logger.debug(f"- Actual: {format_dict_to_string(actual)}")
        return actual

    # ------------------------------------------------ VERIFY ------------------------------------------------ #
    def verify_trade_confirmation(self, trade_object: ObjTrade):
        """Verify the trade confirmation information."""
        expected = trade_object.trade_confirm_details()
        if not trade_object.order_type.is_market():
            expected["price"] = expected.pop("entry_price", None)

        actual = self._get_trade_confirmation()
        soft_assert(actual, expected, check_contains=True, tolerance=1, tolerance_fields=trade_object.tolerance_fields())

    def verify_edit_trade_confirmation(self, trade_object: ObjTrade):
        expected = trade_object.trade_edit_confirm_details()
        actual = self._get_edit_trade_confirmation()
        soft_assert(actual, expected, check_contains=True, tolerance=1, tolerance_fields=trade_object.tolerance_fields())
