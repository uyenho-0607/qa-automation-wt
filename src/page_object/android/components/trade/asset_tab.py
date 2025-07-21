import time
from typing import Optional, Dict, Any

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import SHORT_WAIT
from src.data.enums import AssetTabs, BulkCloseOpts
from src.data.objects.trade_obj import ObjTrade
from src.data.project_info import ProjectConfig
from src.page_object.android.components.trade.base_trade import BaseTrade
from src.utils import DotDict
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import resource_id, cook_element
from src.utils.format_utils import locator_format, extract_asset_tab_number, format_dict_to_string, \
    format_str_price
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
    __item_by_order_no = (
        AppiumBy.XPATH,
        "//*[@resource-id='asset-{}-list-item-order-no' and contains(@text(), '{}')]/parent::android.view.ViewGroup"
    )
    __expand_item = (AppiumBy.XPATH, resource_id('asset-{}-list-item-expand'))
    __expand_item_by_order_no = (
        AppiumBy.XPATH,
        "//*[contains(@text, '{}')]/following-sibling::*[@resource-id='asset-{}-list-item-expand']"
    )
    __btn_cancel_expand_item = (AppiumBy.XPATH, resource_id('action-sheet-cancel-button'))

    # Item expanded data locators
    __item_symbol = (AppiumBy.XPATH, resource_id('asset-detailed-header-symbol'))
    __item_order_type = (AppiumBy.XPATH, resource_id('asset-order-type'))
    __item_order_id = (AppiumBy.XPATH, resource_id('asset-{}-column-order-id-value'))
    __item_volume_value = (
        AppiumBy.XPATH,
        "//*[@resource-id='asset-{}-column-volume-value' or @resource-id='asset-{}-column-size-value']"
    )
    __item_units_value = (AppiumBy.XPATH, resource_id('asset-{}-column-units-value'))
    __item_entry_price = (AppiumBy.XPATH, resource_id('asset-{}-column-entry-price-value'))
    __item_stop_limit_price = (AppiumBy.XPATH, resource_id('asset-{}-column-pending-price-value'))
    __item_profit = (AppiumBy.XPATH, resource_id('asset-{}-column-profit-value'))
    __item_take_profit = (AppiumBy.XPATH, resource_id('asset-{}-column-take-profit-value'))
    __item_stop_loss = (AppiumBy.XPATH, resource_id('asset-{}-column-stop-loss-value'))
    __item_expiry = (AppiumBy.XPATH, resource_id('asset-{}-column-expiry-value'))
    __item_remarks = (AppiumBy.XPATH, resource_id('asset-{}-column-remarks-value'))

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
    __bulk_close = (AppiumBy.XPATH, resource_id('bulk-close'))
    __opt_bulk_close = (AppiumBy.XPATH, "//*[@content-desc='{}']")
    __bulk_delete = (AppiumBy.XPATH, resource_id('bulk-delete'))

    # Close order confirmation locators
    __txt_close_order = (AppiumBy.XPATH, resource_id('close-order-input-volume'))

    # ------------------------ HELPER METHODS ------------------------ #
    def get_tab_amount(self, tab: AssetTabs) -> int:
        """Get the number of items in the specified tab."""
        time.sleep(2)
        amount = self.actions.get_content_desc(cook_element(self.__tab, locator_format(tab)))
        return extract_asset_tab_number(amount)

    def get_last_order_id(self, tab: AssetTabs | str, trade_object: Optional[DotDict] = None) -> str:
        """Get the latest order ID from the specified tab and update value into trade_object"""
        self.select_tab(tab)

        order_id = 0
        res = self.actions.get_text(cook_element(self.__item_order_no, tab.get_col()))
        if res:
            order_id = res.split(": ")[-1]
        if trade_object is not None:
            trade_object.update({"order_id": order_id})

        return order_id

    def get_expand_item_data(
            self, tab: AssetTabs, order_id: int = 0, trade_object: Optional[DotDict] = None
    ) -> Dict[str, Any]:
        """Get detailed data for an expanded item in the specified tab."""
        self.select_tab(tab)
        self._expand_item(tab, order_id=order_id or (trade_object or {}).get("order_id", 0))

        # Define column configurations
        col_config = {
            "general": {
                "symbol": self.__item_symbol,
                "order_id": self.__item_order_id,
                "order_type": self.__item_order_type,
                "volume": cook_element(self.__item_volume_value, tab.get_col()),
                "units": self.__item_units_value,
                "entry_price": self.__item_entry_price,
                "take_profit": self.__item_take_profit,
                "stop_loss": self.__item_stop_loss
            },
            "tab_specific": {
                AssetTabs.OPEN_POSITION: {"profit": self.__item_take_profit},
                AssetTabs.PENDING_ORDER: {
                    "stop_limit_price": self.__item_stop_limit_price if ProjectConfig.is_non_oms() else None,
                    "expiry": self.__item_expiry,
                }
            }
        }

        # Combine base and tab-specific columns
        columns = col_config["general"] | col_config["tab_specific"].get(tab, {})

        if "history" in tab.lower():
            tab = AssetTabs.HISTORY
            columns["remarks"] = self.__item_expiry

        # Get value and update into result dict, except None locator
        res = {
            key: self.actions.get_text(cook_element(value, tab.get_col()), timeout=SHORT_WAIT)
            for key, value in columns.items() if value
        }

        # Adjust special values
        res["volume"] = res["volume"].split(" /")[0]
        # res["stop_loss"] = format_str_price(res["stop_loss"])
        # res["take_profit"] = format_str_price(res["take_profit"])

        logger.debug(f"Item summary: {format_dict_to_string(res)}")
        # Load data into trade_object
        if trade_object is not None:
            trade_object.update(res)

        # close item expand
        self.actions.click(self.__btn_cancel_expand_item)
        return res

    def _expand_item(self, tab: AssetTabs, order_id: int = 0) -> None:
        """Expand an item in the specified tab."""
        locator = cook_element(self.__expand_item, tab.get_col())
        if order_id:
            locator = cook_element(self.__expand_item_by_order_no, order_id, tab.get_col())

        self.actions.click(locator)

    # ------------------------ ACTIONS ------------------------ #
    def select_tab(self, tab: AssetTabs) -> None:
        """Select the specified asset tab."""
        if tab.is_sub_history():
            if not ProjectConfig.is_non_oms():
                self.actions.click(cook_element(self.__tab, locator_format(AssetTabs.HISTORY)))
                return

            # click sub history tab
            self.actions.click(cook_element(self.__tab, locator_format(f"{AssetTabs.HISTORY} {tab}")))
            return

        self.actions.click(cook_element(self.__tab, locator_format(tab)))

    def wait_for_tab_amount(self, tab: AssetTabs, expected_amount: int) -> None:
        """Wait for the asset tab amount to match the expected amount."""
        self.actions.wait_for_element_visible(
            cook_element(self.__tab_amount, locator_format(tab), expected_amount)
        )

    def click_edit_button(self, tab: AssetTabs, order_id: int = 0) -> None:
        """Click the edit button for an item in the specified tab."""
        self.select_tab(tab)
        # edit last item by default
        locator = cook_element(self.__btn_edit, tab.get_col())
        if order_id:
            # edit item with specific order_id
            locator = cook_element(self.__btn_edit_by_id, tab.get_col(), order_id, tab.get_col())
        self.actions.click(locator)

    def click_close_button(self, tab: AssetTabs = AssetTabs.OPEN_POSITION) -> None:
        """Click the close button last item in the specified tab."""
        self.select_tab(tab)
        self.actions.click(cook_element(self.__btn_close_delete, tab.get_col()))

    click_delete_button = click_close_button

    def delete_pending_order(self, order_id: int = 0, trade_object: Optional[DotDict] = None, confirm=True) -> None:
        """Delete a pending order by ID or the last order if no ID provided."""
        if order_id:
            self.actions.click(
                cook_element(self.__btn_close_by_order_no, AssetTabs.PENDING_ORDER.get_col(), order_id)
            )
        else:
            # delete last item
            # load last order_id into trade_object
            self.get_last_order_id(AssetTabs.PENDING_ORDER, trade_object)
            self.actions.click(cook_element(self.__btn_close_delete, AssetTabs.PENDING_ORDER.get_col()))
        if confirm:
            self.confirm_close_order()

    def bulk_delete_orders(self) -> None:
        """Delete multiple pending orders at once."""
        self.select_tab(AssetTabs.PENDING_ORDER)
        self.actions.click(self.__bulk_delete)
        self.click_confirm_btn()

    def full_close_position(self, order_id: int = 0, confirm=True) -> None:
        if order_id:
            # close position by order_id
            self.actions.click(cook_element(
                self.__btn_close_by_order_no, AssetTabs.OPEN_POSITION.get_col(), order_id, AssetTabs.OPEN_POSITION.get_col()
            ))
        else:
            # close latest position
            self.click_close_button()

        not confirm or self.confirm_close_order()

    def partial_close_position(self, order_id=0, trade_object=None, volume=0, confirm=True):
        if not ProjectConfig.is_non_oms():
            trade_object.pop("order_id", None)

        order_id = order_id or trade_object.get("order_id", 0)
        if order_id:
            # close position by order_id
            self.actions.click(cook_element(
                self.__btn_close_by_order_no, AssetTabs.OPEN_POSITION.get_col(), order_id, AssetTabs.OPEN_POSITION.get_col()
            ))
        else:
            # close latest position
            self.click_close_button()

        if volume:
            close_volume = volume
            if trade_object:
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
        if confirm:
            self.confirm_close_order()

    def bulk_close_positions(self, option: BulkCloseOpts = BulkCloseOpts.ALL) -> None:
        """Close multiple positions at once using the specified option."""
        self.select_tab(AssetTabs.OPEN_POSITION)
        self.actions.click(self.__bulk_close)

        options = {
            BulkCloseOpts.ALL: "All Positions",
            BulkCloseOpts.PROFIT: "Profitable Positions",
            BulkCloseOpts.LOSS: "Losing Positions",
        }

        self.actions.click(cook_element(self.__opt_bulk_close, options[option]))
        self.click_confirm_btn()

    # ------------------------ VERIFY ------------------------ #
    def verify_tab_amount(self, tab: AssetTabs, expected_amount: int) -> None:
        """Verify that the tab amount matches the expected amount."""
        self.wait_for_tab_amount(tab, expected_amount)
        soft_assert(self.get_tab_amount(tab), expected_amount)

    def verify_item_data(self, trade_object: ObjTrade, tab: AssetTabs = None) -> None:
        """Verify that the item data matches the expected data."""
        tab = tab or AssetTabs.get_tab(trade_object.order_type)
        expected = trade_object.asset_item_data(tab)

        item_data = self.get_expand_item_data(tab, order_id=trade_object.get("order_id", 0))
        actual = {k: v for k, v in item_data.items() if k in expected}

        # update order_id for trade_object if not yet
        trade_object.get("order_id") or trade_object.update(dict(order_id=item_data.pop("order_id")))

        soft_assert(actual, expected, tolerance=0.1, tolerance_fields=trade_object.tolerance_fields())

    def verify_item_displayed(self, tab: AssetTabs, order_id: int | str | list, is_display: bool = True) -> None:
        """Verify that an item is displayed or not displayed."""
        self.select_tab(tab)
        order_id = order_id if isinstance(order_id, list) else [order_id]
        self.actions.verify_elements_displayed(
            [cook_element(self.__item_by_order_no, tab.get_col(), _id) for _id in order_id],
            is_display=is_display, timeout=SHORT_WAIT
        )
        # for _id in order_id:
        #     self.actions.verify_element_displayed(
        #         cook_element(self.__item_by_order_no, tab.get_col(), _id),
        #         is_display=is_display
        #     )
