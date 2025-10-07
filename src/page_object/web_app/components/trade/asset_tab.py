import time
from typing import Dict, Any
from typing import Literal

from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.enums import BulkCloseOpts, AssetTabs, SLTPType, Expiry
from src.data.objects.trade_obj import ObjTrade
from src.data.project_info import RuntimeConfig
from src.page_object.web_app.components.modals.trading_modals import TradingModals
from src.page_object.web_app.components.trade.base_trade import BaseTrade
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element, data_testid
from src.utils.format_utils import locator_format, extract_asset_tab_number, format_dict_to_string, is_float
from src.utils.logging_utils import logger
from src.utils.trading_utils import calculate_partial_close, get_sl_tp


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
    __tab_amount = (By.XPATH, "//div[@data-testid='tab-asset-order-type-{}' and contains(normalize-space(), '({})')]")

    __item_by_id = (By.XPATH, "//div[@data-testid='asset-{}-list-item-order-no' and contains(normalize-space(), '{}')]")
    __order_id_items = (By.CSS_SELECTOR, "*[data-testid='asset-{}-list-item-order-no']")
    __expand_items = (By.CSS_SELECTOR, data_testid('asset-{}-list-item-expand'))
    __expand_item_by_id = (By.XPATH, "//div[text()='{}']/ancestor::div[2]/following-sibling::div")
    __expand_item_profit_loss = (
        By.XPATH, "//div[@data-testid='asset-open-list-item-expand']/div[contains(normalize-space(), 'Profit/Loss')]"
    )
    __expanded_values = (By.CSS_SELECTOR, "div[data-testid^='asset-{}-column-'][data-testid$='-value']")
    __expanded_symbol = (By.CSS_SELECTOR, data_testid('asset-detailed-header-symbol'))
    __expanded_order_type = (By.CSS_SELECTOR, data_testid('asset-order-type'))  # buy or sell
    __btn_cancel_expand_item = (By.CSS_SELECTOR, data_testid('action-sheet-cancel-button'))

    # Control buttons locators
    __btn_action = (By.CSS_SELECTOR, data_testid('asset-{}-button-{}'))  # actions including close, edit, track
    __btn_action_by_id = (
        By.XPATH, "//div[contains(normalize-space(), '{}')]/..//div[@data-testid='asset-{}-button-{}']"  # - orderID - tab col - btn action
    )
    __txt_close_volume = (By.CSS_SELECTOR, data_testid('close-order-input-volume'))

    # Bulk operations locators
    __btn_bulk_close = (By.CSS_SELECTOR, data_testid('bulk-close'))
    __opt_bulk_close = (By.XPATH, "//div[text()='{}']")
    __btn_bulk_delete = (By.CSS_SELECTOR, data_testid('bulk-delete'))

    # ------------------------ HELPER METHODS ------------------------ #
    def get_profit_loss(self, wait=True):
        not wait or self.wait_for_spin_loader()
        res = self.actions.get_text_elements(self.__expand_item_profit_loss)
        res = [item.split("\n")[-1].replace("--", "0") for item in res]
        return [(float(item) if is_float(item) else 0) for item in res]

    def get_tab_amount(self, tab: AssetTabs, wait=True):
        """Get the number of items in the specified tab."""
        not wait or self.wait_for_spin_loader()
        amount = self.actions.get_text(cook_element(self.__tab, locator_format(tab)))
        return extract_asset_tab_number(amount)

    def get_last_order_id(self, tab: AssetTabs, wait=True):
        """Get the latest order ID from the specified tab."""
        not wait or self.wait_for_spin_loader()
        order_id = self.actions.get_text(cook_element(self.__order_id_items, tab.col_locator())).split(": ")[-1]
        logger.debug(f"- Latest orderID: {order_id!r}")
        return order_id

    def get_expand_item_data(self, tab: AssetTabs, trade_object: ObjTrade) -> Dict[str, Any]:
        """Get detailed data for an expanded item in the specified tab."""
        # expand the item
        expand_item = cook_element(self.__expand_items, tab.col_locator())  # last item
        if trade_object.get("order_id"):
            expand_item = cook_element(self.__expand_item_by_id, trade_object.order_id, tab.col_locator())

        time.sleep(0.5)
        self.actions.click(expand_item)
        logger.debug("- Item expanded, getting item data...")

        # re-assign tab in cased of history - to get correct col locator
        tab = AssetTabs.HISTORY if tab.is_history() else tab
        res = {
            ele.get_attribute("data-testid").split("-column-")[-1].replace("-value", "").replace("-", "_"): ele.text.strip()
            for ele in self.actions.find_elements(cook_element(self.__expanded_values, tab.col_locator()))
        }

        # special locators
        res["order_type"] = self.actions.get_text(self.__expanded_order_type)
        res["symbol"] = self.actions.get_text(self.__expanded_symbol)

        logger.debug(f"Item summary: {format_dict_to_string(res)}")

        # reformat size vs volume column for consistent
        if "size" in res:
            res["volume"] = res.pop("size")

        if tab.is_history() and res.get("volume"):  # todo: improve to check close_volume / x
            res["volume"] = res["volume"].split(" / ")[0]

        # update order_id for trade_object if not present
        trade_object.get("order_id") or trade_object.update(dict(order_id=res.get("order_id", None)))

        # close expand item
        self.actions.click(self.__btn_cancel_expand_item)
        return res

    # ------------------------ ACTIONS ------------------------ #
    def select_tab(self, tab: AssetTabs, wait=False) -> None:
        """Select the specified asset tab."""
        tab_locator = tab
        if tab.is_history():
            if not RuntimeConfig.is_mt4():
                tab_locator = f"{AssetTabs.HISTORY} {AssetTabs.POSITIONS_HISTORY}"
            else:
                tab_locator = AssetTabs.HISTORY

        self.actions.click(cook_element(self.__tab, locator_format(tab_locator)))
        not wait or self.wait_for_spin_loader()

    def wait_for_tab_amount(self, tab: AssetTabs, expected_amount: int) -> None:
        """Wait for the asset tab amount to match the expected amount."""
        self.actions.wait_for_element_visible(
            cook_element(self.__tab_amount, locator_format(tab), expected_amount)
        )

    def click_action_btn(self, tab: AssetTabs, order_id=0, action: Literal["edit", "close"] = "edit"):
        locator = cook_element(self.__btn_action, tab.col_locator(), action)
        if order_id:
            locator = cook_element(self.__btn_action_by_id, order_id, tab.col_locator(), action)
        self.actions.click(locator)

    def delete_order(self, trade_object: ObjTrade, confirm=True) -> None:
        """Delete a pending order by ID or the last order if no ID provided."""
        if not trade_object.get("order_id"):
            trade_object.order_id = self.get_last_order_id(AssetTabs.PENDING_ORDER)

        logger.debug(f"- Deleting order: {trade_object.get('order_id')!r}")
        self.click_action_btn(AssetTabs.PENDING_ORDER, trade_object.get("order_id"), "close")

        not confirm or self.confirm_delete_order()

    def bulk_delete_orders(self) -> None:
        """Delete multiple pending orders at once."""
        time.sleep(1)
        self.actions.click(self.__btn_bulk_delete)
        self.click_confirm_btn()

    def full_close_position(self, trade_object: ObjTrade = None, order_id=0, confirm=True, wait=True) -> None:
        order_id = order_id if order_id else trade_object.get("order_id") if trade_object else 0
        if not order_id:
            order_id = self.get_last_order_id(AssetTabs.OPEN_POSITION)
            if trade_object:
                trade_object.order_id = order_id

        logger.debug(f"- Close order with ID: {order_id!r}")
        self.click_action_btn(AssetTabs.OPEN_POSITION, order_id, "close")

        if confirm:
            not trade_object or self.get_current_price(trade_object)
            self.confirm_close_order()

        not wait or self.wait_for_spin_loader()

    def partial_close_position(self, close_obj: ObjTrade, volume=0, confirm=True, wait=False):
        new_created_obj = ObjTrade(**{k: v for k, v in close_obj.items() if k != "order_id"})
        if not close_obj.get("order_id"):
            close_obj.order_id = self.get_last_order_id(AssetTabs.OPEN_POSITION)

        self.click_action_btn(AssetTabs.OPEN_POSITION, close_obj.get("order_id", 0), "close")

        if volume:
            close_volume = volume
            close_obj["close_volume"] = close_volume
        else:
            # random closed volume value
            values = calculate_partial_close(close_obj.volume, close_obj.units)
            close_volume = values.close_volume

            # update volume for old and new created obj
            new_created_obj |= dict(volume=values.left_volume, units=values.left_units)
            close_obj |= dict(volume=values.close_volume, units=values.close_units)

        # input closed volume
        time.sleep(0.5)
        self.actions.send_keys(self.__txt_close_volume, close_volume)

        if confirm:
            self.get_current_price(close_obj)  # update close price
            self.confirm_close_order()

        not wait or self.wait_for_spin_loader()
        return new_created_obj

    def bulk_close_positions(self, option: BulkCloseOpts = BulkCloseOpts.ALL, submit=False) -> None:
        """Close multiple positions at once using the specified option."""
        self.actions.click(self.__btn_bulk_close)

        options = {
            BulkCloseOpts.ALL: "All Positions",
            BulkCloseOpts.PROFIT: "Profitable Positions",
            BulkCloseOpts.LOSS: "Losing Positions",
        }

        self.actions.click(cook_element(self.__opt_bulk_close, options[option]))

        if submit:
            self.click_confirm_btn()
        else:
            self.click_cancel_btn(cancel_all=False)

    def modify_order(
            self,
            trade_object: ObjTrade,
            sl_type: SLTPType = None,
            tp_type: SLTPType = None,
            confirm=False,
            retry_count=0,
            max_retries=3,
            oct_mode=False,
    ):
        if retry_count >= max_retries:
            logger.error(f"Failed to display edit confirm modal after {max_retries} attempts")
            return

        # Log retry attempts (skip for first attempt)
        if retry_count > 0:
            logger.warning(f"Edit confirm modal not displayed, retrying... ({retry_count}/{max_retries})")
            time.sleep(1)  # Wait before retrying
            self.select_tab(AssetTabs.get_tab(trade_object.order_type))

        self.click_action_btn(AssetTabs.get_tab(trade_object.order_type), trade_object.get("order_id"), "edit")

        # Get current price to re-calculate prices
        self.__trade_modals.fill_update_order(trade_object, sl_type, tp_type)

        time.sleep(1)
        self.__trade_modals.click_update_order_btn()

        # check if edit confirm modal is displayed
        if not self.__trade_modals.is_edit_confirm_modal_displayed() and not oct_mode:
            # Recursive call with incremented retry count
            self.modify_order(trade_object, sl_type, tp_type, confirm, retry_count + 1, max_retries)

        # Success case - confirm modal is displayed
        not confirm or self.__trade_modals.confirm_update_order()

    # ------------------------ VERIFY ------------------------ #
    def verify_tab_amount(self, tab: AssetTabs, expected_amount: int) -> None:
        """Verify that the tab amount matches the expected amount."""
        self.actions.verify_element_displayed(cook_element(self.__tab_amount, locator_format(tab), expected_amount))

    def verify_item_data(self, trade_object: ObjTrade, tab: AssetTabs = None, wait=False) -> None:
        """Verify that the item data matches the expected data."""
        if wait:
            self.wait_for_spin_loader()

        tab = tab or AssetTabs.get_tab(trade_object.order_type)
        # handle expected
        self.get_current_price(trade_object)  # update current price for trade_object
        expected = trade_object.asset_item_data(tab)

        # handle actual
        actual = self.get_expand_item_data(tab, trade_object)
        soft_assert(actual, expected, check_contains=True, tolerance=1, tolerance_fields=trade_object.tolerance_fields())

    def verify_item_displayed(self, tab: AssetTabs, order_id: int | str | list, is_display: bool = True) -> None:
        """Verify that an item is displayed or not displayed."""
        order_id = order_id if isinstance(order_id, list) else [order_id]
        locators = [cook_element(self.__item_by_id, tab.col_locator(), _id) for _id in order_id]
        self.actions.verify_elements_displayed(locators, is_display=is_display)
