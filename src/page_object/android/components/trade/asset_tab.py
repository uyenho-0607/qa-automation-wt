import re
import time
from typing import Dict, Any
from typing import Literal

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import SHORT_WAIT
from src.data.enums import AssetTabs, BulkCloseOpts, SLTPType
from src.data.objects.trade_obj import ObjTrade
from src.data.project_info import RuntimeConfig
from src.page_object.android.components.modals.trading_modals import TradingModals
from src.page_object.android.components.trade.base_trade import BaseTrade
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element
from src.utils.format_utils import locator_format, extract_asset_tab_number, format_dict_to_string
from src.utils.logging_utils import logger
from src.utils.trading_utils import calculate_partial_close


class AssetTab(BaseTrade):
    """
    A class representing the Asset Tab in the trading interface.
    Handles all interactions with the asset tab UI elements and operations.
    """

    def __init__(self, actions: MobileActions):
        super().__init__(actions)
        self.__trade_modals = TradingModals(actions)

    # ------------------------ LOCATORS ------------------------ #
    __tab = (AppiumBy.ID, 'tab-asset-order-type-{}')  # locator_format(tab)
    __tab_amount = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tab-asset-order-type-{}").descriptionContains("({})")')  # locator_format(tab) + amount number

    # Item details locators
    __order_no_items = (AppiumBy.ID, 'asset-{}-list-item-order-no')
    __item_by_order_no = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("asset-{}-list-item-order-no").textContains("{}")')
    __expand_items = (AppiumBy.ID, 'asset-{}-list-item-expand')
    __expand_item_by_order_no = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("{}").fromParent(new UiSelector().resourceId("asset-{}-list-item-expand"))'
    )  # orderID, tab.col_locator
    __btn_cancel_expand_item = (AppiumBy.ID, 'action-sheet-cancel-button')

    # Item expanded data locators
    __expanded_values = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*asset-{}-column.*-value")')
    __expanded_symbol = (AppiumBy.ID, 'asset-detailed-header-symbol')
    __expanded_order_type = (AppiumBy.ID, 'asset-order-type')

    # Control buttons locators
    __btn_action = (AppiumBy.ID, 'asset-{}-button-{}')  # tab.col_locator(), action: close/ edit
    __btn_action_by_id = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("{}").fromParent(new UiSelector().resourceId("asset-{}-button-{}"))'
    )  # orderID, tab.col_locator()

    # Bulk operations locators
    __btn_bulk_close = (AppiumBy.ID, 'bulk-close')
    __opt_bulk_close = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("{}")')
    __btn_bulk_delete = (AppiumBy.ID, 'bulk-delete')

    # Close order confirmation locators
    __txt_close_order = (AppiumBy.ID, 'close-order-input-volume')

    # ------------------------ HELPER METHODS ------------------------ #
    def _get_item_info(self, get_info: Literal["profit_loss", "current_price", "volume"] = "current_price"):
        """Get the outside displaying values (volume, profit/loss, current price)"""
        text = self.actions.get_content_desc(cook_element(self.__expand_items, AssetTabs.OPEN_POSITION.col_locator())).lower()
        pattern = r'(volume|profit/loss|current price),\s*([-+]?\d*\.?\d+)'
        matches = re.findall(pattern, text)
        res_dict = {k: float(v) for k, v in matches}

        return res_dict.get(get_info, 0)

    def get_profit_loss(self):
        return self._get_item_info("profit_loss")

    def get_tab_amount(self, tab: AssetTabs, wait=True) -> int:
        """Get the number of items in the specified tab."""
        not wait or self.wait_for_spin_loader()
        amount = self.actions.get_content_desc(cook_element(self.__tab, locator_format(tab)))
        return extract_asset_tab_number(amount)

    def get_last_order_id(self, tab: AssetTabs, wait=True) -> int:
        """Get the latest order ID from the specified tab."""
        not wait or self.wait_for_spin_loader()
        res = self.actions.get_text(cook_element(self.__order_no_items, tab.col_locator()))
        order_id = res.split(": ")[-1] if res else 0
        logger.debug(f"- Latest order_id: {order_id!r}")
        return order_id

    def get_expand_item_data(self, tab: AssetTabs, trade_object: ObjTrade) -> Dict[str, Any]:
        """Get detailed data for an expanded item in the specified tab."""
        # expand the item
        expand_item = cook_element(self.__expand_items, tab.col_locator())  # last item
        if trade_object.get("order_id"):
            expand_item = cook_element(self.__expand_item_by_order_no, trade_object.order_id, tab.col_locator())

        self.actions.click(expand_item)
        logger.debug("- Item expanded, getting item data...")

        # re-assign tab in case of history - to get correct col locator
        tab = AssetTabs.HISTORY if tab.is_history() else tab

        res = {
            ele.get_attribute("resource-id").split("-column-")[-1].replace("-value", "").replace("-", "_"): ele.text.strip()
            for ele in self.actions.find_elements(cook_element(self.__expanded_values, tab.col_locator()))
        }
        # get order-type and symbol
        res["order_type"] = self.actions.get_text(self.__expanded_order_type)
        res["symbol"] = self.actions.get_text(self.__expanded_symbol)

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

        logger.debug(f"- Select tab: {tab.value.title()!r}")
        self.actions.click(cook_element(self.__tab, locator_format(tab_locator)))
        not wait or self.wait_for_spin_loader()

    def wait_for_tab_amount(self, tab: AssetTabs, expected_amount: int) -> None:
        """Wait for the asset tab amount to match the expected amount."""
        self.actions.wait_for_element_visible(
            cook_element(self.__tab_amount, locator_format(tab), expected_amount)
        )

    def _click_action_btn(
            self, order_id=0, tab: AssetTabs = AssetTabs.OPEN_POSITION, action: Literal["edit", "close"] = "edit"
    ):
        locator = cook_element(self.__btn_action, tab.col_locator(), action)
        if order_id:
            locator = cook_element(self.__btn_action_by_id, order_id, tab.col_locator(), action)
        self.actions.click(locator)

    def delete_order(self, trade_object, confirm=True):
        if not trade_object.get("order_id"):
            trade_object.order_id = self.get_last_order_id(AssetTabs.PENDING_ORDER)

        logger.debug(f"- Delete order with ID: {trade_object.order_id!r}")
        self._click_action_btn(trade_object.order_id, AssetTabs.PENDING_ORDER, "close")  # close == delete in pending orders tab
        if confirm:
            self.__trade_modals.confirm_delete_order()

    def bulk_delete_orders(self) -> None:
        """Delete multiple pending orders at once."""
        time.sleep(1)
        self.actions.click(self.__btn_bulk_delete)
        self.click_confirm_btn()

    def full_close_position(self, order_id, confirm=True):
        logger.debug(f"- Close order with ID: {order_id!r}")
        self._click_action_btn(order_id, AssetTabs.OPEN_POSITION, "close")

        if confirm:
            self.__trade_modals.confirm_close_order()

    def partial_close_position(self, close_obj: ObjTrade, volume=0, confirm=True, wait=False):
        """Partially close a position."""
        new_created_obj = ObjTrade(**{k: v for k, v in close_obj.items() if k != "order_id"})
        if not close_obj.get("order_id"):
            close_obj.order_id = self.get_last_order_id(AssetTabs.OPEN_POSITION)  # update order_id for trade_object

        close_obj.current_price = self.get_current_price()  # update close price

        logger.debug(f'- Close order with ID: {close_obj.order_id!r}')
        self._click_action_btn(close_obj.get("order_id", 0), AssetTabs.OPEN_POSITION, "close")

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
        logger.debug(f"> Close volume: {close_volume!r}")
        self.actions.send_keys(self.__txt_close_order, close_volume)

        if confirm:
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
    ):
        """
        Modify stop loss/ take profit/ fill policy/ Expiry
        trade_object: should contain trade_type and order_type
        sl_type: Price or Points
        tp_type: Price or Points
        """
        # click action button
        self._click_action_btn(trade_object.get("order_id"), AssetTabs.get_tab(trade_object.order_type), "edit")

        # fill update order modal
        self.__trade_modals.fill_update_order(trade_object, sl_type, tp_type)

        # click update order button
        self.__trade_modals.click_update_order_btn()

        # confirm update order
        not confirm or self.__trade_modals.confirm_update_order()

    # ------------------------ VERIFY ------------------------ #
    def verify_tab_amount(self, tab: AssetTabs, expected_amount: int) -> None:
        """Verify that the tab amount matches the expected amount."""
        self.actions.verify_element_displayed(cook_element(self.__tab_amount, locator_format(tab), expected_amount))

    def verify_item_data(self, trade_object: ObjTrade, tab: AssetTabs = None, wait=False) -> None:
        """Verify that the item data matches the expected data."""
        not wait or self.wait_for_spin_loader()
        tab = tab or AssetTabs.get_tab(trade_object.order_type)
        # handle expected
        expected = trade_object.asset_item_data(tab)

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
