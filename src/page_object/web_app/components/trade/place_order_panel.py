import random
import time
from typing import Any

from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import QUICK_WAIT, SHORT_WAIT, WARNING_ICON
from src.data.enums.trading import OrderType, SLTPType, TradeType, FillPolicy, Expiry
from src.data.objects.symbol_obj import ObjSymbol
from src.data.objects.trade_obj import ObjTrade
from src.page_object.web_app.components.trade.base_trade import BaseTrade
from src.utils.common_utils import cook_element, data_testid
from src.utils.format_utils import locator_format, format_str_price, format_dict_to_string
from src.utils.logging_utils import logger
from src.utils.trading_utils import calculate_trading_params


class PlaceOrderPanel(BaseTrade):
    """
    A class representing the Place Order Panel in the trading interface.
    Handles all interactions with the order placement UI elements and operations.
    """

    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    # One-Click Trading elements
    __toggle_oct = (By.CSS_SELECTOR, data_testid('toggle-oct'))
    __toggle_oct_checked = (By.CSS_SELECTOR, data_testid('toggle-oct-checked'))
    __label_oct = (By.CSS_SELECTOR, "div[data-testid*='toggle-oct']")
    __btn_oct_trade = (By.CSS_SELECTOR, data_testid('trade-button-oct-order-{}'))
    __btn_pre_trade_details = (By.CSS_SELECTOR, data_testid('trade-button-pre-trade-details'))

    # UI control buttons for adjusting values
    __swap_units = (By.CSS_SELECTOR, data_testid('trade-swap-to-units'))
    __swap_volume = (By.CSS_SELECTOR, data_testid('trade-swap-to-volume'))

    # Input field elements
    __txt_volume = (By.CSS_SELECTOR, data_testid('trade-input-volume'))
    __txt_price = (By.CSS_SELECTOR, data_testid('trade-input-price'))
    __txt_stop_loss = (By.CSS_SELECTOR, data_testid('trade-input-stoploss-{}'))
    __txt_take_profit = (By.CSS_SELECTOR, data_testid('trade-input-takeprofit-{}'))
    __txt_stop_limit_price = (By.CSS_SELECTOR, data_testid('trade-input-stop-limit-price'))
    __lbl_units_volume = (By.XPATH, "//input[@data-testid='trade-input-volume']/ancestor::div[1]/following-sibling::div/div[2]")

    # Order placement elements
    __btn_trade = (By.XPATH, "(//div[@data-testid='trade-button-order-{}'])[last()]")
    __drp_order_type = (By.CSS_SELECTOR, data_testid('trade-dropdown-order-type'))
    __opt_order_type = (By.CSS_SELECTOR, data_testid('trade-dropdown-order-type-{}'))
    __btn_place_order = (By.CSS_SELECTOR, data_testid('trade-button-order'))
    __drp_expiry = (By.CSS_SELECTOR, data_testid('trade-dropdown-expiry'))
    __opt_expiry = (By.CSS_SELECTOR, data_testid('trade-dropdown-expiry-{}'))
    __expiry_date = (By.CSS_SELECTOR, data_testid('trade-input-expiry-date'))
    __wheel_expiry_date = (By.CSS_SELECTOR, "div.datepicker-wheel")

    # MT5 specific elements
    __drp_fill_policy = (By.CSS_SELECTOR, data_testid('trade-dropdown-fill-policy'))
    __opt_fill_policy = (By.CSS_SELECTOR, data_testid('trade-dropdown-fill-policy-{}'))

    # ------------------------ HELPER METHODS ------------------------ #
    def _get_volume_info_value(self) -> str:
        """Get current volume/units value from UI."""
        return self.actions.get_text(self.__lbl_units_volume)

    def _get_input_sl(self) -> str:
        """Get current stop loss value from input field."""
        locator = cook_element(self.__txt_stop_loss, SLTPType.PRICE.lower())
        self.actions.click(locator)
        time.sleep(0.5)
        return self.actions.get_value(locator)

    def _get_input_tp(self) -> str:
        """Get current take profit value from input field."""
        locator = cook_element(self.__txt_take_profit, SLTPType.PRICE.lower())
        self.actions.click(locator)
        time.sleep(0.5)
        return self.actions.get_value(locator)

    # ------------------------ ACTIONS ------------------------ #
    def is_oct_enable(self):
        is_enable = self.actions.is_element_displayed(self.__label_oct, timeout=SHORT_WAIT)
        logger.debug(f"- OCT enabled in Admin config: {is_enable!r}")
        return is_enable

    def toggle_oct(self, enable: bool = True, confirm=True) -> None:
        """Enable/disable One-Click Trading."""
        is_enabled = self.actions.is_element_displayed(self.__toggle_oct_checked, timeout=5)
        if is_enabled != enable:
            self.actions.click(self.__toggle_oct if enable else self.__toggle_oct_checked)

            if enable:
                self.confirm_oct(confirm=confirm)

    def open_pre_trade_details(self):
        self.actions.click(self.__btn_pre_trade_details)

    def swap_to_units(self) -> None:
        """Swap to units display."""
        if self.actions.is_element_displayed(self.__swap_units, timeout=1):
            self.actions.click(self.__swap_units)

    def _select_trade_type(self, trade_type: TradeType, normal_mode=True) -> None:
        """Select trade type (BUY/SELL)."""
        logger.debug(f"- Select trade type: {trade_type.upper()!r}")
        self.actions.click(cook_element(self.__btn_trade if normal_mode else self.__btn_oct_trade, trade_type.lower()))

    def _select_order_type(self, order_type: OrderType) -> None:
        """Select order type (MARKET/LIMIT/STOP/STOP_LIMIT)."""
        is_select = order_type.lower() in self.actions.get_text(self.__drp_order_type, timeout=QUICK_WAIT).lower()
        if is_select:
            logger.debug(f"- Order type: {order_type} already selected")
            return

        logger.debug(f"- Select order type: {order_type.capitalize()!r}")
        self.actions.click(self.__drp_order_type)
        self.actions.click(cook_element(self.__opt_order_type, locator_format(order_type)))

    def _select_fill_policy(self, fill_policy: FillPolicy | str):
        """Select the fill policy for the order. Return selected fill_policy"""
        # check current selected fill policy
        self.actions.scroll_to_element(self.__drp_fill_policy)
        is_select = fill_policy.lower() in self.actions.get_text(self.__drp_fill_policy, timeout=QUICK_WAIT).lower()
        if is_select:
            logger.debug(f"- Fill Policy: {fill_policy!r} selected")
            return

        logger.debug(f"- Select fill policy: {fill_policy.capitalize()!r}")
        self.actions.click(self.__drp_fill_policy)
        self.actions.click(cook_element(self.__opt_fill_policy, locator_format(fill_policy)))

    def _select_expiry(self, expiry: Expiry | str, retries=3):
        """Select expiry for the order. Return selected expiry"""

        if not retries:
            logger.warning(f"- Max retries exceeded! Fail to select expiry {WARNING_ICON}")
            return

        self.actions.scroll_to_element(self.__drp_expiry)

        # check if expiry is already selected
        cur_expiry = self.actions.get_text(self.__drp_expiry, timeout=QUICK_WAIT).split("\n")[0].lower()
        logger.debug(f"- Current expiry: {cur_expiry!r}")
        if expiry.lower() == cur_expiry:
            logger.debug(f"> Expiry: {expiry!r} selected")
            return

        locator = locator_format(expiry)
        # handle special locator
        if expiry == Expiry.SPECIFIED_DATE:
            locator = "_".join(item.lower() for item in expiry.split(" "))

        logger.debug(f"- Select expiry: {expiry.title()!r}")
        self.actions.click(self.__drp_expiry)
        time.sleep(0.5)
        self.actions.click(cook_element(self.__opt_expiry, locator))

        # select date in case expiry specified date
        expiry not in [Expiry.SPECIFIED_DATE, Expiry.SPECIFIED_DATE_TIME] or self._select_expiry_date()
        self._select_expiry(expiry, retries - 1)

    def _select_expiry_date(self):
        logger.debug("- Select expiry date")
        self.actions.scroll_to_element(self.__expiry_date)
        self.actions.click(self.__expiry_date)  # open expiry wheel date
        self.actions.scroll_picker_down(self.__wheel_expiry_date)  # scroll picker day
        time.sleep(0.5)
        self.click_confirm_btn()

    def _click_place_order_btn(self) -> None:
        """Click place order button."""
        logger.debug(f"- Click place order button")
        self.actions.click(self.__btn_place_order)

    def _input_sl(self, value: Any, sl_type) -> None:
        """Input stop loss value."""
        if sl_type is None:
            for _type in SLTPType.list_values():
                locator = cook_element(self.__txt_stop_loss, _type.lower())
                self.actions.clear_field(locator)
            return

        locator = cook_element(self.__txt_stop_loss, sl_type.lower())
        self.actions.scroll_to_element(locator)

        logger.debug(f"- Input stop loss: {value!r}")
        self.actions.send_keys(cook_element(self.__txt_stop_loss, sl_type), value)

    def _input_tp(self, value: Any, tp_type) -> None:
        """Input take profit value."""
        if tp_type is None:
            for _type in SLTPType.list_values():
                locator = cook_element(self.__txt_take_profit, _type.lower())
                self.actions.clear_field(locator)
            return

        locator = cook_element(self.__txt_take_profit, tp_type.lower())
        self.actions.scroll_to_element(locator)

        logger.debug(f"- Input take profit: {value!r}")
        self.actions.send_keys(cook_element(self.__txt_take_profit, tp_type), value)

    def _input_volume(self, value):
        """Input volume value."""
        logger.debug(f"- Input volume: {value!r}")
        self.actions.send_keys(self.__txt_volume, value)

    def _input_price(self, value: Any) -> None:
        """Input trade price for order type: Limit, Stop, Stop Limit."""
        logger.debug(f"- Input price: {value!r}")
        self.actions.scroll_to_element(self.__txt_price)
        self.actions.send_keys(self.__txt_price, value)

    def _input_stop_limit_price(self, value: Any) -> None:
        """Input stop limit price for order type 'Stop limit'."""
        logger.debug(f"- Input stop limit price: {value!r}")
        self.actions.scroll_to_element(self.__txt_stop_limit_price)
        self.actions.send_keys(self.__txt_stop_limit_price, value)

    def place_order(
            self,
            trade_object: ObjTrade,
            sl_type: SLTPType = SLTPType.PRICE,
            tp_type: SLTPType = SLTPType.PRICE,
            confirm: bool = True,
    ) -> None:
        """
        Place a valid order and load input data into trade_object.
        Args:
            trade_object: Should contain trade_type and order_type
            sl_type: Type of stop loss (PRICE/POINTS)
            tp_type: Type of take profit (PRICE/POINTS)
            confirm: Whether to submit trade confirmation modal
        """
        trade_type, order_type = trade_object.trade_type, trade_object.order_type

        # Select trade type and order type
        self._select_trade_type(trade_type)
        self._select_order_type(order_type)

        # Handle swap to units
        not trade_object.get("is_units") or self.swap_to_units()

        # Input volume and get units
        trade_object.volume = trade_object.get("volume") or random.randint(1, 5)
        self._input_volume(trade_object.volume)
        units = self._get_volume_info_value()

        # Calculate trade parameters
        prices = calculate_trading_params(self.get_live_price(trade_type), trade_type, order_type, sl_type=sl_type, tp_type=tp_type)

        # Input price if present
        if order_type != OrderType.MARKET:
            self._input_price(prices.entry_price)

        # input stop limit price if present
        if order_type == OrderType.STOP_LIMIT:
            self._input_stop_limit_price(prices.stop_limit_price)

        # Select fill_policy
        if trade_object.get("fill_policy"):
            self._select_fill_policy(trade_object.fill_policy)

        # Input stop loss - handle clear field when sl_type = None
        stop_loss = prices.stop_loss
        self._input_sl(stop_loss, sl_type)
        stop_loss = self._get_input_sl() if sl_type == SLTPType.POINTS else stop_loss

        # input take profit - handle clear field when sl_type = None
        take_profit = prices.take_profit
        self._input_tp(take_profit, tp_type)
        take_profit = self._get_input_tp() if tp_type == SLTPType.POINTS else take_profit

        # select expiry
        if trade_object.get("expiry"):
            self._select_expiry(trade_object.expiry)

        # Update placed order details back to trade_object
        volume, units = (trade_object.volume, units) if not trade_object.get("is_units") else (units, trade_object.volume)
        trade_details = {
            'volume': format_str_price(volume),
            'units': format_str_price(units),
            'entry_price': self.get_live_price(trade_type) if order_type == OrderType.MARKET else prices.entry_price,
            'stop_limit_price': prices.stop_limit_price,
            'stop_loss': '--' if sl_type is None else stop_loss,
            'take_profit': '--' if tp_type is None else take_profit,
            'sl_type': sl_type,
            'tp_type': tp_type
        }

        logger.debug(f"- Order Summary: {format_dict_to_string(trade_details)}")
        trade_object |= {k: v for k, v in trade_details.items()}

        # Place order
        self._click_place_order_btn()
        if confirm:
            self.get_current_price(trade_object)  # get most recent current_price
            self.confirm_trade()  # confirm placing order

    def place_oct_order(self, trade_object: ObjTrade) -> None:
        # Input volume and get units
        volume = trade_object.get("volume") or random.randint(1, 5)
        self._input_volume(volume)
        units = volume * trade_object.CONTRACT_SIZE

        # Prepare trade details
        trade_details = {
            'volume': format_str_price(volume),
            'units': format_str_price(units),
            'entry_price': self.get_live_price(trade_object.trade_type, oct_mode=True),
            'stop_loss': '--',
            'take_profit': '--'
        }

        logger.debug(f"- Order Summary: {format_dict_to_string(trade_details)}")
        trade_object |= {k: v for k, v in trade_details.items()}

        # Place Order
        self._select_trade_type(trade_object.trade_type, normal_mode=False)

    # ------------------------ VERIFY ------------------------ #

    def verify_oct_mode(self, enable=True):
        logger.debug(f"- Check OCT button is {'enabled' if enable else 'disabled'}")
        self.actions.verify_element_displayed(self.__toggle_oct_checked if enable else self.__toggle_oct)

        logger.debug(f"- Check pre-trade details tab is {'displayed' if enable else 'not displayed'}")
        self.actions.verify_element_displayed(self.__btn_pre_trade_details, is_display=enable)
