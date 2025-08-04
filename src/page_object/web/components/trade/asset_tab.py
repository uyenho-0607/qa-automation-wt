import random
import time
from typing import Optional, List, Literal

from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import EXPLICIT_WAIT, SHORT_WAIT
from src.data.enums import AssetTabs, ColPreference, SortOptions, BulkCloseOpts, SLTPType, Expiry, OrderType
from src.data.objects.trade_obj import ObjTrade
from src.page_object.web.components.modals.trading_modals import TradingModals
from src.page_object.web.components.trade.base_trade import BaseTrade
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import data_testid, cook_element, convert_strtime
from src.utils.format_utils import extract_asset_tab_number, format_dict_to_string, locator_format
from src.utils.logging_utils import logger
from src.utils.trading_utils import calculate_partial_close, get_sl_tp, get_pending_price, get_stop_price


class AssetTab(BaseTrade):
    """
    A class representing the Asset Tab in the trading interface.
    Handles all interactions with the asset tab UI elements and operations.
    """

    def __init__(self, actions: WebActions):
        super().__init__(actions)
        self.__trade_modals = TradingModals(actions)

    # ------------------------ LOCATORS ------------------------ #
    __tab = (By.CSS_SELECTOR, data_testid('tab-asset-order-type-{}'))
    __tab_amount = (By.XPATH, "//div[@data-testid='tab-asset-order-type-{}' and contains(text(), '({})')]")

    # Control buttons locators
    __btn_actions = (By.CSS_SELECTOR, data_testid('asset-{}-button-{}'))  # EX: asset-open-button-close
    __btn_actions_by_id = (By.XPATH, "//th[text()='{}']/ancestor::tr//div[@data-testid='asset-{}-button-{}']")

    # Bulk operations locators
    __bulk_close = (By.CSS_SELECTOR, data_testid('bulk-close'))
    __drp_bulk_close = (By.CSS_SELECTOR, data_testid('dropdown-bulk-close-{}'))
    __bulk_delete = (By.CSS_SELECTOR, data_testid('bulk-delete'))
    __order_sort = (By.CSS_SELECTOR, data_testid('order-sort-selector'))
    __opt_sort = (By.XPATH, "//div[@data-testid='sort-option-item']/div[text()='{}']")

    # Column preference locators
    __col_preference = (By.CSS_SELECTOR, data_testid('column-preference'))
    __btn_close_col_preference = (By.CSS_SELECTOR, data_testid('order-column-preference-modal-close'))
    __chb_show_all = (By.XPATH, "//div[@data-testid='order-column-preference-modal-select-all-{}']//div")
    __chb_col_preference = (
        By.XPATH, "//div[contains(@data-testid, 'order-column-preference-modal-item-{}') and text()='{}']//div"
    )
    __btn_save_changes = (By.CSS_SELECTOR, data_testid('order-column-preference-modal-save'))

    # Table locators
    __table_headers = (By.XPATH, "//*[@data-testid='asset-{}-table-header']//th[text()='{}']")

    __col_symbol = (By.CSS_SELECTOR, data_testid('asset-{}-column-symbol'))
    __col_order_ids = (By.CSS_SELECTOR, data_testid('asset-{}-column-order-id'))

    __first_item = (By.CSS_SELECTOR, "tr:first-of-type *[data-testid*='asset-{}-column']")
    __item_by_id = (By.XPATH, "//*[@data-testid='asset-{}-column-order-id' and text()='{}']")
    __cols_by_id = (By.XPATH, "//*[@data-testid='asset-{}-column-order-id' and text()='{}']/parent::tr/*[contains(@data-testid, 'asset')]")

    # Close order confirmation locators
    __txt_close_order = (By.CSS_SELECTOR, data_testid('close-order-input-volume'))
    __btn_min_volume = (By.XPATH, "//div[@data-testid='close-order-input-volume-static-min']/..")
    __btn_max_volume = (By.XPATH, "//div[@data-testid='close-order-input-volume-static-max']/..")
    __inc_dec_volume = (By.CSS_SELECTOR, data_testid('close-order-input-volume-{}'))

    # ------------------------ ACTIONS ------------------------ #
    def _is_tab_selected(self, tab: AssetTabs):
        tab_locator = cook_element(self.__tab, locator_format(tab))
        is_select = "selected" in self.actions.get_attribute(tab_locator, "class")
        return is_select

    def get_tab_amount(self, tab: AssetTabs) -> int:
        """Get the number of items in the specified tab."""
        time.sleep(2)
        amount = self.actions.get_text(cook_element(self.__tab, locator_format(tab)))
        return extract_asset_tab_number(amount)

    def get_last_order_id(self, trade_object: ObjTrade) -> str:
        """Get the latest order ID from the specified tab and update value into trade_object."""
        self.wait_for_spin_loader(timeout=SHORT_WAIT)
        tab = AssetTabs.get_tab(trade_object.order_type)
        trade_object.order_id = self.actions.get_text(cook_element(self.__col_order_ids, tab.col_locator()))
        return trade_object.order_id

    def get_order_ids(self, tab: AssetTabs) -> List[str]:
        """Get a list of displaying order IDs in the specified tab."""
        order_ids = self.actions.get_text_elements(cook_element(self.__col_order_ids, tab.col_locator()))
        return order_ids

    def get_item_data(self, tab: AssetTabs, order_id=None, trade_object: ObjTrade = None):
        """Get item data based on order_id or last item, DO NOT leave tab & trade_object = None at the same time"""
        locator = cook_element(self.__cols_by_id if order_id else self.__first_item, tab.col_locator(), order_id)
        elements = self.actions.find_elements(locator)
        res = {
            ele.get_attribute("data-testid").split("column-")[-1].replace("-", "_"): ele.text.strip() for ele in elements
        }

        # reformat size vs volume column
        if "size" in res:
            res["volume"] = res.pop("size")

        # todo: improve to check close_volume / x
        if tab.is_history():
            res["volume"] = res["volume"].split(" / ")[0]

        logger.debug(f"- Item summary: {format_dict_to_string(res)}")
        if trade_object is not None:
            res.pop("order_type", None)
            trade_object |= res

        return res

    def select_tab(self, tab: AssetTabs) -> None:
        """Select the specified asset tab."""
        if self._is_tab_selected(tab):
            logger.debug("- Tab already selected")
            return

        logger.debug(f"- Select asset tab: {tab.capitalize()}")
        self.actions.click(cook_element(self.__tab, locator_format(tab)))
        self.wait_for_spin_loader()

    def select_last_symbol(self, tab: AssetTabs) -> None:
        """Select the last symbol in the specified tab."""
        locator = cook_element(self.__col_symbol, tab.col_locator())
        self.actions.click(locator)

    def wait_for_tab_amount(self, tab: AssetTabs, expected_amount: int) -> None:
        """Wait for the asset tab amount to match the expected amount."""
        self.actions.wait_for_element_visible(
            cook_element(self.__tab_amount, locator_format(tab), expected_amount)
        )

    def _click_action_btn(self, tab: AssetTabs, order_id=0, action: Literal["close", "edit", "track"] = "close") -> None:
        btn = cook_element(self.__btn_actions, tab.col_locator(), action) if not order_id else cook_element(self.__btn_actions_by_id, order_id, tab.col_locator(), action)
        self.actions.click(btn)

    def delete_order(self, trade_object: ObjTrade, confirm=True, wait=False) -> None:
        """Delete a pending order by ID or the last order if no ID provided."""
        if not trade_object.get("order_id"):
            self.get_last_order_id(trade_object)

        self._click_action_btn(AssetTabs.PENDING_ORDER, trade_object.get("order_id"), "close")
        not confirm or self.confirm_delete_order()
        not wait or self.wait_for_spin_loader()

    def bulk_delete_orders(self, wait=False) -> None:
        """Delete multiple pending orders at once."""
        self.actions.click(self.__bulk_delete)
        self.confirm_bulk_delete()
        not wait or self.wait_for_spin_loader()

    def full_close_position(self, trade_object: ObjTrade = None, order_id=0, confirm=True, wait=False) -> None:
        if trade_object:
            trade_object.get("order_id") or self.get_last_order_id(trade_object)  # update order_id for trade_object

        self._click_action_btn(AssetTabs.OPEN_POSITION, order_id or trade_object.get('order_id'), "close")

        if confirm:
            if trade_object:
                self.get_server_device_time(trade_object)  # update close time
            self.confirm_close_order()

        not wait or self.wait_for_spin_loader()

    def partial_close_position(self, close_obj: ObjTrade, volume=0, confirm=True, wait=False):
        new_created_obj = ObjTrade(**{k: v for k, v in close_obj.items() if k != "order_id"})
        close_obj.get("order_id") or self.get_last_order_id(close_obj)  # update order_id for trade_object

        self._click_action_btn(AssetTabs.OPEN_POSITION, close_obj.get("order_id", 0), "close")

        if volume:
            close_volume = volume
            close_obj["close_volume"] = close_volume
        else:
            # random closed volume value
            values = calculate_partial_close(close_obj)
            close_volume = values.close_volume

            # update volume for old and new created obj
            new_created_obj |= dict(volume=values.left_volume, units=values.left_units)
            close_obj |= dict(volume=values.close_volume, units=values.close_units)

        self.actions.send_keys(self.__txt_close_order, close_volume)
        if confirm:
            self.get_server_device_time(close_obj)
            self.confirm_close_order()

        not wait or self.wait_for_spin_loader()
        return new_created_obj

    def bulk_close_positions(self, option: BulkCloseOpts = BulkCloseOpts.ALL, wait=False) -> None:
        """Close multiple positions at once using the specified option."""
        self.actions.click(self.__bulk_close)
        self.actions.click(cook_element(self.__drp_bulk_close, locator_format(option)))
        self.confirm_bulk_close(option)

        if wait:
            self.wait_for_spin_loader()

    def adjust_close_volume_by_control_button(
            self,
            min_volume: bool = False,
            max_volume: bool = False,
            inc_step: bool = False,
            dec_step: bool = False,
    ) -> None:
        """Adjust the close volume using control buttons."""
        not min_volume or self.actions.click(self.__btn_min_volume)
        not max_volume or self.actions.click(self.__btn_max_volume)

        if inc_step:
            inc_step = inc_step if isinstance(inc_step, int) else random.randint(10, 20)
            for _ in range(inc_step):
                self.actions.click(cook_element(self.__inc_dec_volume, "increase", inc_step))

        if dec_step:
            dec_step = dec_step if isinstance(dec_step, int) else random.randint(1, 10)
            for _ in range(dec_step):
                self.actions.click(cook_element(self.__inc_dec_volume, "decrease", dec_step))

    def apply_sorting(self, option: Optional[SortOptions] = None) -> None:
        """Apply sorting to the items in the current tab."""
        option = option or SortOptions.sample_values()
        self.actions.click(self.__order_sort)
        self.actions.click(cook_element(self.__opt_sort, option))
        self.actions.click(self.__order_sort)
        time.sleep(0.5)

    def set_column_preference(
            self,
            tab: AssetTabs,
            options: Optional[List[ColPreference] | ColPreference] = None,
            unchecked: bool = True,
            close_modal: bool = True
    ) -> None:
        """Set column preferences for the specified tab."""
        if options:
            options = options if isinstance(options, list) else [options]
        else:
            options = ColPreference.get_random_columns(tab, amount=random.randint(1, 5))

        custom = "checked" if unchecked else "unchecked"
        self.select_tab(tab)
        self.actions.click(self.__col_preference)
        time.sleep(1)  # wait a bit

        for option in options:
            locator = cook_element(self.__chb_col_preference, custom, option)
            if option == ColPreference.SHOW_ALL:
                locator = cook_element(self.__chb_show_all, custom, option)

            if unchecked and self.actions.is_element_displayed(locator):
                logger.debug(f"- Uncheck option: {option!r}")
                self.actions.click(locator)

            if not unchecked and self.actions.is_element_displayed(locator):
                logger.debug(f"- Check option: {option!r}")
                self.actions.click(locator)

        btn_save = self.actions.find_element(self.__btn_save_changes)
        if btn_save.is_enabled():
            self.actions.click(self.__btn_save_changes)
            time.sleep(2)  # wait a bit

        if close_modal:
            self.actions.click(cook_element(self.__btn_close_col_preference))

    def modify_order(
            self,
            trade_object: ObjTrade,
            sl_type: SLTPType = None,
            tp_type: SLTPType = None,
            expiry: Expiry = None,
            confirm=False,
            retry_count=0,
            max_retries=3
    ):
        """
        Modify stop loss/ take profit/ fill policy/ Expiry
        trade_object: should contain trade_type and order_type
        sl_type: Price or Points
        tp_type: Price or Points
        expiry: one by default, give this value if modifying expiry
        retry_count: Current retry attempt (used internally for recursion)
        max_retries: Maximum number of retry attempts
        """
        if retry_count >= max_retries:
            logger.error(f"Failed to display edit confirm modal after {max_retries} attempts")

        # Log retry attempts (skip for first attempt)
        if retry_count > 0:
            logger.warning(f"Edit confirm modal not displayed, retrying... ({retry_count}/{max_retries})")
            time.sleep(1)  # Wait before retrying

        tab = AssetTabs.get_tab(trade_object.order_type)
        self._click_action_btn(tab, trade_object.get('order_id'), "edit")

        trade_type, order_type = trade_object.trade_type, trade_object.order_type
        edit_price = trade_object.get("stop_limit_price") or trade_object.get("entry_price") or self.__trade_modals.get_edit_price()

        logger.debug(f"- Edit price is {edit_price!r}")
        stop_loss, take_profit = get_sl_tp(edit_price, trade_type, sl_type, tp_type).values()

        if sl_type:
            self.__trade_modals.input_edit_sl(stop_loss, sl_type)
            if sl_type == SLTPType.POINTS:
                stop_loss = self.__trade_modals.get_edit_sl()
                trade_object.sl_type = sl_type

            trade_object.stop_loss = stop_loss

        if tp_type:
            self.__trade_modals.input_edit_tp(take_profit, tp_type)
            if tp_type == SLTPType.POINTS:
                take_profit = self.__trade_modals.get_edit_tp()
                trade_object.tp_type = tp_type

            trade_object.take_profit = take_profit

        if expiry:
            self.__trade_modals.select_expiry(expiry)
            trade_object.expiry = expiry

        self.__trade_modals.click_edit_order_btn()

        # check if edit confirm modal is displayed
        if not self.__trade_modals.is_edit_confirm_modal_displayed():
            # Recursive call with incremented retry count
            self.modify_order(trade_object, sl_type, tp_type, expiry, confirm, retry_count + 1, max_retries)

        # Success case - confirm modal is displayed
        not confirm or self.__trade_modals.confirm_update_order()

    def modify_invalid_order(
            self,
            trade_object: ObjTrade,
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
        self._click_action_btn(AssetTabs.get_tab(order_type), trade_object.get("order_id"), "edit")

        if entry_price:
            price = get_pending_price(self.__trade_modals.get_edit_price(), trade_type, order_type, True)
            self.__trade_modals.input_edit_price(price, order_type)

        if stop_limit_price:
            stp_price = get_stop_price(self.__trade_modals.get_edit_price(order_type), trade_type, True)
            self.__trade_modals.input_edit_stp_price(stp_price, order_type)

        invalid_sl_tp = get_sl_tp(
            self.__trade_modals.get_edit_price(order_type), trade_type, True
        )
        if stop_loss:
            sl = invalid_sl_tp.sl.price
            self.__trade_modals.input_edit_sl(sl)

        if take_profit:
            tp = invalid_sl_tp.tp.price
            self.__trade_modals.input_edit_tp(tp)

        self.__trade_modals.click_edit_order_btn()
        if submit:
            self.__trade_modals.confirm_update_order()

    def modify_order_with_control_buttons(
            self, trade_object: ObjTrade = None,
            stop_loss=True,
            take_profit=True,
    ):
        stop_limit_price = trade_object.order_type.is_stp_limit()
        price = not trade_object.order_type == OrderType.MARKET

        self.__trade_modals.control_price(trade_object.order_type, stop_limit_price, price, stop_loss, take_profit)

        # Load data to trade_object for verifying
        trade_object.stop_loss = self.__trade_modals.get_edit_sl()
        trade_object.take_profit = self.__trade_modals.get_edit_tp()

        if trade_object.order_type != OrderType.MARKET:
            trade_object.entry_price = self.__trade_modals.get_edit_price(trade_object.order_type)

        if trade_object.order_type == OrderType.STOP_LIMIT:
            trade_object.stop_limit_price = self.__trade_modals.get_edit_stp_price()

        self.__trade_modals.click_edit_order_btn()
        self.__trade_modals.confirm_update_order()

    # ------------------------ VERIFY ------------------------ #
    def verify_tab_amount(self, tab: AssetTabs, expected_amount: int) -> None:
        """Verify that the tab amount matches the expected amount."""
        self.wait_for_tab_amount(tab, expected_amount)
        soft_assert(self.get_tab_amount(tab), expected_amount)

    def verify_tab_selected(self, tab: AssetTabs = AssetTabs.OPEN_POSITION):
        locator = cook_element(self.__tab, locator_format(tab))
        is_select = "selected" in self.actions.get_attribute(locator, "class")
        soft_assert(is_select, True, error_message=f"Tab {tab.value!r} is not selected")

    def verify_item_data(self, trade_object: ObjTrade, tab: AssetTabs = None, wait=False) -> None:
        """Verify item data in asset tab"""
        not wait or self.wait_for_spin_loader()
        tab = tab or AssetTabs.get_tab(trade_object.order_type)

        # update current price for trade_object
        self.get_current_price(trade_object)
        expected = trade_object.asset_item_data(tab)

        # actual
        item_data = self.get_item_data(tab, trade_object.get("order_id"))
        if not trade_object.get("order_id"):
            trade_object.order_id = item_data.get("order_id", 0)

        actual = {k: v for k, v in item_data.items() if k in expected}

        # handle convert str time to timestamp for verifying
        if actual.get("open_date"):
            actual["open_date"] = convert_strtime(actual["open_date"])

        if actual.get("close_date"):
            actual["close_date"] = convert_strtime(actual["close_date"])

        soft_assert(actual, expected, tolerance=1, tolerance_fields=trade_object.tolerance_fields())

    def verify_item_displayed(self, tab: AssetTabs, order_id: int | str | list, is_display: bool = True) -> None:
        """Verify that an item is displayed or not displayed."""
        order_id = order_id if isinstance(order_id, list) else [order_id]
        locator_list = [cook_element(self.__item_by_id, tab.col_locator(), _id) for _id in order_id]
        self.actions.verify_elements_displayed(locator_list, timeout=EXPLICIT_WAIT, is_display=is_display)

    def verify_volume_btn_disabled(
            self,
            min_button: bool = False,
            max_button: bool = False,
            dec_button: bool = False,
            inc_button: bool = False
    ) -> None:
        """Verify that specified buttons are disabled."""
        error_message = lambda _locator: f"Button {_locator} is not disabled"
        condition = lambda _locator: "disabled" in self.actions.get_attribute(_locator, "class")

        if min_button:
            logger.debug("- Check min button is disabled")
            locator = self.__btn_min_volume
            soft_assert(condition(locator), True, error_message=error_message(locator))

        if max_button:
            logger.debug("- Check max button is disabled")
            locator = self.__btn_max_volume
            soft_assert(condition(locator), True, error_message=error_message(locator))

        if inc_button:
            logger.debug("- Check increase button is disabled")
            locator = cook_element(self.__inc_dec_volume, "increase")
            soft_assert(condition(locator), True, error_message=error_message(locator))

        if dec_button:
            logger.debug("- Check decrease button is disabled")
            locator = cook_element(self.__inc_dec_volume, "decrease")
            soft_assert(condition(locator), True, error_message=error_message(locator))

    def verify_min_max_value(self, min_value: Optional[int] = None, max_value: Optional[int] = None) -> None:
        """Verify that the volume value is within the specified range."""
        actual_volume = self.actions.get_value(self.__txt_close_order)
        not min_value or soft_assert(actual_volume, min_value)
        not max_value or soft_assert(actual_volume, max_value)

    def verify_table_headers_displayed(
            self,
            tab: AssetTabs,
            headers: List[ColPreference] | ColPreference,
            is_display: bool = True,
    ) -> None:
        """Verify that specified table headers are displayed or not displayed."""
        self.select_tab(tab)
        headers = headers if isinstance(headers, list) else [headers]

        for header in headers:
            self.actions.verify_element_displayed(
                cook_element(self.__table_headers, tab.col_locator(), header),
                is_display=is_display
            )
