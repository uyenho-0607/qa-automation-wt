import time

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import QUICK_WAIT, SHORT_WAIT
from src.data.enums import BulkCloseOpts, OrderType, SLTPType, Expiry
from src.data.objects.trade_obj import ObjTrade
from src.page_object.android.components.trade.base_trade import BaseTrade
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import resource_id, cook_element
from src.utils.format_utils import locator_format, format_dict_to_string
from src.utils.logging_utils import logger


class TradingModals(BaseTrade):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------------------------------ LOCATORS ------------------------------------------------ #

    ##### Trade Confirmation Modal #####
    __confirm_order_type = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("trade-confirmation-order-type")')
    __confirm_symbol = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("trade-confirmation-symbol")')
    __confirm_volume = (
        AppiumBy.XPATH,
        "//*[@resource-id='trade-confirmation-label' and (@text='Size' or @text='Volume')]"
        "/following-sibling::*[2]"
    )
    __confirm_units = (AppiumBy.XPATH, "//*[@resource-id='trade-confirmation-label' and @text='Units']/following-sibling::*[2]")
    __confirm_price = (AppiumBy.XPATH, "//*[@resource-id='trade-confirmation-label' and @text='Price']/following-sibling::*[@resource-id='trade-confirmation-value']")
    __confirm_stop_limit_price = (AppiumBy.XPATH, "//*[@resource-id='trade-confirmation-label' and @text='Stop Limit Price']/following-sibling::*[@resource-id='trade-confirmation-value'][2]")
    __confirm_stop_loss = (AppiumBy.XPATH, "//*[@resource-id='trade-confirmation-label' and @text='Stop Loss']/following-sibling::*[2]")
    __confirm_take_profit = (AppiumBy.XPATH, "//*[@resource-id='trade-confirmation-label' and @text='Take Profit']/following-sibling::*[2]")
    __confirm_expiry = (AppiumBy.XPATH, "//*[@resource-id='trade-confirmation-label' and @text='Expiry']/following-sibling::*[@resource-id='trade-confirmation-value'][1]")
    __confirm_fill_policy_by_text = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("trade-confirmation-value").text("{}")')

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



    __edit_confirm_order_id = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-confirmation-order-id")')
    __edit_confirm_order_type = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-confirmation-order-type")')
    __edit_confirm_symbol = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-confirmation-symbol")')
    __edit_confirm_volume = (
        AppiumBy.XPATH,
        "//*[@resource-id='edit-confirmation-label' and (@text='Volume' or @text='Size')]"
        "/following-sibling::*[@resource-id='edit-confirmation-value'][1]"
    )
    __edit_confirm_units = (
        AppiumBy.XPATH,
        "//*[@resource-id='edit-confirmation-label' and @text='Units']"
        "/following-sibling::*[@resource-id='edit-confirmation-value'][2]"
    )
    __edit_confirm_sl = (
        AppiumBy.XPATH,
        "//*[@resource-id='edit-confirmation-label' and @text='Stop Loss']/following-sibling::*[2]"
    )
    __edit_confirm_tp = (
        AppiumBy.XPATH,
        "//*[@resource-id='edit-confirmation-label' and @text='Take Profit']/following-sibling::*[2]"
    )
    __edit_confirm_price = (
        AppiumBy.XPATH,
        "//*[@resource-id='edit-confirmation-label' and @text='Price']"
        "/following-sibling::*[@resource-id='edit-confirmation-value'][1]"
    )
    __edit_confirm_stop_limit_price = (
        AppiumBy.XPATH,
        "//*[@resource-id='edit-confirmation-label' and @text='Stop Limit Price']"
        "/following-sibling::*[@resource-id='edit-confirmation-value'][1]"
    )
    __edit_confirm_expiry = (
        AppiumBy.XPATH,
        "//*[@resource-id='edit-confirmation-label' and @text='Expiry']"
        "/following-sibling::*[@resource-id='edit-confirmation-value'][1]"
    )
    __edit_confirm_fill_policy_by_text = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("edit-confirmation-value").text("{}")'
    )


    __btn_confirm_update_order = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-confirmation-button-confirm")')
    __btn_cancel_update_order = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("edit-confirmation-button-close")')

    ##### Asset Items #####
    __btn_cancel_close_order = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("close-order-button-cancel")')
    __btn_cancel_delete_order = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("confirmation-modal-button-cancel")')

    __btn_bulk_close_confirm = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("bulk-close-modal-button-submit-{}")')
    __btn_bulk_close_cancel = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("bulk-close-modal-button-cancel-all")')
    __btn_bulk_delete_confirm = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("bulk-delete-modal-button-submit")')
    __btn_bulk_delete_cancel = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("bulk-delete-modal-button-cancel")')

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
        self.actions.click(locator)
        res = self.actions.get_text(locator)
        logger.debug(f"- Edit SL: {res!r}")
        return res

    def get_edit_tp(self):
        """Get input tp price"""
        locator = cook_element(self.__txt_edit_tp, SLTPType.PRICE.lower())
        self.actions.click(locator)
        res = self.actions.get_text(locator)
        logger.debug(f"- Edit TP: {res!r}")
        return res

    def input_edit_sl(self, value, sl_type: SLTPType = SLTPType.PRICE):
        logger.debug(f"- Input SL: {value!r}, type: {sl_type.value.capitalize()!r}")
        locator = cook_element(self.__txt_edit_sl, sl_type.lower())
        self.actions.send_keys(locator, value)
        self.actions.press_done()

    def input_edit_tp(self, value, tp_type: SLTPType = SLTPType.PRICE):
        logger.debug(f"- Input TP: {value!r}, type: {tp_type.value.capitalize()!r}")
        locator = cook_element(self.__txt_edit_tp, tp_type.lower())
        self.actions.send_keys(locator, value)
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

    # def _get_trade_confirmation(self):
    #     """Get trade confirmation data from modal."""
    #     locator_list = [
    #         self.__confirm_order_type,
    #         self.__confirm_symbol,
    #         self.__confirm_volume,
    #         self.__confirm_units,
    #         self.__confirm_stop_loss,
    #         self.__confirm_take_profit,
    #     ]
    #
    #     # Get text from all locators
    #     values = [self.actions.get_text(locator) for locator in locator_list]
    #     keys = ["order_type", "symbol", "volume", "units", "stop_loss", "take_profit"]
    #
    #     actual = dict(zip(keys, values))
    #
    #     # Handle size vs volume
    #     if "size" in actual:
    #         actual["volume"] = actual.pop("size")
    #
    #     logger.debug(f"- Actual: {format_dict_to_string(actual)}")
    #     return actual
    #
    # def _get_edit_trade_confirmation(self):
    #     """Get edit trade confirmation data from modal."""
    #     actual = {
    #         "order_no": self.actions.get_text(self.__edit_confirm_order_id).split(": ")[-1].strip(),
    #         "order_type": self.actions.get_text(self.__edit_confirm_order_type),
    #         "symbol": self.actions.get_text(self.__edit_confirm_symbol),
    #         "volume": self.actions.get_text(self.__edit_confirm_volume),
    #         "units": self.actions.get_text(self.__edit_confirm_units),
    #         "stop_loss": self.actions.get_text(self.__edit_confirm_sl),
    #         "take_profit": self.actions.get_text(self.__edit_confirm_tp)
    #     }
    #
    #     # Handle size vs volume
    #     if "size" in actual:
    #         actual["volume"] = actual.pop("size")
    #
    #     logger.debug(f"- Actual: {format_dict_to_string(actual)}")
    #     return actual

    # ------------------------------------------------ VERIFY ------------------------------------------------ #
# ------------------------------------------------ VERIFY ------------------------------------------------ #
    def verify_trade_confirmation(self, trade_object: ObjTrade):
        """Verify the trade confirmation information."""

        expected = trade_object.trade_confirm_details()

        # Handle actual dict
        locator_list = [
            self.__confirm_order_type,
            self.__confirm_symbol,
            self.__confirm_volume,
            self.__confirm_units,
            self.__confirm_stop_loss,
            self.__confirm_take_profit,
        ]

        not expected.get("fill_policy") or locator_list.append(cook_element(self.__confirm_fill_policy_by_text, expected["fill_policy"]))
        not expected.get("expiry") or locator_list.append(self.__confirm_expiry)

        if trade_object.order_type != OrderType.MARKET:
            locator_list.append(self.__confirm_price)

        if trade_object.order_type.is_stp_limit():
            locator_list.append(self.__confirm_stop_limit_price)

        actual = {
            k: v for k, v in zip(expected, [self.actions.get_text(locator) for locator in locator_list])
        }
        soft_assert(actual, expected, tolerance=1, tolerance_fields=trade_object.tolerance_fields())

    def verify_edit_trade_confirmation(self, trade_object: ObjTrade):
        expected = trade_object.trade_edit_confirm_details()
        actual = {
            "order_no": self.actions.get_text(self.__edit_confirm_order_id),
            "order_type": self.actions.get_text(self.__edit_confirm_order_type),
            "symbol": self.actions.get_text(self.__edit_confirm_symbol),
            "volume": self.actions.get_text(self.__edit_confirm_volume),
            "units": self.actions.get_text(self.__edit_confirm_units),
            "stop_loss": self.actions.get_text(self.__edit_confirm_sl),
            "take_profit": self.actions.get_text(self.__edit_confirm_tp)
        }
        if expected.get("entry_price"):
            actual["entry_price"] = self.actions.get_text(self.__edit_confirm_price)

        if expected.get("stop_limit_price"):
            actual["stop_limit_price"] = self.actions.get_text(self.__edit_confirm_stop_limit_price)

        if expected.get("fill_policy"):
            actual["fill_policy"] = self.actions.get_text(cook_element(self.__edit_confirm_fill_policy_by_text, expected["fill_policy"]))

        if expected.get("expiry"):
            actual["expiry"] = self.actions.get_text(self.__edit_confirm_expiry)

        soft_assert(actual, expected, tolerance=1, tolerance_fields=trade_object.tolerance_fields())
