import random
import time
from typing import Any

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import QUICK_WAIT, SHORT_WAIT
from src.data.enums.trading import OrderType, SLTPType, TradeType, FillPolicy, Expiry
from src.data.objects.trade_obj import ObjTrade
from src.page_object.android.components.trade.base_trade import BaseTrade
from src.utils.common_utils import cook_element
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
    __toggle_oct = (AppiumBy.ID, 'toggle-oct')
    __toggle_oct_checked = (AppiumBy.ID, 'toggle-oct-checked')
    __label_oct = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches("toggle-oct.*")')
    __btn_oct_trade = (AppiumBy.ID, 'trade-button-oct-order-{}')
    __btn_pre_trade_details = (AppiumBy.ID, 'trade-button-pre-trade-details')

    # UI control buttons for adjusting values
    __swap_units = (AppiumBy.ID, 'trade-swap-to-units')
    __swap_volume = (AppiumBy.ID, 'trade-swap-to-volume')

    # Input field elements
    __txt_volume = (AppiumBy.ID, 'trade-input-volume')
    __txt_price = (AppiumBy.ID, 'trade-input-price')
    __txt_stop_loss = (AppiumBy.ID, 'trade-input-stoploss-{}')
    __txt_take_profit = (AppiumBy.ID, 'trade-input-takeprofit-{}')
    __txt_stop_limit_price = (AppiumBy.ID, 'trade-input-stop-limit-price')
    __volume_info_value = (
        AppiumBy.XPATH,
        "//*[@text='Units' or @text='Volume' or @text='Size']/following-sibling::android.widget.TextView[1]"
    )

    # Order placement elements
    __btn_trade = (AppiumBy.ID, 'trade-button-order-{}')
    __drp_order_type = (AppiumBy.ID, 'trade-dropdown-order-type')
    __opt_order_type = (AppiumBy.ID, 'trade-dropdown-order-type-{}')
    __btn_place_order = (AppiumBy.ID, 'trade-button-order')
    __drp_expiry = (AppiumBy.ID, 'trade-dropdown-expiry')
    __opt_expiry = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("{}")')
    __expiry_date = (AppiumBy.ID, 'trade-input-expiry-date')
    __wheel_expiry_date = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.SeekBar").descriptionContains("Select Date")')

    # MT5 specific elements
    __drp_fill_policy = (AppiumBy.ID, 'trade-dropdown-fill-policy')
    __opt_fill_policy = (AppiumBy.ID, 'trade-dropdown-fill-policy-{}')

    # ------------------------ HELPER METHODS ------------------------ #
    def _get_volume_info_value(self) -> str:
        """Get current volume/units value from UI."""
        value = self.actions.get_text(self.__volume_info_value)
        logger.debug(f"- Units is: {value!r}")
        return value

    def _get_input_sl(self) -> str:
        """Get current stop loss value from input field."""
        locator = cook_element(self.__txt_stop_loss, SLTPType.PRICE.lower())
        value = self.actions.get_text(locator)
        logger.debug(f"- Input SL as Price: {value!r}")
        return value

    def _get_input_tp(self) -> str:
        """Get current take profit value from input field."""
        locator = cook_element(self.__txt_take_profit, SLTPType.PRICE.lower())
        value = self.actions.get_text(locator)
        logger.debug(f"- Input TP as Price: {value!r}")
        return value

    # ------------------------ ACTIONS ------------------------ #
    def is_oct_enable(self):
        """Check if OCT mode is enabled in admin config."""
        is_enable = self.actions.is_element_displayed(self.__label_oct, timeout=1)
        logger.debug(f"- OCT enabled in Admin config: {is_enable!r}")
        return is_enable

    def toggle_oct(self, enable: bool = True, confirm=True) -> None:
        """Enable/disable One-Click Trading."""

        # Check current OCT state
        is_enabled = self.actions.is_element_displayed(self.__toggle_oct_checked, timeout=1)
        if is_enabled != enable:
            self.actions.click(self.__toggle_oct if enable else self.__toggle_oct_checked)

            if enable:
                self.confirm_oct(confirm=confirm)

    def open_pre_trade_details(self):
        logger.debug("- Open pre-trade details")
        self.actions.click(self.__btn_pre_trade_details)

    def _swap_to_units(self) -> None:
        """Swap to units display."""
        logger.debug("- Swap to Units")
        if self.actions.is_element_displayed(self.__swap_units, timeout=QUICK_WAIT):
            self.actions.click(self.__swap_units)

    def _swap_to_volume(self) -> None:
        """Swap to volume display."""
        logger.debug("- Swap to Volume")
        if self.actions.is_element_displayed(self.__swap_volume, timeout=QUICK_WAIT):
            self.actions.click(self.__swap_volume)

    def _select_trade_type(self, trade_type: TradeType, normal_mode=True) -> None:
        """Select button trade type in both case: normal_mode and OCT mode (normal mode = False)"""
        logger.debug(f"- Select trade type: {trade_type.value.title()!r}")
        self.actions.click(cook_element(self.__btn_trade if normal_mode else self.__btn_oct_trade, trade_type.lower()))

    def _select_order_type(self, order_type: OrderType) -> None:
        """Select order type (MARKET/LIMIT/STOP/STOP_LIMIT)."""
        # Check current selected order_type
        cur_order_type = self.actions.get_content_desc(self.__drp_order_type).split(", ")[0]
        is_select = order_type.lower() == cur_order_type.lower()

        if is_select:
            logger.debug(f"- Order Type: {order_type.value.title()!r} selected")
            return

        logger.debug(f"- Selecting order type: {order_type.value.title()!r}")
        self.actions.click(self.__drp_order_type)
        self.actions.click(cook_element(self.__opt_order_type, locator_format(order_type)))

    def _select_fill_policy(self, fill_policy: FillPolicy):
        # check current fill policy
        is_select = fill_policy.lower() == self.actions.get_content_desc(self.__drp_fill_policy).split(", ")[0].lower()
        if is_select:
            logger.debug(f"- Fill Policy: {fill_policy.title()!r} selected")
            return

        logger.debug(f"- Selecting fill policy: {fill_policy.title()!r}")
        self.actions.click(self.__drp_fill_policy)
        self.actions.click(cook_element(self.__opt_fill_policy, locator_format(fill_policy)))

    def _select_expiry(self, expiry: Expiry, retries=3):
        # check current selected expiry
        if retries <= 0:
            logger.warning(f"- Failed to select expiry: {expiry.value.title()!r} after retries")
            return

        cur_expiry = self.actions.get_content_desc(self.__drp_expiry).split(", ")[0]
        is_select = cur_expiry.lower() == expiry.lower()

        if is_select:
            logger.debug(f"- Expiry: {expiry.value.title()!r} selected")
            return

        logger.debug(f"- Selecting expiry: {expiry.value.title()!r}")
        self.actions.click(self.__drp_expiry)
        if not self.actions.is_element_displayed(cook_element(self.__opt_expiry, expiry.lower()), timeout=SHORT_WAIT):
            logger.debug("- Retry clicking on expiry dropdown")
            time.sleep(0.5)
            self.actions.click(self.__drp_expiry)

        self.actions.click(cook_element(self.__opt_expiry, expiry.lower()))

        # select date in case expiry specified date
        expiry not in [Expiry.SPECIFIED_DATE, Expiry.SPECIFIED_DATE_TIME] or self._select_expiry_date()

        return self._select_expiry(expiry, retries - 1)

    def _select_expiry_date(self):
        """Select expiry date for specified date expiry."""
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

    def _input_stop_loss(self, value: Any, sl_type) -> None:
        """Input stop loss value."""
        logger.debug(f"- Input SL - {sl_type.value}: {value!r}")
        self.actions.send_keys(cook_element(self.__txt_stop_loss, sl_type), value, hide_keyboard=False)
        self.actions.press_done()

    def _input_take_profit(self, value: Any, tp_type) -> None:
        """Input take profit value."""
        logger.debug(f"- Input TP - {tp_type.value}: {value!r}")
        self.actions.send_keys(cook_element(self.__txt_take_profit, tp_type), value, hide_keyboard=False)
        self.actions.press_done()

    def _input_volume(self, value=None) -> int:
        """Input volume value."""
        volume = value if value is not None else random.randint(2, 10)
        logger.debug(f"- Input volume: {volume!r}")
        self.actions.send_keys(self.__txt_volume, volume, hide_keyboard=False)
        self.actions.press_done()
        return volume

    def _input_price(self, value: Any) -> None:
        """Input trade price."""
        logger.debug(f"- Input Price: {value!r}")
        self.actions.send_keys(self.__txt_price, value, hide_keyboard=True)

    def _input_stop_limit_price(self, value: Any) -> None:
        """Input stop limit price."""
        logger.debug(f"- Input Stop Limit Price: {value!r}")
        self.actions.send_keys(self.__txt_stop_limit_price, value, hide_keyboard=True)

    def place_order(
            self,
            trade_object: ObjTrade,
            sl_type: SLTPType = SLTPType.PRICE,
            tp_type: SLTPType = SLTPType.PRICE,
            confirm: bool = False,
    ) -> None:
        """
        Place a valid order and load input data into trade_object.
        Args:
            trade_object: Should contain trade_type and order_type
            sl_type: Type of stop loss (PRICE/POINTS)
            tp_type: Type of take profit (PRICE/POINTS)
            confirm: Whether to confirm trade confirmation modal
        """
        # Select buy or sell
        self._select_trade_type(trade_object.trade_type)

        # Select order type: market/limit/stop/stop limit
        self._select_order_type(trade_object.order_type)

        # Select swap to units if possible, default is volume
        self._swap_to_units() if trade_object.get('is_units') else self._swap_to_volume()

        # Select fill policy
        if trade_object.fill_policy:
            self._select_fill_policy(trade_object.fill_policy)

        # Set volume property for object
        trade_object.volume = trade_object.get("volume") or random.randint(1, 5)
        self._input_volume(trade_object.volume)
        trade_object.units = self._get_volume_info_value()

        # Calculate price
        prices = calculate_trading_params(
            self.get_live_price(trade_object.trade_type), trade_object.trade_type,
            trade_object.order_type, sl_type=sl_type, tp_type=tp_type
        )

        # input price if present
        if trade_object.order_type != OrderType.MARKET:
            self._input_price(prices.entry_price)

        # input stop limit price if present
        if trade_object.order_type == OrderType.STOP_LIMIT:
            self._input_stop_limit_price(prices.stop_limit_price)
            self.actions.scroll_down(start_x_percent=0.4)

        # Input stop loss
        if prices.stop_loss:
            self._input_stop_loss(prices.stop_loss, sl_type)
            trade_object.stop_loss = self._get_input_sl() if sl_type == SLTPType.POINTS else prices.stop_loss

        # Input take profit
        if prices.take_profit:
            self._input_take_profit(prices.take_profit, tp_type)
            trade_object.take_profit = self._get_input_tp() if tp_type == SLTPType.POINTS else prices.take_profit

        # Select expiry
        if trade_object.expiry:
            self.actions.scroll_down(0.4)
            self._select_expiry(trade_object.expiry)

        trade_details = {
            'volume': format_str_price(trade_object.volume),
            'units': format_str_price(trade_object.units),
            'entry_price': self.get_live_price(trade_object.trade_type) if trade_object.order_type == OrderType.MARKET else prices.entry_price,
            'stop_limit_price': prices.stop_limit_price,
            'stop_loss': '--' if sl_type is None else trade_object.stop_loss,
            'take_profit': '--' if tp_type is None else trade_object.take_profit,
            'sl_type': sl_type,
            'tp_type': tp_type
        }

        logger.debug(f"- Order Summary: {format_dict_to_string(trade_details)}")
        trade_object |= {k: v for k, v in trade_details.items()}

        # click place order button
        self.actions.click(self.__btn_place_order)

        if confirm:
            self.confirm_trade()

    def place_oct_order(self, trade_object: ObjTrade) -> None:
        """
        Place a valid order and load input data into trade_object.
        Args:
            trade_object: contain ObjTrade
        """

        trade_type = trade_object.trade_type

        # Input volume and get units
        volume = self._input_volume()
        units = volume * ObjTrade.CONTRACT_SIZE

        # Prepare trade details
        trade_details = {
            'volume': format_str_price(volume),
            'units': format_str_price(units),
            'entry_price': self.get_live_price(trade_type, oct_mode=True),
            'stop_loss': '--',
            'take_profit': '--'
        }

        logger.debug(f"- Order Summary: {format_dict_to_string(trade_details)}")
        trade_object |= {k: v for k, v in trade_details.items()}

        # Place Order
        self._select_trade_type(trade_type, normal_mode=False)

    # ------------------------ VERIFY ------------------------ #

    def verify_oct_mode(self, enable=True):
        logger.debug(f"- Check OCT button is {'enabled' if enable else 'disabled'}")
        self.actions.verify_element_displayed(self.__toggle_oct_checked if enable else self.__toggle_oct)

        logger.debug(f"- Check pre-trade details tab is {'displayed' if enable else 'not displayed'}")
        self.actions.verify_element_displayed(self.__btn_pre_trade_details, is_display=enable)
