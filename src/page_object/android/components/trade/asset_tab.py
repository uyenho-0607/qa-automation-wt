import time
from typing import Dict, Any
from typing import Literal

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import SHORT_WAIT
from src.data.enums import AssetTabs, BulkCloseOpts, SLTPType, Expiry
from src.data.objects.trade_obj import ObjTrade
from src.data.project_info import RuntimeConfig
from src.page_object.android.components.modals.trading_modals import TradingModals
from src.page_object.android.components.trade.base_trade import BaseTrade
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element
from src.utils.format_utils import locator_format, extract_asset_tab_number, format_dict_to_string, is_float
from src.utils.logging_utils import logger
from src.utils.trading_utils import calculate_partial_close, get_sl_tp


class AssetTab(BaseTrade):
    """
    A class representing the Asset Tab in the trading interface.
    Handles all interactions with the asset tab UI elements and operations.
    """

    def __init__(self, actions: MobileActions):
        super().__init__(actions)
        self.__trade_modals = TradingModals(actions)

    # ------------------------ LOCATORS ------------------------ #
    __tab = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tab-asset-order-type-{}")') # locator_format(tab)
    __tab_amount = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tab-asset-order-type-{}").descriptionContains("({})")') # locator_format(tab) + amount number

    # Item details locators
    __item_order_no = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("asset-{}-list-item-order-no")')
    __item_by_order_no = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("asset-{}-list-item-order-no").textContains("{}")')
    __expand_item = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("asset-{}-list-item-expand")')
    __expand_item_by_order_no = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("tab-asset-order-type-{}").descriptionContains("({})")'
    )
    __btn_cancel_expand_item = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("action-sheet-cancel-button")')

    # Item expanded data locators
    __expand_items = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*asset-{}-column.*-value")')
    __item_symbol = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("asset-detailed-header-symbol")')
    __item_order_type = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("asset-order-type")')
    __expand_item_profit_loss = (
        AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("asset-{}-list-item-expand").childSelector(new UiSelector().textContains("Profit/Loss"))'
    )
    
    # Control buttons locators
    __btn_action = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("asset-{}-button-{}")') # tab.col_locator(), action: close/ edit
    __btn_action_by_id = (
        AppiumBy.XPATH,
        "//*[@resource-id='asset-{}-list-item-order-no' and contains(@text, '{}')]"
        "/preceding-sibling::*[@resource-id='asset-{}-button-{}']"  # tab.col_locator, id , tab.col_locator(), action: close/ edit
    )

    # Bulk operations locators
    __btn_bulk_close = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("bulk-close")')
    __opt_bulk_close = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("{}")')
    __btn_bulk_delete = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("bulk-delete")')

    # Close order confirmation locators
    __txt_close_order = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("close-order-input-volume")')

    # ------------------------ HELPER METHODS ------------------------ #



    def get_profit_loss(self, wait=True):
        not wait or self.wait_for_spin_loader()
        res = self.actions.get_text_elements(cook_element(self.__expand_item_profit_loss, AssetTabs.OPEN_POSITION.col_locator()))
        res = [item.split("\n")[-1].replace("--", "0") for item in res]
        return [(float(item) if is_float(item) else 0) for item in res]

    def get_tab_amount(self, tab: AssetTabs, wait=True) -> int:
        """Get the number of items in the specified tab."""
        not wait or self.wait_for_spin_loader()
        amount = self.actions.get_content_desc(cook_element(self.__tab, locator_format(tab)))
        return extract_asset_tab_number(amount)

    def get_last_order_id(self, trade_object: ObjTrade = None, tab: AssetTabs = None) -> int:
        """
        Get the latest order ID from the specified tab
        -> update value into trade_object if provided
        -> if trade_object has order_type attr, no need to provide tab
        """
        self.wait_for_spin_loader()
        tab = tab or AssetTabs.get_tab(trade_object.order_type)

        res = self.actions.get_text(cook_element(self.__item_order_no, tab.col_locator()))
        order_id = res.split(": ")[-1] if res else 0
        
        if trade_object:
            trade_object.order_id = order_id

        logger.debug(f"> Latest order_id: {order_id!r}")
        return order_id

    def get_expand_item_data(self, tab: AssetTabs, trade_object: ObjTrade) -> Dict[str, Any]:
        """Get detailed data for an expanded item in the specified tab."""
        # expand the item
        expand_item = cook_element(self.__expand_item, tab.col_locator())  # last item
        if trade_object.get("order_id"):
            expand_item = cook_element(self.__expand_item_by_order_no, trade_object.order_id, tab.col_locator())
        
        self.actions.click(expand_item)
        logger.debug("- Item expanded, getting item data...")

        # re-assign tab in case of history - to get correct col locator
        tab = AssetTabs.HISTORY if tab.is_history() else tab
        
        res = {
            ele.get_attribute("resource-id").split("-column-")[-1].replace("-value", "").replace("-", "_"): ele.text.strip()
            for ele in self.actions.find_elements(cook_element(self.__expand_items, tab.col_locator()))
        }
        # get order-type and symbol
        res["order_type"] = self.actions.get_text(self.__item_order_type)
        res["symbol"] = self.actions.get_text(self.__item_symbol)

        logger.debug(f"Item summary: {format_dict_to_string(res)}")

        # reformat size vs volume column for consistent
        if "size" in res:
            res["volume"] = res.pop("size")

        if tab.is_history() and res.get("volume"):  # todo: improve to check close_volume / x
            res["volume"] = res["volume"].split(" / ")[0]

        # update order_id for trade_object if not present
        trade_object.get("order_id") or trade_object.update(dict(order_id=res.get("order_id")))

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
        """Click action button (edit/close) for an item in the specified tab."""
        locator = cook_element(self.__btn_action, tab.col_locator(), action)
        if order_id:
            locator = cook_element(self.__btn_action_by_id, tab.col_locator(), order_id, tab.col_locator(), action)
        self.actions.click(locator)

    def delete_order(self, trade_object: ObjTrade = None, order_id=0, confirm=True, wait=False) -> None:
        """
        Delete a pending order by ID or the last order if no ID provided.
        - if order_id provided: delete this orderID
        - if trade_object provided: with orderID: delete this orderID, if not: delete latest orderID + update this value to trade_object
        """
        order_id = order_id if order_id else trade_object.get("order_id") if trade_object else 0
        if not order_id:
            order_id = self.get_last_order_id(trade_object, AssetTabs.PENDING_ORDER)

        logger.debug(f"- Deleting order: {order_id!r}")
        self.click_action_btn(AssetTabs.PENDING_ORDER, order_id, "close")

        not confirm or self.confirm_delete_order()
        not wait or self.wait_for_spin_loader()

    def bulk_delete_orders(self) -> None:
        """Delete multiple pending orders at once."""
        time.sleep(1)
        self.actions.click(self.__btn_bulk_delete)
        self.click_confirm_btn()

    def full_close_position(self, trade_object: ObjTrade = None, order_id=0, confirm=True, wait=True) -> None:
        """Close a position completely."""
        order_id = order_id if order_id else trade_object.get("order_id") if trade_object else 0
        if not order_id:
            order_id = self.get_last_order_id(trade_object)

        logger.debug(f"- Close order with ID: {order_id!r}")
        self.click_action_btn(AssetTabs.OPEN_POSITION, order_id, "close")

        if confirm:
            not trade_object or self.get_current_price(trade_object)
            self.confirm_close_order()

        not wait or self.wait_for_spin_loader()

    def partial_close_position(self, close_obj: ObjTrade, volume=0, confirm=True, wait=False):
        """Partially close a position."""
        new_created_obj = ObjTrade(**{k: v for k, v in close_obj.items() if k != "order_id"})
        close_obj.get("order_id") or self.get_last_order_id(close_obj)  # update order_id for trade_object

        self.click_action_btn(AssetTabs.OPEN_POSITION, close_obj.get("order_id", 0), "close")

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

        # input closed volume
        time.sleep(0.5)
        self.actions.send_keys(self.__txt_close_order, close_volume)

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
            self.click_cancel_btn()

    def modify_order(
            self,
            trade_object: ObjTrade,
            sl_type: SLTPType = None,
            tp_type: SLTPType = None,
            expiry: Expiry = None,
            confirm=False,
            retry_count=0,
            max_retries=3,
            oct_mode=False,
    ):
        """
        Modify stop loss/ take profit/ fill policy/ Expiry
        trade_object: should contain trade_type and order_type
        sl_type: Price or Points
        tp_type: Price or Points
        expiry: None by default, give this value if modifying expiry
        retry_count: Current retry attempt (used internally for recursion)
        max_retries: Maximum number of retry attempts
        """
        if retry_count >= max_retries:
            logger.error(f"Failed to display edit confirm modal after {max_retries} attempts")
            return

        # Log retry attempts (skip for first attempt)
        if retry_count > 0:
            logger.warning(f"Edit confirm modal not displayed, retrying... ({retry_count}/{max_retries})")
            time.sleep(1)  # Wait before retrying
            self.select_tab(AssetTabs.get_tab(trade_object.order_type))

        trade_type, order_type = trade_object.trade_type, trade_object.order_type
        self.click_action_btn(AssetTabs.get_tab(order_type), trade_object.get("order_id"), "edit")

        # Get current price to re-calculate prices
        edit_price = trade_object.get("stop_limit_price") or trade_object.get("entry_price") or self.__trade_modals.get_edit_price()
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

        time.sleep(1)
        self.__trade_modals.click_update_order_btn()

        # check if edit confirm modal is displayed
        if not self.__trade_modals.is_edit_confirm_modal_displayed() and not oct_mode:
            # Recursive call with incremented retry count
            self.modify_order(trade_object, sl_type, tp_type, expiry, confirm, retry_count + 1, max_retries)

        # Success case - confirm modal is displayed
        not confirm or self.__trade_modals.confirm_update_order()

    # ------------------------ VERIFY ------------------------ #
    def verify_tab_amount(self, tab: AssetTabs, expected_amount: int) -> None:
        """Verify that the tab amount matches the expected amount."""
        self.wait_for_tab_amount(tab, expected_amount)
        soft_assert(self.get_tab_amount(tab, wait=False), expected_amount)

    def verify_item_data(self, trade_object: ObjTrade, tab: AssetTabs = None, wait=False) -> None:
        """Verify that the item data matches the expected data."""
        not wait or self.wait_for_spin_loader()
        tab = tab or AssetTabs.get_tab(trade_object.order_type)
        # handle expected
        self.get_current_price(trade_object)  # update current price for trade_object
        expected = trade_object.asset_item_data(tab)

        if not trade_object.order_type.is_market():
            expected["price"] = expected.pop("entry_price", None)

        # handle actual
        actual = self.get_expand_item_data(tab, trade_object)
        soft_assert(actual, expected, check_contains=True, tolerance=1, tolerance_fields=trade_object.tolerance_fields())

    def verify_item_displayed(self, tab: AssetTabs, order_id: int | str | list, is_display: bool = True) -> None:
        """Verify that an item is displayed or not displayed."""
        order_id = order_id if isinstance(order_id, list) else [order_id]
        self.actions.verify_elements_displayed(
            [cook_element(self.__item_by_order_no, tab.col_locator(), _id) for _id in order_id],
            is_display=is_display, timeout=SHORT_WAIT
        )
