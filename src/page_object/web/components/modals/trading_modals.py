import random
import time

from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import QUICK_WAIT
from src.data.enums import OrderType, SLTPType, FillPolicy, Expiry, AssetTabs
from src.data.objects.trade_obj import ObjTrade
from src.page_object.web.components.trade.asset_tab import AssetTab
from src.page_object.web.components.trade.base_trade import BaseTrade
from src.utils import DotDict
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import data_testid, cook_element
from src.utils.format_utils import locator_format
from src.utils.logging_utils import logger
from src.utils.trading_utils import get_sl_tp, get_pending_price, get_stop_price


class TradingModals(BaseTrade):
    def __init__(self, actions: WebActions):
        super().__init__(actions)
        self.__asset_tab = AssetTab(actions)

    # ------------------------------------------------ LOCATORS ------------------------------------------------ #
    ##### Trade Confirmation Modal #####
    __btn_cancel_trade = (By.XPATH, "//div[text()='Trade Confirmation']/parent::div/following-sibling::div")
    __confirm_order_type = (By.CSS_SELECTOR, data_testid('trade-confirmation-order-type'))
    __confirm_symbol = (By.CSS_SELECTOR, data_testid('trade-confirmation-symbol'))
    __confirm_volume = (
        By.XPATH,
        "//div[@data-testid='trade-confirmation-label' "
        "and (contains(normalize-space(text()), 'Volume') or contains(normalize-space(text()), 'Size'))]"
        "/following-sibling::div"
    )
    __confirm_units = (
        By.XPATH, "//div[@data-testid='trade-confirmation-label' and normalize-space(text())='Units']/following-sibling::div"
    )
    __confirm_price = (
        By.XPATH, "//div[@data-testid='trade-confirmation-label' and normalize-space(text())='Price']/following-sibling::div"
    )
    __confirm_stp_limit_price = (
        By.XPATH, "//div[@data-testid='trade-confirmation-label' and normalize-space(text())='Stop Limit Price']/following-sibling::div"
    )
    __confirm_stop_loss = (
        By.XPATH, "//div[@data-testid='trade-confirmation-label' and normalize-space(text())='Stop Loss']/following-sibling::div"
    )
    __confirm_take_profit = (
        By.XPATH,
        "//div[@data-testid='trade-confirmation-label' and normalize-space(text())='Take Profit']/following-sibling::div"
    )
    __confirm_expiry = (
        By.XPATH,
        "//div[@data-testid='trade-confirmation-label' and normalize-space(text())='Expiry']/following-sibling::div"
    )
    __confirm_fill_policy = (
        By.XPATH,
        "//div[@data-testid='trade-confirmation-label' and normalize-space(text())='Fill Policy']/following-sibling::div"
    )

    ##### Edit Confirmation Modal #####
    __btn_edit_order = (By.CSS_SELECTOR, data_testid('edit-button-order'))
    __txt_edit_sl = (By.CSS_SELECTOR, data_testid('edit-input-stoploss-{}'))  # price or points
    __txt_edit_tp = (By.CSS_SELECTOR, data_testid('edit-input-takeprofit-{}'))  # price or points
    __txt_edit_price = (By.CSS_SELECTOR, data_testid('edit-input-price'))
    __txt_edit_stp_price = (By.CSS_SELECTOR, data_testid('edit-input-stop-limit-price'))

    __drp_edit_expiry = (By.CSS_SELECTOR, data_testid('edit-dropdown-expiry'))
    __opt_edit_expiry = (By.CSS_SELECTOR, data_testid('edit-dropdown-expiry-{}'))
    __txt_edit_expiry_date = (By.CSS_SELECTOR, data_testid('edit-input-expiry-date'))
    __expiry_last_date = (By.XPATH, "(//button[contains(@class, 'month-view')])[last()]")

    __drp_edit_fill_policy = (By.CSS_SELECTOR, data_testid('edit-dropdown-fill-policy'))
    __opt_edit_fill_policy = (By.CSS_SELECTOR, data_testid('edit-dropdown-fill-policy-{}'))

    __btn_confirm_update_order = (By.CSS_SELECTOR, data_testid('edit-confirmation-button-confirm'))
    __edit_symbol_price = (By.CSS_SELECTOR, data_testid('edit-symbol-price'))
    __edit_confirm_order_id = (By.CSS_SELECTOR, data_testid('edit-confirmation-order-id'))
    __edit_confirm_order_type = (By.CSS_SELECTOR, data_testid('edit-confirmation-order-type'))
    __edit_confirm_symbol = (By.CSS_SELECTOR, data_testid('edit-confirmation-symbol'))
    __edit_confirm_volume = (
        By.XPATH, "//div[@data-testid='edit-confirmation-label' and (text()='Volume' or text()='Size')]/following-sibling::div"
    )
    __edit_confirm_units = (By.XPATH, "//div[@data-testid='edit-confirmation-label' and text()='Units']/following-sibling::div")
    __edit_confirm_stop_loss = (By.XPATH, "//div[@data-testid='edit-confirmation-label' and text()='Stop Loss']/following-sibling::div")
    __edit_confirm_take_profit = (By.XPATH, "//div[@data-testid='edit-confirmation-label' and text()='Take Profit']/following-sibling::div")
    __edit_confirm_fill_policy = (By.XPATH, "//div[@data-testid='edit-confirmation-label' and text()='Fill Policy']/following-sibling::div")
    __edit_confirm_expiry = (By.XPATH, "//div[@data-testid='edit-confirmation-label' and text()='Expiry']/following-sibling::div")

    # control buttons
    __btn_inc_dec_sl = (By.CSS_SELECTOR, data_testid('edit-input-stoploss-{}-{}'))  # price/ points - increase/ decrease
    __btn_inc_dec_tp = (By.CSS_SELECTOR, data_testid('edit-input-takeprofit-{}-{}'))
    __btn_inc_dec_price = (By.CSS_SELECTOR, data_testid('edit-input-price-{}'))
    __btn_inc_dec_stp_price = (By.CSS_SELECTOR, data_testid('edit-input-stop-limit-price-{}'))

    # ------------------------------------------------ ACTIONS ------------------------------------------------ #
    def close_trade_confirm_modal(self, timeout=QUICK_WAIT):
        self.actions.click(self.__btn_cancel_trade, timeout=timeout, raise_exception=False, show_log=False)

    # Edit Confirmation Modal Actions
    def close_edit_confirm_modal(self, timeout=QUICK_WAIT):
        self.actions.click_by_offset(self.__edit_confirm_order_id, x_offset=173, y_offset=-12, timeout=timeout, raise_exception=False)
        self.actions.click_by_offset(
            self.__edit_confirm_order_type, 300, 20, timeout=timeout, raise_exception=False
        )

    def click_edit_order_btn(self):
        """Click the edit order button."""
        time.sleep(1)
        self.actions.click(self.__btn_edit_order)

    def confirm_update_order(self):
        """Click the confirm update order button."""
        self.actions.click(self.__btn_confirm_update_order)

    def _get_edit_price(self, order_type: OrderType = None):
        """Return current price of the symbol"""
        time.sleep(0.5)
        if not order_type or order_type == OrderType.MARKET:
            return self.actions.get_text(self.__edit_symbol_price)

        return self.actions.get_value(self.__txt_edit_price)

    def _get_edit_sl(self):
        locator = cook_element(self.__txt_edit_sl, SLTPType.PRICE.lower())
        self.actions.click(locator)
        res = self.actions.get_value(locator, retry=True)
        logger.debug(f"- Edit SL: {res!r}")
        return res

    def _get_edit_tp(self):
        locator = cook_element(self.__txt_edit_tp, SLTPType.PRICE.lower())
        self.actions.click(locator)
        res = self.actions.get_value(locator, retry=True)
        logger.debug(f"- Edit TP: {res!r}")
        return res

    def _input_edit_sl(self, value, sl_type: SLTPType = SLTPType.PRICE):
        if sl_type is None:
            return

        logger.debug(f"Input edit SL: {value} - type: {sl_type.lower()}")
        locator = cook_element(self.__txt_edit_sl, sl_type.lower())
        self.actions.clear_field(locator)
        time.sleep(1)
        self.actions.send_keys(locator, value)

    def _input_edit_tp(self, value, tp_type: SLTPType = SLTPType.PRICE):
        if tp_type is None:
            return

        logger.debug(f"Input edit TP: {value} - type: {tp_type.lower()}")
        locator = cook_element(self.__txt_edit_tp, tp_type.lower())
        self.actions.clear_field(locator)
        time.sleep(1)
        self.actions.send_keys(locator, value)

    def _input_edit_price(self, value, order_type: OrderType | str = None):
        if not order_type or order_type == OrderType.MARKET:
            return

        logger.debug(f"Input edit price: {value}")
        self.actions.send_keys(self.__txt_edit_price, value)

    def _input_edit_stp_price(self, value, order_type: OrderType | str = None):
        if not order_type or not order_type.is_stp_limit():
            return

        logger.debug(f"Input edit STP price: {value}")
        self.actions.send_keys(self.__txt_edit_stp_price, value)

    def _select_fill_policy(self, fill_policy):
        if not fill_policy:
            return

        logger.debug(f"Select fill policy: {fill_policy}")
        self.actions.click(self.__drp_edit_fill_policy)
        self.actions.click(cook_element(self.__opt_edit_fill_policy, locator_format(fill_policy)))

    def _select_expiry(self, expiry):
        if not expiry:
            return

        logger.debug(f"Select expiry: {expiry}")
        self.actions.click(self.__drp_edit_expiry)
        self.actions.click(cook_element(self.__opt_edit_expiry, locator_format(expiry)))

        if expiry in [Expiry.SPECIFIED_DATE, Expiry.SPECIFIED_DATE_TIME]:
            logger.debug("Select expiry date")
            self.actions.click(self.__txt_edit_expiry_date)
            self.actions.click(self.__expiry_last_date)

    # Control buttons
    def __control_price(self, order_type: OrderType, stp_price=True, price=True, stop_loss=True, take_profit=True):

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

    def modify_order(
            self,
            trade_object: ObjTrade,
            tab: AssetTabs = None,
            sl_type: SLTPType = None,
            tp_type: SLTPType = None,
            fill_policy: FillPolicy = None,
            expiry: Expiry = None,
            confirm=False
    ):
        """
        Modify stop loss/ take profit/ fill policy/ Expiry
        trade_object: should contain trade_type and order_type
        sl_type: Price or Points
        tp_type: Price or Points
        fill_policy: None by default, give this value if modifying fill_policy
        expiry: same with fill_policy
        """
        tab = tab or AssetTabs.get_tab(trade_object.order_type)
        self.__asset_tab.click_edit_button(tab, trade_object.get("order_id"))

        trade_type, order_type = trade_object.trade_type, trade_object.order_type
        edit_price = trade_object.get("stop_limit_price") or trade_object.get("entry_price") or self._get_edit_price()

        logger.debug(f"- Edit price is {edit_price!r}")
        stop_loss, take_profit = get_sl_tp(edit_price, trade_type, sl_type, tp_type).values()

        self._input_edit_sl(stop_loss, sl_type)
        if sl_type == SLTPType.POINTS:
            sl = self._get_edit_sl()
            if "-" in sl:
                logger.debug("- Fall back - stop loss is negative, re-input")
                self._input_edit_sl(stop_loss, sl_type)
                sl = self._get_edit_sl()
            stop_loss = sl

        self._input_edit_tp(take_profit, tp_type)
        if tp_type == SLTPType.POINTS:
            tp = self._get_edit_tp()
            if "-" in tp:
                logger.debug("- Fall back - take profit is negative, re-input")
                self._input_edit_tp(take_profit, tp_type)
                tp = self._get_edit_tp()
            take_profit = tp

        if expiry:
            self._select_expiry(expiry)
            trade_object["expiry"] = expiry

        if fill_policy:
            self._select_fill_policy(fill_policy)
            trade_object["fill_policy"] = fill_policy

        self.click_edit_order_btn()

        # update trade object
        if sl_type:
            trade_object.stop_loss = stop_loss
            trade_object.sl_type = sl_type

        if tp_type:
            trade_object.take_profit = take_profit
            trade_object.tp_type = tp_type

        if confirm:
            time.sleep(1)
            self.confirm_update_order()

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
        self.__asset_tab.click_edit_button(AssetTabs.get_tab(order_type), trade_object.get("order_id"))

        if entry_price:
            price = get_pending_price(self._get_edit_price(), trade_type, order_type, True)
            self._input_edit_price(price, order_type)

        if stop_limit_price:
            stp_price = get_stop_price(self._get_edit_price(order_type), trade_type, True)
            self._input_edit_stp_price(stp_price, order_type)

        invalid_sl_tp = get_sl_tp(
            self._get_edit_price(order_type), trade_type, True
        )
        if stop_loss:
            sl = invalid_sl_tp.sl.price
            self._input_edit_sl(sl)

        if take_profit:
            tp = invalid_sl_tp.tp.price
            self._input_edit_tp(tp)

        self.click_edit_order_btn()
        if submit:
            self.confirm_update_order()

    def modify_order_with_control_buttons(
            self, trade_object: DotDict = None,
            stop_loss=True,
            take_profit=True,
    ):
        stop_limit_price = trade_object.order_type.is_stp_limit()
        price = not trade_object.order_type == OrderType.MARKET

        self.__control_price(trade_object.order_type, stop_limit_price, price, stop_loss, take_profit)

        # Load data to trade_object for verifying
        edit_sl = self.actions.get_value(cook_element(self.__txt_edit_sl, SLTPType.PRICE.lower()))
        edit_tp = self.actions.get_value(cook_element(self.__txt_edit_tp, SLTPType.PRICE.lower()))

        trade_object.stop_loss = edit_sl
        trade_object.take_profit = edit_tp

        if trade_object.order_type != OrderType.MARKET:
            trade_object.entry_price = self.actions.get_value(self.__txt_edit_price)

        if trade_object.order_type == OrderType.STOP_LIMIT:
            trade_object.stop_limit_price = self.actions.get_value(self.__txt_edit_stp_price)

        self.click_edit_order_btn()
        self.confirm_update_order()

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
        not expected.get("fill_policy") or locator_list.append(self.__confirm_fill_policy)
        not expected.get("expiry") or locator_list.append(self.__confirm_expiry)

        if trade_object.order_type != OrderType.MARKET:
            locator_list.append(self.__confirm_price)

        if trade_object.order_type.is_stp_limit():
            locator_list.append(self.__confirm_stp_limit_price)

        actual = {
            k: v for k, v in zip(expected, [self.actions.get_text(locator) for locator in locator_list])
        }

        soft_assert(actual, expected, tolerance=0.5, tolerance_fields=trade_object.tolerance_fields())

    def verify_trade_edit_confirm_details(self, trade_object: ObjTrade):
        expected = trade_object.trade_edit_confirm_details()
        actual_locators = [
            self.__edit_confirm_order_id,
            self.__edit_confirm_order_type,
            self.__edit_confirm_symbol,
            self.__edit_confirm_volume,
            self.__edit_confirm_units,
            self.__edit_confirm_stop_loss,
            self.__edit_confirm_take_profit,
        ]

        not expected.get("fill_policy") or actual_locators.append(self.__edit_confirm_fill_policy)
        not expected.get("expiry") or actual_locators.append(self.__edit_confirm_expiry)

        actual = {
            k: v for k, v in zip(list(expected.keys()), [self.actions.get_text(locator) for locator in actual_locators])
        }

        soft_assert(actual, expected, tolerance=0.5, tolerance_fields=trade_object.tolerance_fields())
