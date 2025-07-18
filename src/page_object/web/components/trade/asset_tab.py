import random
import time
from typing import Optional, List, Literal

from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import SHORT_WAIT
from src.data.enums import AssetTabs, ColPreference, SortOptions, BulkCloseOpts
from src.data.objects.trade_object import ObjectTrade
from src.page_object.web.components.trade.base_trade import BaseTrade
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import data_testid, cook_element
from src.utils.format_utils import extract_asset_tab_number, format_dict_to_string, locator_format
from src.utils.logging_utils import logger
from src.utils.trading_utils import calculate_partial_close


class AssetTab(BaseTrade):
    """
    A class representing the Asset Tab in the trading interface.
    Handles all interactions with the asset tab UI elements and operations.
    """

    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __tab = (By.CSS_SELECTOR, data_testid('tab-asset-order-type-{}'))
    __tab_amount = (By.XPATH, "//div[@data-testid='tab-asset-order-type-{}' and contains(text(), '({})')]")

    # Control buttons locators
    __btn_edit = (By.CSS_SELECTOR, data_testid('asset-{}-button-edit'))
    __btn_edit_by_id = (
        By.XPATH,
        "//th[text()='{}']/ancestor::*[@data-testid='asset-{}-list-item']//div[@data-testid='asset-{}-button-edit']"
    )
    __btn_close_delete = (By.CSS_SELECTOR, data_testid('asset-{}-button-close'))
    __btn_close_delete_by_id = (
        By.XPATH,
        "//th[@data-testid='asset-{}-column-order-id' and text()='{}']/ancestor::tr//div[@data-testid='asset-{}-button-close']"
    )

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
    __item_profit_by_id = (
        By.XPATH,
        "//div[contains(text(), '+')]/ancestor::td[@data-testid='asset-open-column-profit']"
        "/preceding-sibling::th[@data-testid='asset-open-column-order-id']"
    )
    __item_loss_by_id = (
        By.XPATH,
        "//div[contains(text(), '-')]/ancestor::td[@data-testid='asset-open-column-profit']"
        "/preceding-sibling::th[@data-testid='asset-open-column-order-id']"
    )

    # Close order confirmation locators
    __txt_close_order = (By.CSS_SELECTOR, data_testid('close-order-input-volume'))
    __btn_min_volume = (By.XPATH, "//div[@data-testid='close-order-input-volume-static-min']/..")
    __btn_max_volume = (By.XPATH, "//div[@data-testid='close-order-input-volume-static-max']/..")
    __inc_dec_volume = (By.CSS_SELECTOR, data_testid('close-order-input-volume-{}'))

    # ------------------------ HELPER METHODS ------------------------ #
    def get_tab_amount(self, tab: AssetTabs) -> int:
        """Get the number of items in the specified tab."""
        time.sleep(2)
        amount = self.actions.get_text(cook_element(self.__tab, locator_format(tab)))
        return extract_asset_tab_number(amount)

    def get_last_order_id(self, trade_object: ObjectTrade, tab: AssetTabs = None) -> str:
        """Get the latest order ID from the specified tab and update value into trade_object."""
        tab = tab or AssetTabs.get_tab(trade_object.order_type)

        self.select_tab(tab)
        element = self.actions.find_element(
            cook_element(self.__col_order_ids, tab.get_col()), raise_exception=False
        )
        order_id = element.text.strip() if element else 0
        trade_object.order_id = order_id

        return order_id

    def _get_col_value(
            self,
            tab: AssetTabs,
            col_name: Literal["order-id", "open-date", "close-date", "profit", "symbol"]
    ) -> List[str]:
        """Get values from a specific column in the table."""
        self.select_tab(tab)
        elements = self.actions.find_elements(cook_element(self.__cols, tab.get_col(), locator_format(col_name)))
        return [ele.text.strip() for ele in elements] if elements else []

    def get_order_id_list(self, tab: AssetTabs) -> List[str]:
        """Get a list of all order IDs in the specified tab."""
        return self._get_col_value(tab, "order-id")

    def _get_open_date_list(self, tab: AssetTabs) -> List[str]:
        """Get a list of all open dates in the specified tab."""
        return self._get_col_value(tab, "open-date")

    def _get_close_date_list(self, tab: AssetTabs) -> List[str]:
        """Get a list of all close dates in the specified tab."""
        return self._get_col_value(tab, "close-date")

    def _get_profit_list(self, tab: AssetTabs) -> List[str]:
        """Get a list of all profits in the specified tab."""
        return self._get_col_value(tab, "profit")

    def _get_symbol_list(self, tab: AssetTabs) -> List[str]:
        """Get a list of all symbols in the specified tab."""
        return self._get_col_value(tab, "symbol")

    def get_item_data(self, tab: AssetTabs = None, order_id=None, trade_object: ObjectTrade = None):
        """Get item data based on order_id or last item, DO NOT leave tab & trade_object = None at the same time"""

        if not tab and trade_object is not None:
            tab = AssetTabs.get_tab(trade_object.get("order_type"))

        locator = cook_element(self.__cols_by_id if order_id else self.__first_item, tab.get_col(), order_id)
        elements = self.actions.find_elements(locator)
        res = {
            ele.get_attribute("data-testid").split("column-")[-1].replace("-", "_"): ele.text.strip() for ele in elements
        }

        if "size" in res:
            res["volume"] = res.pop("size")

        # todo: improve to check close_volume / x
        if tab in [AssetTabs.HISTORY, AssetTabs.POSITIONS_HISTORY]:
            res["volume"] = res["volume"].split(" / ")[0]

        logger.debug(f"- Item summary: {format_dict_to_string(res)}")

        if trade_object:
            res.pop("order_type", None)
            trade_object |= res

        return res

    # ------------------------ ACTIONS ------------------------ #
    def select_tab(self, tab: AssetTabs) -> None:
        """Select the specified asset tab."""
        tab_locator = cook_element(self.__tab, locator_format(tab))
        self.actions.click(tab_locator)
        self.wait_for_spin_loader()

    def select_last_symbol(self, tab: AssetTabs) -> None:
        """Select the last symbol in the specified tab."""
        self.select_tab(tab)
        locator = cook_element(self.__col_symbol, tab.get_col())
        self.actions.click(locator)

    def wait_for_tab_amount(self, tab: AssetTabs, expected_amount: int) -> None:
        """Wait for the asset tab amount to match the expected amount."""
        self.actions.wait_for_element_visible(
            cook_element(self.__tab_amount, locator_format(tab), expected_amount)
        )

    def click_edit_button(self, tab: AssetTabs, order_id=0) -> None:
        """Click the edit button for an item in the specified tab."""
        self.select_tab(tab)
        locator = cook_element(self.__btn_edit, tab.get_col())

        if order_id:
            locator = cook_element(self.__btn_edit_by_id, order_id, tab.get_col(), tab.get_col())

        self.actions.click(locator)

    def click_close_button(self, tab: AssetTabs = AssetTabs.OPEN_POSITION) -> None:
        """Click the close button last item in the specified tab."""
        self.select_tab(tab)
        self.actions.click(cook_element(self.__btn_close_delete, tab.get_col()))

    click_delete_button = click_close_button

    def delete_pending_order(self, order_id: int = 0, trade_object: ObjectTrade = None, confirm=True, wait=False) -> None:
        """Delete a pending order by ID or the last order if no ID provided."""
        tab = AssetTabs.PENDING_ORDER
        if order_id:
            # delete order with specific id
            self.select_tab(tab)
            locator = cook_element(self.__btn_close_delete_by_id, tab.get_col(), order_id, tab.get_col())
            self.actions.click(locator)
        else:
            # delete last item
            if trade_object:
                # load delete order_id for trade_object if provided
                self.get_last_order_id(trade_object, tab)

            self.actions.click(cook_element(self.__btn_close_delete, tab.get_col()))

        if confirm:
            self.confirm_delete_order()
        if wait:
            self.wait_for_spin_loader()

    def bulk_delete_orders(self, wait=False) -> None:
        """Delete multiple pending orders at once."""
        self.select_tab(AssetTabs.PENDING_ORDER)
        self.actions.click(self.__bulk_delete)
        self.confirm_bulk_delete()

        if wait:
            self.wait_for_spin_loader()

    def full_close_position(self, order_id: int = 0, confirm=True, wait=False) -> None:
        tab = AssetTabs.OPEN_POSITION
        self.select_tab(tab)
        if order_id:
            self.actions.click(cook_element(self.__btn_close_delete_by_id, tab.get_col(), order_id, tab.get_col()))

        else:
            self.click_close_button()

        not confirm or self.confirm_close_order()
        not wait or self.wait_for_spin_loader()

    def partial_close_position(self, order_id=0, trade_object=None, volume=0, confirm=True, wait=False):
        order_id = order_id or trade_object.get("order_id", 0)
        tab = AssetTabs.OPEN_POSITION
        if order_id:
            self.actions.click(
                cook_element(self.__btn_close_delete_by_id, tab.get_col(), order_id, tab.get_col())
            )
        else:
            self.click_close_button()

        if volume:
            close_volume = volume
            if trade_object is not None:
                trade_object["close_volume"] = close_volume

        else:
            # random closed volume value
            values = calculate_partial_close(trade_object)
            close_volume = values.close_volume

            if trade_object:
                trade_object |= {
                    "volume": values.left_volume, "close_volume": close_volume,
                    "units": values.left_units, "close_units": values.close_units
                }

        self.actions.send_keys(self.__txt_close_order, close_volume)
        not confirm or self.confirm_close_order()
        not wait or self.wait_for_spin_loader()

    def bulk_close_positions(self, option: BulkCloseOpts = BulkCloseOpts.ALL, wait=False) -> None:
        """Close multiple positions at once using the specified option."""
        self.select_tab(AssetTabs.OPEN_POSITION)
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

    # ------------------------ VERIFY ------------------------ #
    def verify_tab_amount(self, tab: AssetTabs, expected_amount: int) -> None:
        """Verify that the tab amount matches the expected amount."""
        self.wait_for_tab_amount(tab, expected_amount)
        soft_assert(self.get_tab_amount(tab), expected_amount)

    def verify_tab_selected(self, tab: AssetTabs = AssetTabs.OPEN_POSITION):
        locator = cook_element(self.__tab, locator_format(tab))
        is_select = "selected" in self.actions.get_attribute(locator, "class")
        soft_assert(is_select, True, error_message=f"Tab {tab.value!r} is not selected")


    def verify_item_data(self, trade_object: ObjectTrade, tab: AssetTabs = None) -> None:
        """Verify item data in asset tab"""
        tab = tab or AssetTabs.get_tab(trade_object.order_type)
        self.select_tab(tab)

        expected = trade_object.asset_item_data(tab)

        # actual
        item_data = self.get_item_data(tab, trade_object.get("order_id"))
        actual = {k: v for k, v in item_data.items() if k in expected}

        soft_assert(actual, expected, tolerance=0.1, tolerance_fields=trade_object.tolerance_fields())

    def verify_item_displayed(self, tab: AssetTabs, order_id: int | str | list, is_display: bool = True) -> None:
        """Verify that an item is displayed or not displayed."""
        self.select_tab(tab)
        order_id = order_id if isinstance(order_id, list) else [order_id]
        locator_list = [cook_element(self.__item_by_id, tab.get_col(), _id) for _id in order_id]
        self.actions.verify_elements_displayed(locator_list, timeout=SHORT_WAIT, is_display=is_display)

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
                cook_element(self.__table_headers, tab.get_col(), header),
                is_display=is_display
            )
