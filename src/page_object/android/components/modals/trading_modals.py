import time

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import QUICK_WAIT, SHORT_WAIT
from src.data.enums import BulkCloseOpts, OrderType, SLTPType, Expiry
from src.data.objects.trade_obj import ObjTrade
from src.page_object.android.components.trade.base_trade import BaseTrade
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element
from src.utils.format_utils import locator_format, format_dict_to_string
from src.utils.logging_utils import logger


class TradingModals(BaseTrade):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------------------------------ LOCATORS ------------------------------------------------ #

    ##### Trade Confirmation Modal #####
    __confirm_order_type = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("trade-confirmation-order-type")')
    __confirm_symbol = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("trade-confirmation-symbol")')
    __confirm_labels = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("trade-confirmation-label")')
    __confirm_values = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("trade-confirmation-value")')

    ##### Edit Confirmation Modal #####
    __edit_symbol_price = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-symbol-price")')
    __btn_edit_order = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-button-order")')
    __btn_cancel_edit_order = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-button-cancel")')
    __txt_edit_sl = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-input-stoploss-{}")')  # price or points
    __txt_edit_tp = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-input-takeprofit-{}")')  # price or points
    __txt_edit_price = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-input-price")')
    __txt_edit_stop_limit_price = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-input-stop-limit-price")')

    __drp_expiry = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-dropdown-expiry")')
    __option_edit_expiry = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-dropdown-expiry-{}")')
    __expiry_date = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-input-expiry-date")')
    __wheel_expiry_date = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.SeekBar").descriptionContains("Select Date")')
    __edit_confirm_labels = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-confirmation-label")')
    __edit_confirm_values = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-confirmation-value")')

    __edit_confirm_order_id = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-confirmation-order-id")')
    __edit_confirm_order_type = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-confirmation-order-type")')
    __edit_confirm_symbol = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-confirmation-symbol")')


    __btn_confirm_update_order = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-confirmation-button-confirm")')
    __btn_cancel_update_order = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-confirmation-button-close")')

    ##### Asset Items #####
    __btn_cancel_close_order = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("close-order-button-cancel")')
    __btn_cancel_delete_order = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("confirmation-modal-button-cancel")')

    __btn_bulk_close_confirm = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("bulk-close-modal-button-submit-{}")')
    __btn_bulk_close_cancel = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("bulk-close-modal-button-cancel-all")')

    # ------------------------------------------------ ACTIONS ------------------------------------------------ #
    def close_trade_confirm_modal(self, timeout=QUICK_WAIT):
        self.actions.click(self.__btn_cancel_close_order, timeout=timeout, raise_exception=False, show_log=False)

    def confirm_bulk_close(self, option: BulkCloseOpts = BulkCloseOpts.ALL):
        """Click the bulk close confirm button."""
        self.actions.click(cook_element(self.__btn_bulk_close_confirm, locator_format(option)))

    def cancel_bulk_close(self, timeout=QUICK_WAIT):
        self.actions.click(self.__btn_bulk_close_cancel, timeout=timeout, raise_exception=False, show_log=False)

    def cancel_close_order(self, timeout=QUICK_WAIT):
        self.actions.click(self.__btn_cancel_close_order, timeout=timeout, raise_exception=False, show_log=False)

    def cancel_delete_order(self, timeout=QUICK_WAIT):
        self.actions.click(self.__btn_cancel_delete_order, timeout=timeout, raise_exception=False)

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
        res = self.actions.get_text(locator)
        logger.debug(f"- Edit SL: {res!r}")
        return res

    def get_edit_tp(self):
        """Get input tp price"""
        locator = cook_element(self.__txt_edit_tp, SLTPType.PRICE.lower())
        res = self.actions.get_text(locator)
        logger.debug(f"- Edit TP: {res!r}")
        return res

    def input_edit_sl(self, value, sl_type: SLTPType = SLTPType.PRICE):
        logger.debug(f"- Input SL: {value!r}, type: {sl_type.value.capitalize()!r}")
        locator = cook_element(self.__txt_edit_sl, sl_type.lower())
        self.actions.send_keys(locator, value, hide_keyboard=False)
        self.actions.press_done()

    def input_edit_tp(self, value, tp_type: SLTPType = SLTPType.PRICE):
        logger.debug(f"- Input TP: {value!r}, type: {tp_type.value.capitalize()!r}")
        locator = cook_element(self.__txt_edit_tp, tp_type.lower())
        self.actions.send_keys(locator, value, hide_keyboard=False)
        self.actions.press_done()

    def input_edit_price(self, value):
        logger.debug(f"- Input price: {value!r}")
        self.actions.send_keys(self.__txt_edit_price, value)

    def input_edit_stop_price(self, value):
        logger.debug(f"- Input stop limit price: {value!r}")
        self.actions.send_keys(self.__txt_edit_stop_limit_price, value)
    
    def select_expiry(self, expiry: Expiry):
        self.actions.click(self.__drp_expiry)
        
        locator = locator_format(expiry)
        # handle special locator
        if expiry == Expiry.SPECIFIED_DATE:
            locator = "_".join(item.lower() for item in expiry.split(" "))
        
        self.actions.click(cook_element(self.__option_edit_expiry, locator))

        if expiry in [Expiry.SPECIFIED_DATE, Expiry.SPECIFIED_DATE_TIME]:
            logger.debug(f"- Select expiry date")
            self.actions.scroll_down()
            self.actions.click(self.__expiry_date)
            self.actions.swipe_picker_wheel_down(self.__wheel_expiry_date)
            self.click_confirm_btn()
        
    def click_update_order_btn(self):
        self.actions.click(self.__btn_edit_order, timeout=SHORT_WAIT, raise_exception=False)

    def confirm_update_order(self):
        self.actions.click(self.__btn_confirm_update_order)

    def cancel_edit_order(self):
        self.actions.click(self.__btn_cancel_edit_order, timeout=QUICK_WAIT, raise_exception=False, show_log=False)

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
        actual['order_no'] = self.actions.get_text(self.__edit_confirm_order_id).split(": ")[-1].strip()

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
