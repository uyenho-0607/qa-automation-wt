import random
import time
from typing import Optional, Any

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.enums.trading import OrderType, SLTPType, TradeType, FillPolicy, Expiry
from src.data.objects.symbol_obj import ObjSymbol
from src.data.objects.trade_obj import ObjTrade
from src.page_object.android.components.trade.base_trade import BaseTrade
from src.utils.common_utils import cook_element, resource_id
from src.utils.format_utils import locator_format, format_str_price, format_dict_to_string
from src.utils.logging_utils import logger
from src.utils.trading_utils import calculate_trading_params


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

    # ------------------------ ACTIONS ------------------------ #
    def toggle_oct(self, enable: bool = True, submit: bool = False) -> None:
        """Enable/disable One-Click Trading."""

        # Check current OCT state
        is_enabled = self.actions.is_element_displayed(self.__toggle_oct_checked, timeout=1)
        if is_enabled != enable:
            self.actions.click(self.__toggle_oct if enable else self.__toggle_oct_checked)

        if enable:
            self.confirm_oct(confirm=submit)

    def open_pre_trade_details(self):
        self.actions.click(self.__btn_pre_trade_details)

    def swap_to_units(self) -> None:
        """Swap to units display."""
        if self.actions.is_element_displayed(self.__swap_units, timeout=1):
            self.actions.click(self.__swap_units)

    def swap_to_volume(self) -> None:
        """Swap to volume display."""
        if self.actions.is_element_displayed(self.__swap_volume, timeout=1):
            self.actions.click(self.__swap_volume)

    def _select_trade_type(self, trade_type: TradeType) -> None:
        """Select trade type (BUY/SELL
        )."""
        logger.debug(f"- Select trade type: {trade_type.upper()!r}")
        self.actions.click(cook_element(self.__btn_trade, trade_type.lower()))

    def _select_oct_trade_type(self, trade_type: TradeType) -> None:
        """Select trade type (BUY/SELL
        )."""
        logger.debug(f"- Select trade type: {trade_type.upper()!r}")
        self.actions.click(cook_element(self.__btn_oct_trade, trade_type.lower()))

    def _select_order_type(self, order_type: OrderType) -> None:
        """Select order type (MARKET/LIMIT/STOP/STOP_LIMIT)."""
        is_selected = order_type.lower() in self.actions.get_content_desc(self.__drp_order_type).lower()
        if is_selected:
            logger.debug(f"- Order type: {order_type} already selected")
            return

        logger.debug(f"- Select order type: {order_type.capitalize()!r}")
        self.actions.click(self.__drp_order_type)
        self.actions.click(cook_element(self.__opt_order_type, locator_format(order_type)))

    def _select_fill_policy(self, fill_policy: FillPolicy | str):
        """Select the fill policy for the order. Return selected fill_policy"""
        # check current selected fill policy
        is_selected = fill_policy.lower() in self.actions.get_content_desc(self.__drp_fill_policy).lower()
        if is_selected:
            logger.debug(f"- Fill Policy: {fill_policy!r} already selected")
            return

        logger.debug(f"- Select fill policy: {fill_policy.capitalize()!r}")
        self.actions.click(self.__drp_fill_policy)
        self.actions.click(cook_element(self.__opt_fill_policy, locator_format(fill_policy)))

    def _select_expiry(self, expiry: Expiry | str):
        """Select expiry for the order. Return selected expiry"""
        is_selected = expiry.lower() in self.actions.get_content_desc(self.__drp_expiry).lower()
        if is_selected:
            logger.debug(f"- Expiry: {expiry!r} already selected")
            return

        logger.debug(f"- Select expiry: {expiry.capitalize()!r}")
        self.actions.click(self.__drp_expiry)
        self.actions.click(cook_element(self.__opt_expiry, expiry.lower()))

        if expiry in [Expiry.SPECIFIED_DATE, Expiry.SPECIFIED_DATE_TIME]:
            logger.debug(f"- Select expiry date")
            time.sleep(0.5)
            self.actions.scroll_down(start_x_percent=0.4)
            self.actions.click(self.__expiry_date)
            self.actions.swipe_picker_wheel_down(self.__wheel_expiry_date)
            self.click_confirm_btn()

    def _click_place_order_btn(self) -> None:
        """Click place order button."""
        logger.debug(f"- Click place order button")
        self.actions.click(self.__btn_place_order)

    def _input_sl(self, value: Any, sl_type) -> None:
        """Input stop loss value."""
        self.actions.click(cook_element(self.__txt_stop_loss, sl_type.lower()))
        logger.debug(f"- Input stop loss: {value!r}")
        self.actions.send_keys(cook_element(self.__txt_stop_loss, sl_type), value, hide_keyboard=True)

    def _input_tp(self, value: Any, tp_type) -> None:
        """Input take profit value."""
        self.actions.click(cook_element(self.__txt_take_profit, tp_type.lower()))
        logger.debug(f"- Input take profit: {value!r}")
        self.actions.send_keys(cook_element(self.__txt_take_profit, tp_type), value, hide_keyboard=True)

    def _input_volume(self, value: Optional[int] = None) -> int:
        """Input volume value."""
        volume = value if value is not None else random.randint(2, 10)
        logger.debug(f"- Input volume: {volume!r}")
        self.actions.send_keys(self.__txt_volume, volume, hide_keyboard=True)
        return volume

    def _input_price(self, value: Any, order_type: Optional[OrderType] = None) -> None:
        """Input trade price for order type: Limit, Stop, Stop Limit."""
        if order_type == OrderType.MARKET:
            return
        logger.debug(f"- Input price: {value!r}")
        self.actions.send_keys(self.__txt_price, value, hide_keyboard=True)

    def _input_stop_price(self, value: Any, order_type: Optional[OrderType] = None) -> None:
        """Input stop limit price for order type 'Stop limit'."""
        if order_type != OrderType.STOP_LIMIT:
            return
        logger.debug(f"- Input stop limit price: {value!r}")
        self.actions.send_keys(self.__txt_stop_limit_price, value, hide_keyboard=True)

    def place_oct_order(self, trade_object: ObjTrade) -> None:
        """
        Place a valid order and load input data into trade_object.
        Args:
            trade_object: contain ObjTrade
        """

        symbol_details = ObjSymbol().get_symbol_details(trade_object.symbol)
        contract_size = symbol_details["contract_size"]

        trade_type = trade_object.trade_type

        # Input volume and get units
        volume = self._input_volume()
        units = volume * contract_size

        # Prepare trade details
        trade_details = {
            'volume': format_str_price(volume),
            'units': format_str_price(units),
            'entry_price': self.get_live_price(trade_type, oct=True),
            'stop_loss': '--',
            'take_profit': '--'
        }

        logger.debug(f"- Order Summary: {format_dict_to_string(trade_details)}")
        trade_object |= {k: v for k, v in trade_details.items()}

        # Place Order
        self._select_oct_trade_type(trade_type)

    def place_order(
            self,
            trade_object: ObjTrade,
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
        units = self._get_volume_info_value()

        # Calculate trade parameters
        prices = calculate_trading_params(self.get_live_price(trade_type), trade_type, order_type, sl_type=sl_type, tp_type=tp_type)

        # Input prices
        self._input_price(prices.entry_price, order_type)
        self._input_stop_price(prices.stop_limit_price, order_type)

        # Select fill_policy
        not trade_object.get("fill_policy") or self._select_fill_policy(trade_object.fill_policy)

        # scroll down a bit
        time.sleep(0.5)
        self.actions.scroll_down(start_x_percent=0.3)

        # Input SL/TP
        if sl_type is not None:
            stop_loss = prices.stop_loss
            self._input_sl(stop_loss, sl_type)
            # get SL price
            if sl_type == SLTPType.POINTS:
                stop_loss = self._get_input_sl()

        if tp_type is not None:
            take_profit = prices.take_profit
            self._input_tp(take_profit, tp_type)
            # get TP price
            if tp_type == SLTPType.POINTS:
                take_profit = self._get_input_tp()

        # select expiry
        not trade_object.get("expiry") or self._select_expiry(trade_object.expiry)

        # Prepare trade details
        volume, units = (volume, units) if not swap_to_units else (units, volume)
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
        not submit or self.confirm_trade()

    # ------------------------ VERIFY ------------------------ #

    def verify_oct_mode(self, enable=True):
        logger.info(f"Verifying OCT mode is {'enabled' if enable else 'disabled'}")
        self.actions.verify_element_displayed(self.__btn_pre_trade_details, is_display=enable)
