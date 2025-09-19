from typing import Literal

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import SHORT_WAIT
from src.data.enums import AssetTabs, SLTPType
from src.data.objects.trade_obj import ObjTrade
from src.data.project_info import RuntimeConfig
from src.page_object.ios.components.modals.trading_modals import TradingModals
from src.page_object.ios.components.trade.base_trade import BaseTrade
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element
from src.utils.format_utils import locator_format, format_dict_to_string, extract_asset_tab_number
from src.utils.logging_utils import logger


class AssetTab(BaseTrade):
    """
    A class representing the Asset Tab in the trading interface.
    Handles all interactions with the asset tab UI elements and operations.
    """

    def __init__(self, actions: MobileActions):
        super().__init__(actions)
        self.__trade_modals = TradingModals(actions)

    # ------------------------ LOCATORS ------------------------ #
    __tab = (AppiumBy.ACCESSIBILITY_ID, "tab-asset-order-type-{}")  # tab: open, pending, history
    __tab_amount = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeOther[`name == "tab-asset-order-type-{}" AND label CONTAINS "({})"`]')  # tab - exp_amount
    __item_by_id = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`name == "asset-{}-list-item-order-no" AND label CONTAINS "{}"`]')  # tab - orderID
    __order_id_items = (AppiumBy.ACCESSIBILITY_ID, "asset-{}-list-item-order-no")  # tab

    # expand item
    __expand_items = (AppiumBy.ACCESSIBILITY_ID, "asset-{}-list-item-expand")  # tab
    __btn_cancel_expand_item = (AppiumBy.ACCESSIBILITY_ID, "action-sheet-cancel-button")
    __expanded_labels = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`name BEGINSWITH "asset-{}-column-" AND name ENDSWITH "-label"`]')
    __expanded_values = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`name BEGINSWITH "asset-{}-column-" AND name ENDSWITH "-value"`]')
    __expanded_order_type = (AppiumBy.ACCESSIBILITY_ID, "asset-order-type")
    __expanded_symbol = (AppiumBy.ACCESSIBILITY_ID, "asset-detailed-header-symbol")

    # Control buttons locators
    __btn_action = (AppiumBy.ACCESSIBILITY_ID, "asset-{}-button-{}")  # tab: open, pending, history - action: close, edit
    __btn_action_by_id = (
        AppiumBy.IOS_CLASS_CHAIN,
        '**/XCUIElementTypeOther[`name CONTAINS "{}"`]/**/XCUIElementTypeOther[`name == "%s"`]' % __btn_action[1]  # orderID - tab - action
    )
    __txt_close_volume = (AppiumBy.ACCESSIBILITY_ID, "close-order-input-volume")

    # ------------------------ HELPER METHODS ------------------------ #
    def _expand_item(self, tab=None, expand=True):
        if expand:
            self.actions.click(cook_element(self.__expand_items, tab.col_locator()), timeout=SHORT_WAIT)
            logger.debug("- Item expanded")
            return

        self.actions.click(self.__btn_cancel_expand_item)
        logger.debug("- Item closed")

    def wait_for_tab_amount(self, tab: AssetTabs, expected_amount: int) -> None:
        """Wait for the asset tab amount to match the expected amount."""
        self.actions.wait_for_element_visible(cook_element(self.__tab_amount, locator_format(tab), expected_amount))

    def get_tab_amount(self, tab: AssetTabs, wait=True) -> int:
        """Get the number of items in the specified tab."""
        not wait or self.wait_for_spin_loader()
        amount = self.actions.get_text(cook_element(self.__tab, locator_format(tab)))
        return extract_asset_tab_number(amount)

    def get_last_order_id(self, tab: AssetTabs, trade_object: ObjTrade = None, wait=False):
        not wait or self.wait_for_spin_loader()
        order_id = self.actions.get_attribute(cook_element(self.__order_id_items, tab.col_locator()), "label")
        order_id = order_id.split(": ")[-1] if order_id else 0
        logger.debug(f"- Lastest orderID: {order_id!r}")

        if trade_object:
            trade_object.order_id = order_id

        return order_id

    def get_expand_item_data(self, tab: AssetTabs, trade_object: ObjTrade):
        """Get latest data for placed order"""
        # not wait or self.wait_for_spin_loader()
        if trade_object.get("order_id"):
            logger.debug(f"- Wait for order: {trade_object.order_id} display")
            self.actions.wait_for_element_visible(cook_element(self.__item_by_id, tab.col_locator(), trade_object.order_id))

        # expand last item
        self._expand_item(tab)

        # re-assign tab in cased of history - to get correct col locator
        tab = AssetTabs.HISTORY if tab.is_history() else tab

        # get item col name & value
        expand_labels = self.actions.get_text_elements(cook_element(self.__expanded_labels, tab.col_locator()))
        expand_values = self.actions.get_text_elements(cook_element(self.__expanded_values, tab.col_locator()))

        res = {k.lower().replace(" ", "_").replace(".", ""): v for k, v in zip(expand_labels, expand_values)}
        res["order_type"] = self.actions.get_text(self.__expanded_order_type)
        res["symbol"] = self.actions.get_text(self.__expanded_symbol)

        logger.debug(f"Item summary: {format_dict_to_string(res)}")

        # reformat size vs volume column for consistent
        if "size" in res:
            res["volume"] = res.pop("size")

        if tab.is_history() and res.get("volume"):  # todo: improve to check close_volume / x
            res["volume"] = res["volume"].split(" / ")[0]

        # update order_id for trade_object if not present
        trade_object.get("order_id") or trade_object.update(dict(order_id=res.get("order_no", None)))

        # close expanded item
        self._expand_item(expand=False)
        return res

    # ------------------------ ACTIONS ------------------------ #
    def select_tab(self, tab: AssetTabs, wait=False):
        tab_locator = tab
        if tab.is_history():
            if not RuntimeConfig.is_mt4():
                tab_locator = f"{AssetTabs.HISTORY} {AssetTabs.POSITIONS_HISTORY}"
            else:
                tab_locator = AssetTabs.HISTORY

        logger.debug(f"- Select tab: {tab.value.title()!r}")
        self.actions.click(cook_element(self.__tab, locator_format(tab_locator)))
        not wait or self.wait_for_spin_loader()

    def delete_order(self, trade_obj: ObjTrade = None, order_id=None, confirm=True, wait=False):
        ...

    def full_close_order(self):
        ...

    def partial_close_order(self, trade_object: ObjTrade):
        ...

    def _click_action_btn(
            self, order_id=0, tab: AssetTabs = AssetTabs.OPEN_POSITION, action: Literal["edit", "close"] = "edit"
    ):
        locator = cook_element(self.__btn_action, tab.col_locator(), action)
        if order_id:
            locator = cook_element(self.__btn_action_by_id, order_id, tab.col_locator(), action)
        self.actions.click(locator)

    def modify_order(
            self,
            trade_object: ObjTrade,
            sl_type: SLTPType = SLTPType.PRICE,
            tp_type: SLTPType = SLTPType.PRICE,
            confirm=True
    ):
        # Click edit button
        self._click_action_btn(trade_object.order_id, AssetTabs.get_tab(trade_object.order_type))

        # Fill edit order modal
        self.__trade_modals.fill_update_order(trade_object, sl_type, tp_type)

        # Click update order button
        self.__trade_modals.click_update_order_btn()

        # confirm update order
        if confirm:
            self.click_confirm_btn()

    # ------------------------ VERIFY ------------------------ #
    def verify_tab_amount(self, tab: AssetTabs, exp_amount):
        self.wait_for_tab_amount(tab, exp_amount)
        soft_assert(self.get_tab_amount(tab), exp_amount)

    def verify_items_displayed(self, tab: AssetTabs, order_id, is_display=True):
        order_ids = order_id if isinstance(order_id, list) else [order_id]
        locators = [cook_element(self.__item_by_id, tab.col_locator(), _id) for _id in order_ids]
        self.actions.verify_elements_displayed(locators, is_display=is_display)

    def verify_item_data(self, trade_object: ObjTrade, tab: AssetTabs = None, wait=True) -> None:
        """Verify that the item data matches the expected data, only need to input tab in case of history"""
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
