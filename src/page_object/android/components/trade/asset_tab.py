import time
from typing import Dict, Any

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import SHORT_WAIT
from src.data.enums import AssetTabs, BulkCloseOpts
from src.data.objects.trade_obj import ObjTrade
from src.data.project_info import RuntimeConfig
from src.page_object.android.components.trade.base_trade import BaseTrade
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import resource_id, cook_element
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

    # ------------------------ LOCATORS ------------------------ #
    __tab = (AppiumBy.XPATH, resource_id('tab-asset-order-type-{}'))
    __tab_amount = (AppiumBy.XPATH, "//*[@resource-id='tab-asset-order-type-{}' and contains(@content-desc, '({})')]")

    # Item details locators
    __item_order_no = (AppiumBy.XPATH, resource_id('asset-{}-list-item-order-no'))
    __item_by_order_no = (AppiumBy.XPATH, "//*[@resource-id='asset-{}-list-item-order-no' and contains(@text, '{}')]")
    __expand_item = (AppiumBy.XPATH, resource_id('asset-{}-list-item-expand'))
    __expand_item_by_order_no = (
        AppiumBy.XPATH,
        "//*[contains(@text, '{}')]/following-sibling::*[@resource-id='asset-{}-list-item-expand']"
    )
    __btn_cancel_expand_item = (AppiumBy.XPATH, resource_id('action-sheet-cancel-button'))

    # Item expanded data locators
    __expand_items = (AppiumBy.XPATH, "//*[contains(@resource-id, 'asset-{}-column') and contains(@resource-id, '-value')]")
    __item_symbol = (AppiumBy.XPATH, resource_id('asset-detailed-header-symbol'))
    __item_order_type = (AppiumBy.XPATH, resource_id('asset-order-type'))

    # Control buttons locators
    __btn_edit = (AppiumBy.XPATH, resource_id('asset-{}-button-edit'))
    __btn_edit_by_id = (
        AppiumBy.XPATH,
        "//*[@resource-id='asset-{}-list-item-order-no' and contains(@text, '{}')]"
        "/preceding-sibling::*[@resource-id='asset-{}-button-edit']"
    )
    __btn_close_delete = (AppiumBy.XPATH, resource_id('asset-{}-button-close'))
    __btn_close_by_order_no = (
        AppiumBy.XPATH,
        "//*[@resource-id='asset-{}-list-item-order-no' and contains(@text, '{}')]"
        "/preceding-sibling::*[@resource-id='asset-{}-button-close']"
    )

    # Bulk operations locators
    __btn_bulk_close = (AppiumBy.XPATH, resource_id('bulk-close'))
    __opt_bulk_close = (AppiumBy.XPATH, "//*[@content-desc='{}']")
    __btn_bulk_delete = (AppiumBy.XPATH, resource_id('bulk-delete'))

    # Close order confirmation locators
    __txt_close_order = (AppiumBy.XPATH, resource_id('close-order-input-volume'))

    # ------------------------ HELPER METHODS ------------------------ #
    def get_tab_amount(self, tab: AssetTabs) -> int:
        """Get the number of items in the specified tab."""
        time.sleep(2)
        amount = self.actions.get_content_desc(cook_element(self.__tab, locator_format(tab)))
        return extract_asset_tab_number(amount)

    def get_last_order_id(self, trade_object: ObjTrade) -> None:
        """Get the latest order ID from the specified tab and update value into trade_object"""
        self.wait_for_spin_loader()
        res = self.actions.get_text(cook_element(self.__item_order_no, AssetTabs.get_tab(trade_object.order_type).col_locator()))
        trade_object.order_id = res.split(": ")[-1] if res else 0

    def get_expand_item_data(self, tab: AssetTabs, order_id: int = 0) -> Dict[str, Any]:
        """Get detailed data for an expanded item in the specified tab."""
        # expand the item
        locator = cook_element(self.__expand_item_by_order_no, order_id, tab.col_locator()) if order_id else cook_element(self.__expand_item, tab.col_locator())
        self.actions.click(locator)

        # get expanded item details 
        tab = AssetTabs.HISTORY if tab.is_history() else tab
        res = {
            ele.get_attribute("resource-id").split("-column-")[-1].replace("-value", "").replace("-", "_"): ele.text.strip()
            for ele in self.actions.find_elements(cook_element(self.__expand_items, tab.col_locator()))
        }
        # get order-type
        res["order_type"] = self.actions.get_text(self.__item_order_type)

        # reformat size vs volume column for consistent
        if "size" in res:
            res["volume"] = res.pop("size")
            # todo: improve to check close_volume / x
            if tab.is_history():
                res["volume"] = res["volume"].split(" / ")[0]

        logger.debug(f"Item summary: {format_dict_to_string(res)}")

        # close item expand
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

    def click_edit_button(self, tab: AssetTabs, order_id: int = 0) -> None:
        """Click the edit button for an item in the specified tab."""
        # edit last item by default
        locator = cook_element(self.__btn_edit, tab.col_locator())
        if order_id:
            # edit item with specific order_id
            locator = cook_element(self.__btn_edit_by_id, tab.col_locator(), order_id, tab.col_locator())
        self.actions.click(locator)

    def click_close_button(self, tab: AssetTabs = AssetTabs.OPEN_POSITION) -> None:
        """Click the close button last item in the specified tab."""
        self.actions.click(cook_element(self.__btn_close_delete, tab.col_locator()))

    click_delete_button = click_close_button

    def delete_order(self, order_id: int = 0, trade_object: ObjTrade = None, confirm=True) -> None:
        """Delete a pending order by ID or the last order if no ID provided."""
        tab_col = AssetTabs.PENDING_ORDER.col_locator()
        if not order_id and trade_object:
            self.get_last_order_id(trade_object)  # load order_id for trade object if provided

        locator = cook_element(self.__btn_close_by_order_no if order_id else self.__btn_close_delete, tab_col, order_id, tab_col)
        self.actions.click(locator)
        not confirm or self.confirm_delete_order()

    def bulk_delete_orders(self) -> None:
        """Delete multiple pending orders at once."""
        self.actions.click(self.__btn_bulk_delete)
        self.click_confirm_btn()

    def full_close_position(self, order_id: int = 0, confirm=True) -> None:
        locator = cook_element(self.__btn_close_by_order_no if order_id else self.__btn_close_delete, AssetTabs.OPEN_POSITION.col_locator(), order_id, AssetTabs.OPEN_POSITION.col_locator())
        self.actions.click(locator)
        not confirm or self.confirm_close_order()

    def partial_close_position(self, trade_object: ObjTrade, order_id=0, confirm=True):

        tab_col = AssetTabs.OPEN_POSITION.col_locator()
        order_id = order_id or trade_object.get("order_id", 0) if trade_object else 0
        locator = cook_element(self.__btn_close_by_order_no if order_id else self.__btn_close_delete, tab_col, order_id, tab_col)
        self.actions.click(locator)

        # random closed volume value
        values = calculate_partial_close(trade_object)
        close_volume = values.close_volume

        logger.debug(f"- Close volume: {close_volume!r} / {trade_object.volume}")

        if trade_object:
            trade_object |= {
                "volume": values.left_volume,
                "close_volume": close_volume,
                "units": values.left_units,
                "close_units": values.close_units
            }

        self.actions.send_keys(self.__txt_close_order, close_volume)
        not confirm or self.confirm_close_order()

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

    # ------------------------ VERIFY ------------------------ #
    def verify_tab_amount(self, tab: AssetTabs, expected_amount: int) -> None:
        """Verify that the tab amount matches the expected amount."""
        self.wait_for_tab_amount(tab, expected_amount)
        soft_assert(self.get_tab_amount(tab), expected_amount)

    def verify_item_data(self, trade_object: ObjTrade, tab: AssetTabs = None, wait=False) -> None:
        """Verify that the item data matches the expected data."""
        not wait or self.wait_for_spin_loader()
        tab = tab or AssetTabs.get_tab(trade_object.order_type)
        expected = trade_object.asset_item_data(tab)

        item_data = self.get_expand_item_data(tab, order_id=trade_object.get("order_id", 0))
        actual = {k: v for k, v in item_data.items() if k in expected}

        # update order_id for trade_object if not yet
        trade_object.get("order_id") or trade_object.update(dict(order_id=item_data.pop("order_id")))

        soft_assert(actual, expected, tolerance=1, tolerance_fields=trade_object.tolerance_fields())

    def verify_item_displayed(self, tab: AssetTabs, order_id: int | str | list, is_display: bool = True) -> None:
        """Verify that an item is displayed or not displayed."""
        order_id = order_id if isinstance(order_id, list) else [order_id]
        self.actions.verify_elements_displayed(
            [cook_element(self.__item_by_order_no, tab.col_locator(), _id) for _id in order_id],
            is_display=is_display, timeout=SHORT_WAIT
        )
