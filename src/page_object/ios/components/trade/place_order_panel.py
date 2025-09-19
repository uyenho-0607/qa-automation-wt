import random

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import QUICK_WAIT
from src.data.enums import SLTPType, TradeType, OrderType, Expiry
from src.data.objects.trade_obj import ObjTrade
from src.page_object.ios.components.trade.base_trade import BaseTrade
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
    __toggle_oct = (AppiumBy.ACCESSIBILITY_ID, 'toggle-oct')
    __toggle_oct_checked = (AppiumBy.ACCESSIBILITY_ID, 'toggle-oct-checked')
    __btn_pre_trade_details = (AppiumBy.ACCESSIBILITY_ID, "trade-button-pre-trade-details")

    __btn_trade_type = (AppiumBy.ACCESSIBILITY_ID, "trade-button-order-{}")  # buy / sell
    __drp_order_type = (AppiumBy.ACCESSIBILITY_ID, "trade-dropdown-order-type")
    __opt_order_type = (AppiumBy.ACCESSIBILITY_ID, "trade-dropdown-order-type-{}")  # market/ limit/ stop/ stop-limit
    __drp_fill_policy = (AppiumBy.ACCESSIBILITY_ID, "trade-dropdown-fill-policy")
    __opt_fill_policy = (AppiumBy.ACCESSIBILITY_ID, "trade-dropdown-fill-policy-{}")
    __drp_expiry = (AppiumBy.ACCESSIBILITY_ID, "trade-dropdown-expiry")
    __opt_expiry = (AppiumBy.ACCESSIBILITY_ID, "trade-dropdown-expiry-{}")
    __expiry_date = (AppiumBy.ACCESSIBILITY_ID, "trade-input-expiry-date")

    __txt_volume = (AppiumBy.ACCESSIBILITY_ID, "trade-input-volume")
    __lbl_units_volume = (AppiumBy.IOS_CLASS_CHAIN,
                          "**/XCUIElementTypeOther[`name BEGINSWITH 'Units'`]")  # value of units/ volume (NOT the input value)
    __txt_price = (AppiumBy.ACCESSIBILITY_ID, "trade-input-price")  # price
    __txt_stop_limit_price = (AppiumBy.ACCESSIBILITY_ID, "trade-input-stop-limit-price")  # stop limit price
    __txt_stop_loss = (AppiumBy.ACCESSIBILITY_ID, "trade-input-stoploss-{}")  # price | points
    __txt_take_profit = (AppiumBy.ACCESSIBILITY_ID, "trade-input-takeprofit-{}")  # price | points
    __btn_place_order = (AppiumBy.ACCESSIBILITY_ID, "trade-button-order")
    __btn_cancel_order = (AppiumBy.ACCESSIBILITY_ID, "trade-button-cancel")
    __opt_trade_swap_dyn = (AppiumBy.ACCESSIBILITY_ID, "trade-swap-to-{}")  # volume | units

    # ------------------------ HELPER METHODS ------------------------ #
    def _get_input_sl(self):
        locator = cook_element(self.__txt_stop_loss, SLTPType.PRICE.lower())
        value = self.actions.get_attribute(locator, "value")
        logger.debug(f"- Input SL as Price: {value!r}")
        return value

    def _get_input_tp(self):
        locator = cook_element(self.__txt_take_profit, SLTPType.PRICE.lower())
        value = self.actions.get_attribute(locator, "value")
        logger.debug(f"- Input TP as Price: {value!r}")
        return value

    def _get_vol_info_value(self):
        value = self.actions.get_attribute(self.__lbl_units_volume, "label").split(" ")[-1]
        logger.debug(f"- Units is: {value!r}")
        return value

    # ------------------------ ACTIONS ------------------------ #
    def toggle_oct(self, enable=True, submit=True):
        # Check current OCT state
        is_enabled = self.actions.is_element_displayed(self.__toggle_oct_checked, timeout=QUICK_WAIT)
        if is_enabled != enable:
            self.actions.click(self.__toggle_oct if enable else self.__toggle_oct_checked)

            if enable:
                self.confirm_oct(submit)

    def open_pre_trade_details(self):
        logger.debug("- Open pre-trade details")
        self.actions.click(self.__btn_pre_trade_details)

    def _select_trade_type(self, trade_type: TradeType):
        logger.debug(f"- Select trade type: {trade_type.value.title()!r}")
        self.actions.click(cook_element(self.__btn_trade_type, trade_type.lower()))

    def _select_order_type(self, order_type: OrderType, retries=3):
        if retries <= 0:
            logger.warning(f"- Failed to select order type: {order_type.value.title()} after retries")
            return

        # check current selected order_type
        if retries <= 0:
            logger.warning(f"- Failed to select order type: {order_type.value.title()} after retries")
            return

        cur_order_type = self.actions.get_attribute(self.__drp_order_type, "label")
        cur_order_type = " ".join(cur_order_type.split(" ")[:-1])  # handle unexpected icon
        is_select = order_type.lower() == cur_order_type.lower()

        if is_select:
            logger.debug(f"- Order Type: {order_type.value.title()!r} selected")
            return

        logger.info(f"- Selecting order type: {order_type.value.title()!r}")
        self.actions.click(self.__drp_order_type)
        self.actions.click(cook_element(self.__opt_order_type, locator_format(order_type)))

        return self._select_order_type(order_type, retries - 1)

    def _select_fill_policy(self, fill_policy, retries=3):
        # check current fill policy
        if retries <= 0:
            logger.warning(f"- Failed to select fill policy: {fill_policy!r} after retries")
            return

        cur_fp = self.actions.get_attribute(self.__drp_fill_policy, "label")
        cur_fp = " ".join(cur_fp.split(" ")[:-1])
        is_select = fill_policy.lower() == cur_fp.lower()

        if is_select:
            logger.debug(f"- Fill Policy: {fill_policy!r} selected")
            return

        logger.info(f"- Selecting fill policy: {fill_policy!r}")
        self.actions.click(self.__drp_fill_policy)
        self.actions.click(cook_element(self.__opt_fill_policy, locator_format(fill_policy)))
        return self._select_fill_policy(fill_policy, retries - 1)

    def _select_expiry(self, expiry: Expiry, retries=3):
        # check current selected expiry
        if retries <= 0:
            logger.warning(f"- Failed to select expiry: {expiry.value.title()!r} after retries")
            return

        cur_expiry = self.actions.get_attribute(self.__drp_expiry, "label")
        cur_expiry = " ".join(cur_expiry.split(" ")[:-1])
        is_select = cur_expiry.lower() == expiry.lower()

        if is_select:
            logger.debug(f"- Expiry: {expiry.value.title()!r} selected")
            return

        logger.info(f"- Selecting expiry: {expiry.value.title()!r}")
        self.actions.click(self.__drp_expiry)

        locator = locator_format(expiry) if expiry != Expiry.SPECIFIED_DATE else "_".join(item.lower() for item in expiry.split(" "))
        self.actions.click(cook_element(self.__opt_expiry, locator))

        # todo: update handle select specified date when having locators
        # if expiry in [Expiry.SPECIFIED_DATE, Expiry.SPECIFIED_DATE_TIME]:
        #     self.actions.scroll_down(start_x_percent=0.4)
        #     self.actions.click(self.__expiry_date)

        return self._select_expiry(expiry, retries - 1)

    def _click_place_order_btn(self):
        logger.debug("- Click place order button")
        self.actions.click(self.__btn_place_order)

    def _click_cancel_order_btn(self):
        logger.debug("- Click cancel order button")
        self.actions.click(self.__btn_cancel_order)

    def _input_stop_loss(self, value, sl_type: SLTPType):
        locator = cook_element(self.__txt_stop_loss, sl_type.lower())
        logger.debug(f"- Input SL - {sl_type.value}: {value!r}")
        self.actions.send_keys(locator, value)

    def _input_take_profit(self, value, tp_type: SLTPType):
        locator = cook_element(self.__txt_take_profit, tp_type.lower())
        logger.debug(f"- Input TP - {tp_type.value}: {value!r}")
        self.actions.send_keys(locator, value)

    def _input_volume(self, value):
        logger.debug(f"- Input Volume: {value!r}")
        self.actions.send_keys(self.__txt_volume, value)

    def _input_price(self, value):
        logger.debug(f"- Input Price: {value!r}")
        self.actions.send_keys(self.__txt_price, value)

    def _input_stop_limit_price(self, value):
        logger.debug(f"- Input Stop Limit Price: {value!r}")
        self.actions.send_keys(self.__txt_stop_limit_price, value)

    def _swap_to_units(self):
        logger.debug("Swap to Units")
        self.actions.click_if_displayed(cook_element(self.__opt_trade_swap_dyn, "units"))

    def _swap_to_volume(self):
        logger.debug("Swap to Volume")
        self.actions.click_if_displayed(cook_element(self.__opt_trade_swap_dyn, "volume"))

    def place_order(
            self, trade_object: ObjTrade,
            sl_type: SLTPType = SLTPType.PRICE,
            tp_type: SLTPType = SLTPType.PRICE,
            confirm=True
    ):
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
        trade_object.units = self._get_vol_info_value()

        # Calculate price
        prices = calculate_trading_params(
            self.get_live_price(trade_object.trade_type), trade_object.trade_type,
            trade_object.order_type, sl_type=sl_type, tp_type=tp_type
        )

        # Select order type
        self._select_order_type(trade_object.order_type)

        # input stop limit price if present
        if trade_object.order_type == OrderType.STOP_LIMIT:
            self._input_stop_limit_price(prices.stop_limit_price)

        # input price if present
        if trade_object.order_type != OrderType.MARKET:
            self._input_price(prices.entry_price)

        # Input stop loss
        if prices.stop_loss:
            self._input_stop_loss(prices.stop_loss, sl_type)
            trade_object.stop_loss = self._get_input_sl() if sl_type == SLTPType.POINTS else prices.stop_loss

        # Scroll to bottom
        self.actions.scroll_down(0.4)

        # Input take profit
        if prices.take_profit:
            self._input_take_profit(prices.take_profit, tp_type)
            trade_object.take_profit = self._get_input_tp() if tp_type == SLTPType.POINTS else prices.take_profit

        # Select expiry
        if trade_object.expiry:
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

    def place_oct_order(self):
        ...

    # ------------------------ VERIFY ------------------------ #

    def verify_oct_mode(self, enable=True):
        ...
