from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import SHORT_WAIT, EXPLICIT_WAIT, LONG_WAIT
from src.data.enums import AccSummary
from src.data.ui_messages import UIMessages
from src.page_object.android.base_screen import BaseScreen
from src.page_object.android.components.modals.feature_anm_modal import FeatureAnnouncementModal
from src.page_object.android.components.modals.my_acc_modal import MyAccountModal
from src.page_object.android.components.notifications import Notifications
from src.page_object.android.components.settings import Settings
from src.page_object.android.components.trade.watch_list import WatchList
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import resource_id, cook_element
from src.utils.format_utils import format_acc_balance
from src.utils.logging_utils import logger


class HomeScreen(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)
        self.feature_anm_modal = FeatureAnnouncementModal(actions)
        self.settings = Settings(actions)
        self.notifications = Notifications(actions)
        self.my_account_modal = MyAccountModal(actions)
        self.watch_list = WatchList(actions)

    # ------------------------ LOCATORS ------------------------ #
    __account_selector = (AppiumBy.XPATH, resource_id("account-selector"))
    __account_type_tag = (AppiumBy.XPATH, resource_id("account-type-tag"))

    __available_balance_dropdown = (AppiumBy.XPATH, resource_id("available-balance-dropdown"))
    __available_account_amount = (AppiumBy.XPATH, resource_id('available-balance-amount'))
    __available_balance_title = (AppiumBy.XPATH, resource_id("available-balance-title"))

    __symbol_search_selector = (AppiumBy.XPATH, resource_id("symbol-search-selector"))
    __txt_symbol_search = (AppiumBy.XPATH, resource_id("symbol-input-search"))
    __item_search_result = (AppiumBy.XPATH, "//*[@resource-id='watchlist-symbol' and @text='{}']")
    __items_search_result = (AppiumBy.XPATH, resource_id('symbol-input-search-items'))
    __search_history = (AppiumBy.XPATH, "//android.widget.TextView[@text='Search History']")
    __btn_delete_search_history = (AppiumBy.XPATH, "//android.widget.TextView[@text='Search History']/following-sibling::android.widget.TextView")
    __btn_search_cancel = (AppiumBy.XPATH, resource_id("symbol-input-search-cancel"))
    __item_search_history = (AppiumBy.XPATH, "//android.view.ViewGroup[2]/android.view.ViewGroup[@content-desc]")
    __item_search_history_by_text = (AppiumBy.XPATH, "//android.view.ViewGroup[2]/android.view.ViewGroup[@content-desc='{}']")
    __notification_selector = (AppiumBy.XPATH, resource_id("notification-selector"))
    __empty_search_result = (AppiumBy.XPATH, "//android.widget.TextView[@text='No items available']")

    # ------------------------ ACTIONS ------------------------ #
    def is_logged_in(self):
        return self.actions.is_element_displayed(self.__account_selector, timeout=LONG_WAIT)

    def open_my_account(self, open=True):
        is_open = self.my_account_modal.is_open()
        if open != is_open:
            self.actions.click(self.__available_balance_dropdown)

    def search_selector(self):
        """Click the search icon if it is visible"""
        if self.actions.is_element_displayed(self.__symbol_search_selector):
            self.actions.click(self.__symbol_search_selector)

    def search_symbol(self, symbol: str):
        """Search symbol"""
        self.search_selector()
        self.actions.send_keys(self.__txt_symbol_search, symbol)
        # self.actions.press_done()

    def search_and_select_symbol(self, symbol: str):
        """Search and select the found symbol"""
        self.search_symbol(symbol)
        self.actions.click(cook_element(self.__item_search_result, symbol))

    def delete_search_history(self):
        self.search_selector()
        self.actions.click(self.__txt_symbol_search)
        if self.actions.is_element_displayed(self.__btn_delete_search_history):
            self.actions.click(self.__btn_delete_search_history)

    def cancel_search(self):
        self.actions.click(self.__btn_search_cancel, raise_exception=False, show_log=False, timeout=SHORT_WAIT)

    # ------------------------ VERIFY ------------------------ #
    def verify_account_info_displayed(self):
        """Verify that account information is displayed"""
        self.actions.verify_element_displayed(self.__account_selector)

    def verify_search_result(self, symbol: str):
        self.actions.verify_element_displayed(cook_element(self.__item_search_result, symbol))

    def verify_wildcard_search_result(self, search_text: str):
        elements = self.actions.find_elements(self.__items_search_result)
        texts = [ele.get_attribute("content-desc").strip() for ele in elements]
        for text in texts:
            logger.debug(f"Check {text!r} contains {search_text!r}")
            soft_assert(text.lower(), search_text.lower(), check_contains=True)

    def verify_empty_search_result(self):
        self.actions.verify_element_displayed(self.__empty_search_result)
        text = self.actions.get_text(self.__empty_search_result)
        if text:
            text.replace(".", "")
        soft_assert(text, UIMessages.NO_ITEM_AVAILABLE)

    def verify_search_history_deleted(self):
        self.actions.verify_element_displayed(self.__item_search_history, is_display=False)
        self.actions.verify_element_displayed(self.__search_history, is_display=False)

    def verify_search_history_items(self, symbols: str | list[str]):
        symbols = symbols if isinstance(symbols, list) else [symbols]
        for symbol in symbols:
            logger.debug(f"Check search history with symbol: {symbol!r} displayed")
            self.actions.verify_element_displayed(cook_element(self.__item_search_history_by_text, symbol))

    # account info
    def verify_available_account(self, exp_dict: dict):
        amount = self.actions.get_text(self.__available_account_amount)
        amount = format_acc_balance(amount)
        soft_assert(amount, exp_dict.get(AccSummary.BALANCE))