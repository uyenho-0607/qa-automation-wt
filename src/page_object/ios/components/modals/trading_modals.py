import random
import time

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import QUICK_WAIT
from src.data.enums import BulkCloseOpts, OrderType, SLTPType, FillPolicy, Expiry, AssetTabs
from src.data.objects.trade_obj import ObjTrade
from src.page_object.ios.components.trade.asset_tab import AssetTab
from src.page_object.ios.components.trade.base_trade import BaseTrade
from src.utils import DotDict
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import resource_id, cook_element
from src.utils.format_utils import locator_format
from src.utils.logging_utils import logger
from src.utils.trading_utils import get_sl_tp, calculate_trading_params


class TradingModals(BaseTrade):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)
        self.__asset_tab = AssetTab(actions)

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

    # Control buttons
    def __control_price(self, order_type, stop_limit_price=True, price=True, stop_loss=True, take_profit=True):

        if stop_limit_price and order_type == OrderType.STOP_LIMIT:
            for _ in range(random.randint(10, 20)):
                self.actions.click(cook_element(self.__btn_inc_dec_stop_limit_price, "increase"))

            for _ in range(random.randint(1, 10)):
                self.actions.click(cook_element(self.__btn_inc_dec_stop_limit_price, "decrease"))

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

        # if order_type != OrderType.MARKET:
        #     self.input_edit_price(trade_params.entry_price)
        #     trade_object.entry_price = trade_params.entry_price
        #
        # if order_type.is_stp_limit():
        #     self.input_edit_stop_limit_price(trade_params.stop_limit_price)
        #     trade_object.stop_limit_price = trade_params.stop_limit_price

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

    def modify_invalid_order(
            self,
            trade_object: DotDict,
            stop_loss=False,
            take_profit=False,
            entry_price=False,
            stop_limit_price=False,
            submit=False
    ):
        """
        Modify invalid order with option
        trade_object: Should contain trade_type (BUY / SELL), order_type (MARKET/ LIMIT/ STOP/ STOP LIMIT)
        stop_loss: set to True >> stop_loss will be invalid
        take_profit: set to True >> take_profit will be invalid
        entry_price: set to True >> entry_price will be invalid
        stop_limit_price: set to True >> stop_limit_price will be invalid
        NOTE: whether stop_loss/ take_profit is invalid or entry_price is invalid
        """

        trade_type, order_type = trade_object.trade_type, trade_object.order_type

        edit_price = self.get_edit_price(trade_object.order_type)
        invalid_price = calculate_trading_params(edit_price, trade_type, order_type, is_invalid=True)

        if entry_price:
            price = invalid_price.entry_price
            self.input_edit_price(price)

        if stop_limit_price:
            stp_price = invalid_price.stop_limit_price
            self.input_edit_stop_limit_price(stp_price)

        if stop_loss:
            sl = invalid_price.stop_loss
            self.input_edit_sl(sl)

        if take_profit:
            tp = invalid_price.take_profit
            self.input_edit_tp(tp)

        self.click_btn_edit_order()
        if submit:
            self.confirm_update_order()

    def modify_order_with_control_buttons(
            self, trade_object: DotDict = None,
            stop_limit_price=True, price=True,
            stop_loss=True,
            take_profit=True,
    ):
        self.__control_price(trade_object.order_type, stop_limit_price, price, stop_loss, take_profit)

        # Load data to trade_object for verifying
        edit_sl = self.actions.get_text(cook_element(self.__txt_edit_sl, SLTPType.PRICE.lower()))
        edit_tp = self.actions.get_text(cook_element(self.__txt_edit_tp, SLTPType.PRICE.lower()))

        trade_object.stop_loss = edit_sl
        trade_object.take_profit = edit_tp

        if trade_object.order_type != OrderType.MARKET:
            trade_object.entry_price = self.actions.get_text(self.__txt_edit_price)

        if trade_object.order_type == OrderType.STOP_LIMIT:
            trade_object.stop_limit_price = self.actions.get_text(self.__txt_edit_stop_limit_price)

        self.click_btn_edit_order()

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

        soft_assert(actual, expected, tolerance=0.1, tolerance_fields=trade_object.tolerance_fields())

    def verify_edit_trade_confirmation(self, trade_object: ObjTrade):

        expected = trade_object.trade_edit_confirm_details()

        actual = {
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

        soft_assert(actual, expected)
