import random
import time
from typing import Literal, Optional, Any

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.enums.trading import OrderType, SLTPType, TradeType, FillPolicy, Expiry
from src.data.objects.trade_object import ObjectTrade
from src.data.project_info import ProjectConfig
from src.page_object.android.components.trade.base_trade import BaseTrade
from src.utils import DotDict
from src.utils.common_utils import cook_element, resource_id
from src.utils.format_utils import locator_format, add_commas, format_dict_to_string, is_integer
from src.utils.logging_utils import logger
from src.utils.trading_utils import calculate_trade_parameters


class PlaceOrderPanel(BaseTrade):
    """
    A class representing the Place Order Panel in the trading interface.
    Handles all interactions with the order placement UI elements and operations.
    """

    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    # One-Click Trading elements
    __toggle_oct = (AppiumBy.XPATH, resource_id('toggle-oct'))
    __toggle_oct_checked = (AppiumBy.XPATH, resource_id('toggle-oct-checked'))
    __btn_oct_trade = (AppiumBy.XPATH, resource_id('trade-button-oct-order-{}'))
    __btn_pre_trade_details = (AppiumBy.XPATH, resource_id('trade-button-pre-trade-details'))

    # UI control buttons for adjusting values
    __inc_dec_volume = (AppiumBy.XPATH, resource_id('trade-input-volume-{}'))
    __inc_dec_sl = (AppiumBy.XPATH, resource_id('trade-input-stoploss-{}-{}'))
    __inc_dec_tp = (AppiumBy.XPATH, resource_id('trade-input-takeprofit-{}-{}'))
    __inc_dec_price = (AppiumBy.XPATH, resource_id('trade-input-price-{}'))
    __inc_dec_stop_limit = (AppiumBy.XPATH, resource_id('trade-input-stop-limit-price-{}'))
    __swap_units = (AppiumBy.XPATH, resource_id('trade-swap-to-units'))
    __swap_volume = (AppiumBy.XPATH, resource_id('trade-swap-to-volume'))

    # Input field elements
    __txt_volume = (AppiumBy.XPATH, resource_id('trade-input-volume'))
    __txt_price = (AppiumBy.XPATH, resource_id('trade-input-price'))
    __txt_stop_loss = (AppiumBy.XPATH, resource_id('trade-input-stoploss-{}', ))
    __txt_take_profit = (AppiumBy.XPATH, resource_id('trade-input-takeprofit-{}', ))
    __txt_stop_limit_price = (AppiumBy.XPATH, resource_id('trade-input-stop-limit-price'))
    __volume_info_value = (
        AppiumBy.XPATH,
        "//*[@text='Units' or @text='Volume' or @text='Size']/following-sibling::android.widget.TextView[1]"
    )

    # Order placement elements
    __btn_trade = (AppiumBy.XPATH, resource_id('trade-button-order-{}'))
    __drp_order_type = (AppiumBy.XPATH, resource_id('trade-dropdown-order-type'))
    __opt_order_type = (AppiumBy.XPATH, resource_id('trade-dropdown-order-type-{}', "android.view.ViewGroup"))
    __btn_place_order = (AppiumBy.XPATH, resource_id('trade-button-order'))
    __drp_expiry = (AppiumBy.XPATH, resource_id('trade-dropdown-expiry'))
    __opt_expiry = (AppiumBy.XPATH,
                    "//android.view.ViewGroup[contains(translate(@content-desc, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('{}', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))]")
    __expiry_date = (AppiumBy.XPATH, resource_id('trade-input-expiry-date'))
    __wheel_expiry_date = (AppiumBy.XPATH, "//android.widget.SeekBar[contains(@content-desc, 'Select Date')]")

    # MT5 specific elements
    __drp_fill_policy = (AppiumBy.XPATH, resource_id('trade-dropdown-fill-policy'))
    __opt_fill_policy = (AppiumBy.XPATH, resource_id('trade-dropdown-fill-policy-{}'))

    # ------------------------ HELPER METHODS ------------------------ #
    def _get_volume_info_value(self) -> str:
        """Get current volume/units value from UI."""
        return self.actions.get_text(self.__volume_info_value)

    def _get_input_sl(self) -> str:
        """Get the current stop loss value from the input field."""
        return self.actions.get_text(cook_element(self.__txt_stop_loss, SLTPType.PRICE.lower()))

    def _get_input_tp(self) -> str:
        """Get the current take profit value from the input field."""
        return self.actions.get_text(cook_element(self.__txt_take_profit, SLTPType.PRICE.lower()))

    def _input_trade_value(self, locator: tuple[str, str], value: Any, value_type: str) -> None:
        """Input value into a trade field."""
        logger.debug(f"- Input {value_type}: {value!r}")
        self.actions.send_keys(locator, value)

    # ------------------------ ACTIONS ------------------------ #
    def get_min_volume(self) -> Optional[str]:
        """Get minimum allowed volume from placeholder."""
        value = self.actions.get_attribute(self.__txt_volume, "placeholder")
        if value:
            return value.split(": ")[-1]
        return None

    def toggle_oct(self, enable: bool = True) -> None:
        """Enable/disable One-Click Trading."""
        is_enabled = self.actions.is_element_displayed(self.__toggle_oct_checked, timeout=1)
        if is_enabled == enable:
            return

        self.actions.click(self.__toggle_oct if enable else self.__toggle_oct_checked)
        if enable:
            self.agree_and_continue()

    def open_pre_trade_details(self):
        self.actions.click(self.__btn_pre_trade_details)

    def _control_inc_dec_btn(
            self,
            button_type: Literal["volume", "sl", "tp", "price", "stop_limit"],
            inc_step: Optional[int] = None,
            dec_step: Optional[int] = None,
            sl_tp_type: SLTPType = SLTPType.PRICE
    ) -> None:
        """
        Adjust a value using increase/decrease buttons.
        Args:
            button_type: Type of value to adjust
            inc_step: Number of times to click increase button
            dec_step: Number of times to click decrease button
            sl_tp_type: Type of SL/TP adjustment (PRICE/POINTS)
        """
        locators = {
            "volume": self.__inc_dec_volume,
            "sl": self.__inc_dec_sl,
            "tp": self.__inc_dec_tp,
            "price": self.__inc_dec_price,
            "stop_limit": self.__inc_dec_stop_limit
        }

        inc_step = inc_step or random.randint(10, 20)
        dec_step = dec_step or random.randint(1, inc_step - 1)

        for _ in range(inc_step):
            if button_type in ["sl", "tp"]:
                self.actions.click(cook_element(locators[button_type], sl_tp_type.lower(), "increase"))
            else:
                self.actions.click(cook_element(locators[button_type], "increase"))

        for _ in range(dec_step):
            if button_type in ["sl", "tp"]:
                self.actions.click(cook_element(locators[button_type], sl_tp_type.lower(), "decrease"))
            else:
                self.actions.click(cook_element(locators[button_type], "decrease"))

    def control_volume(self, inc_step: Optional[int] = None, dec_step: Optional[int] = None) -> None:
        """Adjust volume using control buttons."""
        self._control_inc_dec_btn("volume", inc_step, dec_step)

    def control_sl(self, inc_step: Optional[int] = None, dec_step: Optional[int] = None, sl_type: SLTPType = SLTPType.PRICE) -> None:
        """Adjust stop loss using control buttons."""
        self._control_inc_dec_btn("sl", inc_step, dec_step, sl_type)

    def control_tp(self, inc_step: Optional[int] = None, dec_step: Optional[int] = None, tp_type: SLTPType = SLTPType.PRICE) -> None:
        """Adjust take profit using control buttons."""
        self._control_inc_dec_btn("tp", inc_step, dec_step, tp_type)

    def control_price(self, inc_step: Optional[int] = None, dec_step: Optional[int] = None, order_type: OrderType = OrderType.LIMIT) -> None:
        """Adjust price using control buttons."""
        if order_type != OrderType.MARKET:
            self._control_inc_dec_btn("price", inc_step, dec_step)

    def control_stop_limit(self, inc_step: Optional[int] = None, dec_step: Optional[int] = None, order_type: OrderType = OrderType.STOP_LIMIT) -> None:
        """Adjust stop limit price using control buttons."""
        if order_type.is_stp_limit():
            self._control_inc_dec_btn("stop_limit", inc_step, dec_step)

    def swap_to_units(self) -> None:
        """Swap to units display."""
        if self.actions.is_element_displayed(self.__swap_units, timeout=1):
            self.actions.click(self.__swap_units)

    def swap_to_volume(self) -> None:
        """Swap to volume display."""
        if self.actions.is_element_displayed(self.__swap_volume, timeout=1):
            self.actions.click(self.__swap_volume)

    def _select_trade_type(self, trade_type: TradeType) -> None:
        """Select trade type (BUY/SELL)."""
        logger.debug(f"- Select trade type: {trade_type.upper()!r}")
        self.actions.click(cook_element(self.__btn_trade, trade_type.lower()))

    def _select_order_type(self, order_type: OrderType) -> None:
        """Select order type (MARKET/LIMIT/STOP/STOP_LIMIT)."""
        logger.debug(f"- Select order type: {order_type.capitalize()!r}")
        self.actions.click(self.__drp_order_type)
        self.actions.click(cook_element(self.__opt_order_type, locator_format(order_type)))

    def _select_fill_policy(self, fill_policy: FillPolicy | str) -> Optional[str]:
        """Select the fill policy for the order. Return selected fill_policy"""
        if not ProjectConfig.is_non_oms() or not fill_policy:
            return None

        logger.debug(f"- Select fill policy: {fill_policy.capitalize()!r}")
        self.actions.click(self.__drp_fill_policy)
        self.actions.click(cook_element(self.__opt_fill_policy, locator_format(fill_policy)))
        return fill_policy

    def _select_expiry(self, expiry: Expiry | str) -> Optional[str]:
        """Select expiry for the order. Return selected expiry"""
        if expiry:
            logger.debug(f"- Select expiry: {expiry.capitalize()!r}")
            self.actions.click(self.__drp_expiry)
            self.actions.click(cook_element(self.__opt_expiry, expiry.lower()))

            if expiry in [Expiry.SPECIFIED_DATE, Expiry.SPECIFIED_DATE_TIME]:
                logger.debug(f"- Select expiry date")
                self.actions.scroll_down()
                self.actions.click(self.__expiry_date)
                self.actions.swipe_picker_wheel_down(self.__wheel_expiry_date)
                self.click_confirm_btn()
            return expiry

        return None

    def _click_place_order_btn(self) -> None:
        """Click place order button."""
        logger.debug(f"- Click place order button")
        self.actions.click(self.__btn_place_order)

    def _input_stop_loss(self, value: Any) -> None:
        """Input stop loss value."""
        sl_type = SLTPType.POINTS if is_integer(value) else SLTPType.PRICE
        self.actions.click(cook_element(self.__txt_stop_loss, sl_type.lower()))
        self._input_trade_value(cook_element(self.__txt_stop_loss, sl_type), value, "stop loss")
        self.actions.press_done()

    def _input_take_profit(self, value: Any) -> None:
        """Input take profit value."""
        tp_type = SLTPType.POINTS if is_integer(value) else SLTPType.PRICE
        self.actions.click(cook_element(self.__txt_take_profit, tp_type.lower()))
        self._input_trade_value(cook_element(self.__txt_take_profit, tp_type), value, "take profit")
        self.actions.press_done()

    def _input_volume(self, value: Optional[int] = None) -> int:
        """Input volume value."""
        volume = value if value is not None else random.randint(2, 10)
        self._input_trade_value(self.__txt_volume, volume, "volume")
        return volume

    def _input_price(self, value: Any, order_type: Optional[OrderType] = None) -> None:
        """Input trade price for order type: Limit, Stop, Stop Limit."""
        if order_type == OrderType.MARKET:
            return
        self._input_trade_value(self.__txt_price, value, "price")

    def _input_stop_limit_price(self, value: Any, order_type: Optional[OrderType] = None) -> None:
        """Input stop limit price for order type 'Stop limit'."""
        if order_type != OrderType.STOP_LIMIT:
            return
        self._input_trade_value(self.__txt_stop_limit_price, value, "stop limit price")

    def place_order(
            self,
            trade_object: ObjectTrade,
            sl_type: SLTPType = SLTPType.PRICE,
            tp_type: SLTPType = SLTPType.PRICE,
            swap_to_units: bool = False,
            submit: bool = False,
    ) -> None:
        """
        Place a valid order and load input data into trade_object.
        Args:
            trade_object: Should contain trade_type and order_type
            sl_type: Type of stop loss (PRICE/POINTS)
            tp_type: Type of take profit (PRICE/POINTS)
            swap_to_units: Whether to swap to units display
            submit: Whether to submit trade confirmation modal
        """
        trade_type, order_type = trade_object.trade_type, trade_object.order_type

        # Select trade type and order type
        self._select_trade_type(trade_type)
        self._select_order_type(order_type)

        # Handle volume display
        not swap_to_units or self.swap_to_units()

        # Input volume and get units
        volume = self._input_volume()
        units = volume / ObjectTrade.CONTRACT_SIZE if ObjectTrade.CONTRACT_SIZE else self._get_volume_info_value()

        # Calculate trade parameters
        params = calculate_trade_parameters(
            self.get_live_price(trade_type), trade_type, order_type, sl_type=sl_type, tp_type=tp_type
        )

        # Input prices
        self._input_price(params.entry_price, order_type)
        self._input_stop_limit_price(params.stop_limit_price, order_type)
        self.actions.scroll_down(amount=1)  # scroll down a bit

        # Input SL/TP if needed
        if sl_type is not None:
            stop_loss = params.stop_loss
            self._input_stop_loss(stop_loss)

        if tp_type is not None:
            take_profit = params.take_profit
            self._input_take_profit(take_profit)

        # Select fill policy and expiry
        fill_policy = self._select_fill_policy(trade_object.fill_policy)
        expiry = self._select_expiry(trade_object.get("expiry", None))

        # Get final values for SL/TP if using points
        if sl_type == SLTPType.POINTS:
            stop_loss = self._get_input_sl()

        if tp_type == SLTPType.POINTS:
            take_profit = self._get_input_tp()

        # Prepare trade details
        volume, units = (volume, units) if not swap_to_units else (units, volume)

        entry_price = self.get_live_price(trade_type)
        trade_details = {
            'live_price': self.get_live_price(trade_type),
            'volume': add_commas(volume),
            'units': add_commas(units),
            'entry_price': entry_price if order_type == OrderType.MARKET else params.entry_price,
            'stop_limit_price': params.stop_limit_price,
            'stop_loss': '--' if sl_type is None else stop_loss,
            'take_profit': '--' if tp_type is None else take_profit,
            'fill_policy': fill_policy,
            'expiry': expiry
        }

        logger.debug(f"- Order Summary: {format_dict_to_string(trade_details)}")
        trade_object |= {k: v for k, v in trade_details.items() if v}

        # Place order
        self._click_place_order_btn()
        not submit or self.confirm_trade()

    def place_invalid_order(
            self,
            trade_object: DotDict,
            stop_loss: bool = False,
            take_profit: bool = False,
            entry_price: bool = False,
            stop_limit_price: bool = False,
            submit: bool = False
    ) -> None:
        """
        Place an invalid order with specified invalid parameters.
        Args:
            trade_object: Should contain trade_type and order_type
            stop_loss: Whether to make stop loss invalid
            take_profit: Whether to make take profit invalid
            entry_price: Whether to make entry price invalid
            stop_limit_price: Whether to make stop limit price invalid
            submit: Whether to submit trade confirmation modal
        """
        trade_type, order_type = trade_object.trade_type, trade_object.order_type

        self._select_trade_type(trade_type)
        self._select_order_type(order_type)
        self._input_volume()

        # Calculate valid and invalid prices
        live_price = self.get_live_price(trade_type)
        valid_price = calculate_trade_parameters(live_price, trade_type, order_type)
        invalid_price = calculate_trade_parameters(live_price, trade_type, order_type, invalid=True)

        # Determine which prices to use
        price = invalid_price.entry_price if entry_price else valid_price.entry_price
        stp_price = invalid_price.stop_limit_price if stop_limit_price else valid_price.stop_limit_price
        sl = invalid_price.stop_loss if stop_loss else valid_price.stop_loss
        tp = invalid_price.take_profit if take_profit else valid_price.take_profit

        # Input prices
        self._input_price(price, order_type)
        self._input_stop_limit_price(stp_price, order_type)

        not stop_loss or self._input_stop_loss(sl)
        not take_profit or self._input_take_profit(tp)

        self._click_place_order_btn()
        not submit or self.confirm_trade()

    def place_oct_order(self, trade_object: DotDict) -> None:
        """Place a MARKET order with One-Click Trading in OCT TAB."""
        time.sleep(1)
        trade_type = trade_object.trade_type

        volume = self._input_volume()
        units = self._get_volume_info_value()

        # Get live price for One-Click Trading
        live_price = self.get_live_price(trade_type, oct=True)

        logger.debug(f"- Click {trade_type.upper()} button")
        self.actions.click(cook_element(self.__btn_oct_trade, trade_type.lower()))

        # Load input data into trade_object
        trade_details = {
            'live_price': live_price,
            'volume': add_commas(volume),
            'units': add_commas(units),
            'stop_loss': '--',
            'take_profit': '--',
        }

        logger.debug(f"- Order Summary: {format_dict_to_string(trade_details)}")
        trade_object |= {k: v for k, v in trade_details.items() if v}

    def place_order_by_control_button(
            self,
            trade_object: DotDict,
            sl_type: SLTPType = SLTPType.PRICE,
            tp_type: SLTPType = SLTPType.PRICE,
            submit: bool = False,
            input_value: bool = False,
    ) -> None:
        """
        Place an order using control buttons for value adjustment.
        Args:
            trade_object: Should contain trade_type and order_type
            sl_type: Type of stop loss (PRICE/POINTS)
            tp_type: Type of take profit (PRICE/POINTS)
            submit: Whether to submit trade confirmation modal
            input_value: Whether to input initial values before using control buttons
        """
        self._select_trade_type(trade_object.trade_type)
        self._select_order_type(trade_object.order_type)

        # Calculate price parameters
        live_price = self.get_live_price(trade_object.trade_type)
        params = calculate_trade_parameters(live_price, trade_object.trade_type, trade_object.order_type)

        if input_value:
            logger.debug("- Input value before using control buttons")
            self._input_volume(random.randint(1, 10))
            self._input_stop_limit_price(params.stop_limit_price, trade_object.order_type)
            self._input_price(params.entry_price, trade_object.order_type)
            self._input_stop_loss(params.stop_loss)
            self._input_take_profit(params.take_profit)

        logger.debug("- Adjust price using increase and decrease button")
        self.control_volume()
        self.control_price(order_type=trade_object.order_type)
        self.control_stop_limit(order_type=trade_object.order_type)
        self.control_sl(sl_type=sl_type)
        self.control_tp(tp_type=tp_type)

        fill_policy = self._select_fill_policy(FillPolicy.sample_values(trade_object.order_type))
        expiry = self._select_expiry(Expiry.sample_values(trade_object.order_type))

        # Get final values after adjustment
        volume = self.actions.get_text(self.__txt_volume)
        entry_price = live_price if trade_object.order_type == OrderType.MARKET else self.actions.get_text(self.__txt_price)

        trade_details = {
            'live_price': live_price,
            'volume': add_commas(volume),
            'units': add_commas(self._get_volume_info_value()),
            'entry_price': entry_price,
            'stop_loss': self._get_input_sl(),
            'take_profit': self._get_input_tp(),
            'fill_policy': fill_policy,
            'expiry': expiry
        }

        trade_object |= trade_details

        self._click_place_order_btn()
        not submit or self.confirm_trade()

    # ------------------------ VERIFY ------------------------ #
