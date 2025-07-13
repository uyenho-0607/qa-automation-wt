import random
import time
from typing import Literal

from selenium.webdriver.common.by import By

from src.data.objects.trade_object import ObjectTrade
from src.core.actions.web_actions import WebActions
from src.data.enums import OrderType, FillPolicy, SLTPType, Expiry, TradeTab, TradeType
from src.data.project_info import ProjectConfig
from src.page_object.web.components.trade.base_trade import BaseTrade
from src.utils import DotDict
from src.utils.common_utils import data_testid, cook_element
from src.utils.format_utils import locator_format, format_dict_to_string, format_str_price
from src.utils.logging_utils import logger
from src.utils.trading_utils import calculate_trade_parameters

class PlaceOrderPanel(BaseTrade):
    """Panel for placing orders in the trading interface.
    This class provides functionality for:
    - Placing orders
    """

    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    # One-Click Trading elements
    __toggle_oct = (By.CSS_SELECTOR, data_testid('toggle-oct'))
    __toggle_oct_checked = (By.CSS_SELECTOR, data_testid('toggle-oct-checked'))
    __trade_tab = (By.CSS_SELECTOR, data_testid('tab-{}'))
    __btn_oct_trade = (By.CSS_SELECTOR, data_testid('trade-button-oct-order-{}'))

    __tab_oct = (By.CSS_SELECTOR, data_testid('tab-one-click-trading'))
    __tab_trade = (By.CSS_SELECTOR, data_testid('tab-trade'))
    __tab_specification = (By.CSS_SELECTOR, data_testid('tab-specification'))

    # UI control buttons for adjusting values
    __inc_dec_volume = (By.CSS_SELECTOR, data_testid('trade-input-volume-{}'))  # increase / decrease
    __inc_dec_sl = (By.CSS_SELECTOR, data_testid('trade-input-stoploss-{}-{}'))  # point/ price
    __inc_dec_tp = (By.CSS_SELECTOR, data_testid('trade-input-takeprofit-{}-{}'))
    __inc_dec_price = (By.CSS_SELECTOR, data_testid('trade-input-price-{}'))  # increase / decrease
    __inc_dec_stop_limit = (By.CSS_SELECTOR, data_testid('trade-input-stop-limit-price-{}'))  # increase / decrease
    __swap_units = (By.CSS_SELECTOR, data_testid('trade-swap-to-units'))
    __swap_volume = (By.CSS_SELECTOR, data_testid('trade-swap-to-volume'))

    # Input field elements
    __txt_volume = (By.CSS_SELECTOR, data_testid('trade-input-volume'))
    __txt_price = (By.CSS_SELECTOR, data_testid('trade-input-price'))
    __txt_stop_loss = (By.CSS_SELECTOR, data_testid('trade-input-stoploss-{}', 'input'))
    __txt_take_profit = (By.CSS_SELECTOR, data_testid('trade-input-takeprofit-{}', 'input'))
    __txt_stop_limit_price = (By.CSS_SELECTOR, data_testid('trade-input-stop-limit-price'))

    __min_volume_info_value = (By.CSS_SELECTOR, data_testid('trade-volume-info-min-value'))
    __volume_info_value = (By.CSS_SELECTOR, data_testid('trade-volume-info-value'))

    # Order placement elements
    __btn_trade = (By.CSS_SELECTOR, data_testid('trade-button-order-{}'))  # buy or sell btn
    __drp_order_type = (By.CSS_SELECTOR, data_testid('trade-dropdown-order-type'))
    __opt_order_type = (By.CSS_SELECTOR, data_testid('trade-dropdown-order-type-{}'))
    __btn_place_order = (By.CSS_SELECTOR, data_testid('trade-button-order'))
    __drp_expiry = (By.CSS_SELECTOR, data_testid('trade-dropdown-expiry'))
    __opt_expiry = (By.CSS_SELECTOR, data_testid('trade-dropdown-expiry-{}'))
    __expiry_trade = (By.CSS_SELECTOR, data_testid('trade-input-expiry-date'))
    __expiry_last_date = (By.XPATH, "(//button[contains(@class, 'month-view')])[last()]")

    # MT5 specific elements
    __drp_fill_policy = (By.CSS_SELECTOR, data_testid('trade-dropdown-fill-policy'))
    __opt_fill_policy = (By.CSS_SELECTOR, data_testid('trade-dropdown-fill-policy-{}'))

    # ------------------------ HELPER METHODS ------------------------ #
    def _get_volume_info_value(self) -> str:
        """Get current volume/units value from UI."""
        return self.actions.get_text(self.__volume_info_value)

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

    def _get_input_price(self):
        return self.actions.get_value(self.__txt_price)

    def _get_input_stop_limit_price(self):
        return self.actions.get_value(self.__txt_stop_limit_price)

    def _input_trade_value(self, locator, value, value_type: str) -> None:
        """Input value into a trade field."""
        logger.debug(f"- Input {value_type}: {value!r}")
        self.actions.send_keys(locator, value)

    # ------------------------ ACTIONS ------------------------ #
    def get_min_volume(self) -> str | None:
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

    def select_tab(self, tab: TradeTab):
        self.actions.click(cook_element(self.__trade_tab, tab))

    # UI Control Buttons
    def _control_inc_dec_btn(
            self,
            button_type: Literal["volume", "sl", "tp", "price", "stop_limit"],
            inc_step: int | None = None,
            dec_step: int | None = None,
            sl_tp_type: SLTPType = SLTPType.PRICE
    ) -> None:
        """Adjust a value using increase/decrease buttons."""
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

    def control_volume(self, inc_step: int | None = None, dec_step: int | None = None) -> None:
        """Adjust volume using control buttons."""
        self._control_inc_dec_btn("volume", inc_step, dec_step)

    def control_sl(self, inc_step: int | None = None, dec_step: int | None = None, sl_type: SLTPType = SLTPType.PRICE) -> None:
        """Adjust stop loss using control buttons."""
        self._control_inc_dec_btn("sl", inc_step, dec_step, sl_type)

    def control_tp(self, inc_step: int | None = None, dec_step: int | None = None, tp_type: SLTPType = SLTPType.PRICE) -> None:
        """Adjust take profit using control buttons."""
        self._control_inc_dec_btn("tp", inc_step, dec_step, tp_type)

    def control_price(self, inc_step: int | None = None, dec_step: int | None = None, order_type: OrderType = OrderType.LIMIT) -> None:
        """Adjust price using control buttons."""
        if not order_type == OrderType.MARKET:
            self._control_inc_dec_btn("price", inc_step, dec_step)

    def control_stop_limit(self, inc_step: int | None = None, dec_step: int | None = None, order_type: OrderType = OrderType.STOP_LIMIT) -> None:
        """Adjust stop limit price using control buttons."""
        if order_type.is_stp_limit():
            self._control_inc_dec_btn("stop_limit", inc_step, dec_step)

    def swap_to_units(self) -> None:
        """Swap to units display."""
        if self.actions.is_element_displayed(self.__swap_units, timeout=1):
            self.actions.click(self.__swap_units)

    def swap_to_volume(self) -> None:
        """Swap to volume display."""
        if self.actions.is_element_displayed(self.__swap_volume):
            self.actions.click(self.__swap_volume)

    def _select_trade_type(self, trade_type: TradeType) -> None:
        """Select trade type (BUY/SELL)."""
        locator = cook_element(self.__btn_trade, trade_type.lower())
        if "selected" in self.actions.get_attribute(locator, "class"):
            logger.debug(f"- Trade Type {trade_type.value!r} already correct")
            return

        logger.debug(f"- Select trade type: {trade_type.upper()!r}")
        self.actions.click(locator)

    def _select_order_type(self, order_type: OrderType) -> None:
        """Select order type (MARKET/LIMIT/STOP/STOP_LIMIT)."""
        locator = cook_element(self.__opt_order_type, locator_format(order_type))
        if "selected" in self.actions.get_attribute(locator, "class"):
            logger.debug(f"- Order Type {order_type.value!r} already selected")
            return

        logger.debug(f"- Select order type: {order_type.capitalize()!r}")
        self.actions.click(self.__drp_order_type)
        time.sleep(1)
        self.actions.click(locator)

    def _select_fill_policy(self, fill_policy: FillPolicy | str) -> str | None:
        """Select fill policy for the order. Return selected fill_policy."""
        if ProjectConfig.is_mt4() or not fill_policy:
            return

        locator = cook_element(self.__opt_fill_policy, locator_format(fill_policy))
        if "selected" in self.actions.get_attribute(locator, "class"):
            logger.debug(f"- Fill Policy: {fill_policy.capitalize()!r} already selected")
            return

        logger.debug(f"- Select Fill Policy: {fill_policy.capitalize()!r}")
        self.actions.click(self.__drp_fill_policy)
        self.actions.click(cook_element(self.__opt_fill_policy, locator_format(fill_policy)))

    def _select_expiry(self, expiry: Expiry | str) -> str | None:
        """Select expiry for the order. Return selected expiry."""
        if expiry:
            logger.debug(f"- Select expiry: {expiry.capitalize()!r}")
            self.actions.click(self.__drp_expiry)
            self.actions.click(cook_element(self.__opt_expiry, locator_format(expiry)))

            if expiry in [Expiry.SPECIFIED_DATE, Expiry.SPECIFIED_DATE_TIME]:
                logger.debug(f"- Select expiry date")
                self.actions.click(self.__expiry_trade)
                self.actions.click(self.__expiry_last_date)

    def _click_place_order_btn(self) -> None:
        """Click place order button."""
        logger.debug(f"- Click place order button")
        self.actions.click(self.__btn_place_order)

    def _input_stop_loss(self, value: any) -> None:
        """Input stop loss value."""
        sl_type = SLTPType.POINTS if isinstance(value, int) else SLTPType.PRICE
        self._input_trade_value(cook_element(self.__txt_stop_loss, sl_type), value, "stop loss")

    def _input_take_profit(self, value: any) -> None:
        """Input take profit value."""
        tp_type = SLTPType.POINTS if isinstance(value, int) else SLTPType.PRICE
        self._input_trade_value(cook_element(self.__txt_take_profit, tp_type), value, "take profit")

    def _input_volume(self, value: int | None = None) -> int:
        """Input volume value."""
        volume = value if value is not None else random.randint(2, 10)
        self._input_trade_value(self.__txt_volume, volume, "volume")
        return volume

    def _input_price(self, value: any, order_type: OrderType | None = None) -> None:
        """Input trade price for order type: Limit, Stop, Stop Limit."""
        if order_type == OrderType.MARKET:
            return
        self._input_trade_value(self.__txt_price, value, "price")

    def _input_stop_limit_price(self, value: any, order_type: OrderType | None = None) -> None:
        """Input stop limit price for order type 'Stop limit'."""
        if not order_type.is_stp_limit():
            return
        self._input_trade_value(self.__txt_stop_limit_price, value, "stop limit price")

    def place_order(
            self,
            trade_object: ObjectTrade,
            sl_type: SLTPType = SLTPType.PRICE,
            tp_type: SLTPType = SLTPType.PRICE,
            swap_to_units: bool = False,
            swap_to_volume: bool = True,
            submit: bool = False,
            is_chart: bool = False
    ) -> None:
        """Place a valid order and load input data into trade_object."""
        trade_type, order_type = trade_object.trade_type, trade_object.order_type
        # select trade tab
        if not is_chart:
            self.select_tab(TradeTab.TRADE)

        # select trade_type and order_type
        self._select_trade_type(trade_type)
        self._select_order_type(order_type)

        not swap_to_units or self.swap_to_units()
        not swap_to_volume or self.swap_to_volume()

        # Handle input volume and units
        volume = self._input_volume()
        units = self._get_volume_info_value()

        # calculate price params
        trade_params = calculate_trade_parameters(
            self.get_live_price(trade_type), trade_type, order_type, sl_type=sl_type, tp_type=tp_type
        )
        stop_loss, take_profit = "--", "--"

        # input price values
        self._input_price(trade_params.entry_price, order_type)
        self._input_stop_limit_price(trade_params.stop_limit_price, order_type)

        if sl_type is not None:
            stop_loss = trade_params.stop_loss
            self._input_stop_loss(stop_loss)

        if tp_type is not None:
            take_profit = trade_params.take_profit
            self._input_take_profit(take_profit)

        # Select fill policy and expiry
        self._select_fill_policy(trade_object.get("fill_policy"))
        self._select_expiry(trade_object.get("expiry"))

        if sl_type == SLTPType.POINTS:
            stop_loss = self._get_input_sl()
            trade_object.sl_type = sl_type # update sl_type for define tolerance fields

        if tp_type == SLTPType.POINTS:
            take_profit = self._get_input_tp()
            trade_object.tp_type = tp_type # update sl_type for define tolerance fields

        # Load input data into trade_object
        volume, units = (units, volume) if swap_to_units else (volume, units)

        trade_details = {
            'live_price': self.get_live_price(trade_type),
            'volume': volume,
            'units': units,
            'entry_price': trade_params.entry_price,
            'stop_limit_price': trade_params.stop_limit_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'fill_policy': trade_object.get("fill_policy"),
            'expiry': trade_object.get("expiry")
        }

        logger.debug(f"- Order Summary: {format_dict_to_string(trade_details)}")
        self._click_place_order_btn()

        if submit:
            self.confirm_trade()

        trade_object |= {k: v for k, v in trade_details.items() if v}

    def place_invalid_order(
            self,
            trade_object: DotDict,
            stop_loss=False,
            take_profit=False,
            entry_price=False,
            stop_limit_price=False,
            is_chart=False,
            submit=False
    ):
        """
        Place invalid order with option
        trade_object: Should contain trade_type (BUY / SELL), order_type (MARKET/ LIMIT/ STOP/ STOP LIMIT)
        stop_loss: set to True >> stop_loss will be invalid
        take_profit: set to True >> take_profit will be invalid
        entry_price: set to True >> entry_price will be invalid
        stop_limit_price: set to True >> stop_limit_price will be invalid
        NOTE: whether stop_loss/ take_profit is invalid or entry_price is invalid
        """
        trade_type, order_type = trade_object.trade_type, trade_object.order_type
        is_chart or self.select_tab(TradeTab.TRADE)

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

    def place_oct_order(
            self,
            trade_object: DotDict,
            # swap_to_units: bool = False,
    ) -> None:
        """Place a MARKET order with One-Click Trading in OCT TAB."""
        trade_type = trade_object.trade_type

        # not swap_to_units or self.swap_to_units()

        volume = self._input_volume()
        units = self._get_volume_info_value()
        # volume, units = (volume, units) if not swap_to_units else (units, volume)

        # Get live price for One-Click Trading
        live_price = self.get_live_price(trade_type, oct=True)

        logger.debug(f"- Click {trade_type.upper()} button")
        self.actions.click(cook_element(self.__btn_oct_trade, trade_type.lower()))

        # Load input data into trade_object
        trade_details = {
            'entry_price': live_price,
            'volume': volume,
            'units': units,
            'stop_loss': '--',
            'take_profit': '--',
        }

        logger.debug(f"- Order Summary: {format_dict_to_string(trade_details)}")
        trade_object |= trade_details

    def place_order_by_control_button(
            self,
            trade_object: DotDict,
            sl_type: SLTPType = SLTPType.PRICE,
            tp_type: SLTPType = SLTPType.PRICE,
            submit: bool = False,
            is_chart: bool = False,
            input_value: bool = False,
    ) -> None:
        """
        Place an order using control buttons for value adjustment.
        Args:
            trade_object: Should contain trade_type and order_type
            sl_type: Type of stop loss (PRICE/POINTS)
            tp_type: Type of take profit (PRICE/POINTS)
            submit: Whether to submit trade confirmation modal
            is_chart: Whether placing order using chart
            input_value: Whether to input initial values before using control buttons
        """
        is_chart or self.select_tab(TradeTab.TRADE)
        trade_type, order_type = trade_object.trade_type, trade_object.order_type

        self._select_trade_type(trade_type)
        self._select_order_type(order_type)

        # Calculate price parameters
        params = calculate_trade_parameters(
            self.get_live_price(trade_type), trade_type, order_type, sl_type=sl_type, tp_type=tp_type
        )

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

        self._select_fill_policy(trade_object.get("fill_policy"))
        self._select_expiry(trade_object.get("expiry"))

        # Get final values after adjustment
        volume = self.actions.get_value(self.__txt_volume)
        entry_price = params.entry_price if order_type == OrderType.MARKET else self._get_input_price()

        trade_details = {
            'volume': volume,
            'units': self._get_volume_info_value(),
            'entry_price': entry_price,
            'stop_loss': self._get_input_sl(),
            'take_profit': self._get_input_tp(),
        }

        if order_type.is_stp_limit():
            trade_details |= {'stop_limit_price': self._get_input_stop_limit_price()}

        trade_object |= trade_details

        self._click_place_order_btn()
        not submit or self.confirm_trade()

# ------------------------ VERIFY ------------------------ #
