import time

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import QUICK_WAIT
from src.data.enums import BulkCloseOpts, OrderType, SLTPType, FillPolicy, Expiry, AssetTabs
from src.data.objects.trade_obj import ObjTrade
from src.page_object.ios.components.trade.base_trade import BaseTrade
from src.utils.common_utils import resource_id, cook_element
from src.utils.format_utils import locator_format
from src.utils.logging_utils import logger
from src.utils.trading_utils import get_sl_tp


class TradingModals(BaseTrade):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------------------------------ LOCATORS ------------------------------------------------ #

    ##### Trade Confirmation Modal #####
    __confirm_order_type = (AppiumBy.ACCESSIBILITY_ID, 'trade-confirmation-order-type')
    __confirm_symbol = (AppiumBy.ACCESSIBILITY_ID, 'trade-confirmation-symbol')
    __confirm_volume = (
        AppiumBy.XPATH,
        "//*[@name='trade-confirmation-label' and (@label='Size' or @text='Volume')]/following-sibling::*[1]"
    )
    __confirm_units = (
        AppiumBy.XPATH, "//*[@name='trade-confirmation-label' and @label='Units']/following-sibling::*[1]")
    __confirm_price = (
        AppiumBy.XPATH, "//*[@name='trade-confirmation-label' and @label='Price']/following-sibling::*[1]")
    __confirm_stop_limit_price = (
        AppiumBy.XPATH, "//*[@name='trade-confirmation-label' and @label='Stop Limit Price']/following-sibling::*[1]"
    )
    __confirm_stop_loss = (
        AppiumBy.XPATH, "//*[@name='trade-confirmation-label' and @label='Stop Loss']/following-sibling::*[1]"
    )
    __confirm_take_profit = (
        AppiumBy.XPATH, "//*[@name='trade-confirmation-label' and @label='Take Profit']/following-sibling::*[1]"
    )
    __confirm_expiry = (
        AppiumBy.XPATH, "//*[@name='trade-confirmation-label' and @label='Expiry']/following-sibling::*[1]"
    )
    __confirm_fill_policy_by_text = (
        AppiumBy.XPATH, "//*[@name='trade-confirmation-value' and @label='{}']"
    )

    ##### Edit Confirmation Modal #####
    __edit_symbol_price = (AppiumBy.ACCESSIBILITY_ID, 'edit-symbol-price')
    __btn_edit_order = (AppiumBy.ACCESSIBILITY_ID, 'edit-button-order')
    __btn_cancel_edit_order = (AppiumBy.ACCESSIBILITY_ID, 'edit-button-cancel')
    __txt_edit_sl = (AppiumBy.ACCESSIBILITY_ID, 'edit-input-stoploss-{}')  # price or points
    __txt_edit_tp = (AppiumBy.ACCESSIBILITY_ID, 'edit-input-takeprofit-{}')  # price or points
    __txt_edit_price = (AppiumBy.ACCESSIBILITY_ID, 'edit-input-price')
    __txt_edit_stop_limit_price = (AppiumBy.ACCESSIBILITY_ID, 'edit-input-stop-limit-price')

    __drp_expiry = (AppiumBy.XPATH, resource_id('edit-dropdown-expiry'))
    __option_edit_expiry = (AppiumBy.XPATH, resource_id('edit-dropdown-expiry-{}'))
    __expiry_date = (AppiumBy.XPATH, resource_id('edit-input-expiry-date'))
    __wheel_expiry_date = (AppiumBy.XPATH, "//android.widget.SeekBar[contains(@content-desc, 'Select Date')]")

    __drp_fill_policy = (AppiumBy.XPATH, resource_id('edit-dropdown-fill-policy'))
    __opt_edit_fill_policy = (AppiumBy.XPATH, resource_id('edit-dropdown-fill-policy-{}'))

    __edit_confirm_order_id = (AppiumBy.ACCESSIBILITY_ID, "edit-confirmation-order-id")
    __edit_confirm_order_type = (AppiumBy.ACCESSIBILITY_ID, "edit-confirmation-order-type")
    __edit_confirm_symbol = (AppiumBy.ACCESSIBILITY_ID, "edit-confirmation-symbol")

    __edit_confirm_volume = (
        AppiumBy.XPATH,
        "//*[@name='edit-confirmation-label' and (@label='Size' or @text='Volume')]/following-sibling::*[1]"
    )
    __edit_confirm_units = (
        AppiumBy.XPATH,
        "//*[@name='edit-confirmation-label' and @label='Units']/following-sibling::*[1]"
    )
    __edit_confirm_sl = (
        AppiumBy.XPATH,
        "//*[@name='trade-confirmation-label' and @label='Stop Loss']/following-sibling::*[1]"
    )
    __edit_confirm_tp = (
        AppiumBy.XPATH,
        "//*[@name='edit-confirmation-label' and @label='Take Profit']/following-sibling::*[1]"
    )
    __edit_confirm_price = (
        AppiumBy.XPATH, "//*[@name='edit-confirmation-label' and @label='Price']/following-sibling::*[1]"
    )
    __edit_confirm_stop_limit_price = (
        AppiumBy.XPATH,
        "//*[@name='edit-confirmation-label' and @label='Stop Limit Price']/following-sibling::*[1]"
    )
    __edit_confirm_expiry = (
        AppiumBy.XPATH, "//*[@name='edit-confirmation-label' and @label='Expiry']/following-sibling::*[1]"
    )
    __edit_confirm_fill_policy_by_text = (
        AppiumBy.XPATH,
        "//*[@name='edit-confirmation-value' and @label='{}']"
    )

    # control buttons
    __btn_inc_dec_sl = (AppiumBy.XPATH, resource_id('edit-input-stoploss-{}-{}'))  # price/ points - increase/ decrease
    __btn_inc_dec_tp = (AppiumBy.XPATH, resource_id('edit-input-takeprofit-{}-{}'))
    __btn_inc_dec_price = (AppiumBy.XPATH, resource_id('edit-input-price-{}'))
    __btn_inc_dec_stop_limit_price = (AppiumBy.XPATH, resource_id('edit-input-stoplimit-price-{}'))

    __btn_confirm_update_order = (AppiumBy.XPATH, resource_id('edit-confirmation-button-confirm'))
    __btn_cancel_update_order = (AppiumBy.XPATH, resource_id('edit-confirmation-button-close'))

    ##### Asset Items #####
    __btn_cancel_close_order = (AppiumBy.ACCESSIBILITY_ID, "close-order-button-cancel")
    __btn_cancel_delete_order = (AppiumBy.XPATH, resource_id('confirmation-modal-button-cancel'))

    __btn_bulk_close_confirm = (AppiumBy.XPATH, resource_id('bulk-close-modal-button-submit-{}'))
    __btn_bulk_close_cancel = (AppiumBy.XPATH, resource_id('bulk-close-modal-button-cancel-all'))
    __btn_bulk_delete_confirm = (AppiumBy.XPATH, resource_id('bulk-delete-modal-button-submit'))
    __btn_bulk_delete_cancel = (AppiumBy.XPATH, resource_id('bulk-delete-modal-button-cancel'))

    # ------------------------------------------------ ACTIONS ------------------------------------------------ #
    def close_edit_confirm_modal(self, timeout=QUICK_WAIT):
        self.actions.click(self.__btn_cancel_close_order, timeout=timeout, raise_exception=False, show_log=False)

    def confirm_bulk_delete(self):
        """Confirm bulk delete action."""
        self.actions.click(self.__btn_bulk_delete_confirm)

    def cancel_bulk_delete(self, timeout=QUICK_WAIT):
        self.actions.click(self.__btn_bulk_delete_cancel, timeout=timeout, raise_exception=False)

    def cancel_delete_order(self, timeout=QUICK_WAIT):
        self.actions.click(self.__btn_cancel_delete_order, timeout=timeout, raise_exception=False)

    def confirm_bulk_close(self, option: BulkCloseOpts = BulkCloseOpts.ALL):
        """Click the bulk close confirm button."""
        self.actions.click(cook_element(self.__btn_bulk_close_confirm, locator_format(option)))

    def cancel_bulk_close(self, timeout=QUICK_WAIT):
        self.actions.click(self.__btn_bulk_close_cancel, timeout=timeout, raise_exception=False, show_log=False)

    def confirm_close_order(self):
        """Confirm close order action."""
        self.actions.click(self.__btn_confirm_close_order)

    def cancel_close_order(self, timeout=QUICK_WAIT):
        self.actions.click(self.__btn_cancel_close_order, timeout=timeout, raise_exception=False, show_log=False)

    # Edit Confirmation Modal Actions
    def click_btn_edit_order(self):
        self.actions.click(self.__btn_edit_order)

    def cancel_edit_order(self):
        self.actions.click(self.__btn_cancel_edit_order, timeout=QUICK_WAIT, raise_exception=False, show_log=False)

    def confirm_update_order(self):
        self.actions.click(self.__btn_confirm_update_order)

    def get_edit_price(self, order_type: OrderType = OrderType.MARKET):
        """Return current price of the symbol"""
        res = None
        if order_type == OrderType.MARKET:
            res = self.actions.get_text(self.__edit_symbol_price)

        if order_type in [OrderType.LIMIT, OrderType.STOP]:
            res = self.actions.get_text(self.__txt_edit_price)

        if order_type.is_stp_limit():
            res = self.actions.get_text(self.__txt_edit_stop_limit_price)

        logger.debug(f"- Current edit price: {res!r}")
        return res

    def input_edit_sl(self, value, sl_type: SLTPType = SLTPType.PRICE):
        logger.debug(f"- Input stop loss as {sl_type.capitalize()!r}, value: {value!r}")
        locator = cook_element(self.__txt_edit_sl, sl_type.lower())
        self.actions.click(locator)
        self.actions.send_keys(locator, value)
        self.actions.press_done()

    def input_edit_tp(self, value, tp_type: SLTPType = SLTPType.PRICE):
        logger.debug(f"- Input take profit as {tp_type.capitalize()!r}, value: {value!r}")
        locator = cook_element(self.__txt_edit_tp, tp_type.lower())
        self.actions.click(locator)
        self.actions.send_keys(locator, value)
        self.actions.press_done()

    def input_edit_price(self, value):
        logger.debug(f"- Input price: {value!r}")
        self.actions.send_keys(self.__txt_edit_price, value)

    def input_edit_stop_limit_price(self, value):
        logger.debug(f"- Input stop limit price: {value!r}")
        self.actions.send_keys(self.__txt_edit_stop_limit_price, value)

    def modify_order(
            self,
            trade_object: ObjTrade,
            sl_type: SLTPType = None,
            tp_type: SLTPType = None,
            fill_policy: FillPolicy = None,
            expiry: Expiry = None
    ):
        """
        Modify stop loss/ take profit/ fill policy/ Expiry
        trade_object: should contain trade_type and order_type
        sl_type: Price or Points
        tp_type: Price or Points
        fill_policy: None by default, give this value if modifying fill_policy
        """
        trade_type, order_type = trade_object.trade_type, trade_object.order_type
        self.__asset_tab.click_edit_button(AssetTabs.get_tab(order_type), trade_object.get("order_id", 0))

        # Get current price to re-calculate prices
        edit_price = self.get_edit_price(trade_object.order_type) or trade_object.entry_price
        stop_loss, take_profit = get_sl_tp(edit_price, trade_type, sl_type, tp_type)

        if sl_type:
            self.input_edit_sl(stop_loss, sl_type)
            time.sleep(0.5)

        if tp_type:
            self.input_edit_tp(take_profit, tp_type)
            time.sleep(0.5)

        if expiry:
            self.actions.click(self.__drp_expiry)
            self.actions.click(cook_element(self.__option_edit_expiry, locator_format(expiry)))

            if expiry in [Expiry.SPECIFIED_DATE, Expiry.SPECIFIED_DATE_TIME]:
                logger.debug(f"- Select expiry date")
                self.actions.scroll_down()
                self.actions.click(self.__expiry_date)
                self.actions.swipe_picker_wheel_down(self.__wheel_expiry_date)
                self.click_confirm_btn()

            trade_object.expiry = expiry

        if fill_policy:
            self.actions.click(self.__drp_fill_policy)
            self.actions.click(cook_element(self.__opt_edit_fill_policy, locator_format(fill_policy)))
            trade_object.fill_policy = fill_policy

        if sl_type:
            trade_object.stop_loss = self.actions.get_text(cook_element(self.__txt_edit_sl, SLTPType.PRICE.lower()))

        if tp_type:
            trade_object.take_profit = self.actions.get_text(cook_element(self.__txt_edit_tp, SLTPType.PRICE.lower()))

        self.click_btn_edit_order()

    # ------------------------------------------------ VERIFY ------------------------------------------------ #
    def verify_trade_confirmation(self, trade_object: ObjTrade):
        ...

    def verify_edit_trade_confirmation(self, trade_object: ObjTrade):
        ...
