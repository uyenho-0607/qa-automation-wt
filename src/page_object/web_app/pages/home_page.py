import time

from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import SHORT_WAIT, EXPLICIT_WAIT
from src.data.enums import AccSummary
from src.data.ui_messages import UIMessages
from src.page_object.web_app.base_page import BasePage
from src.page_object.web_app.components.modals.feature_anm_modal import FeatureAnnouncementModal
from src.page_object.web_app.components.modals.my_acc_modal import MyAccountModal
from src.page_object.web_app.components.notifications import Notifications
from src.page_object.web_app.components.settings import Settings
from src.page_object.web_app.components.trade.watch_list import WatchList
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element, data_testid
from src.utils.format_utils import format_acc_balance
from src.utils.logging_utils import logger


class HomePage(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)
        self.feature_anm_modal = FeatureAnnouncementModal(actions)
        self.settings = Settings(actions)
        self.notifications = Notifications(actions)
        self.my_account_modal = MyAccountModal(actions)
        self.watch_list = WatchList(actions)

    # ------------------------ LOCATORS ------------------------ #
    __account_selector = (By.CSS_SELECTOR, data_testid("account-selector"))
    __account_type_tag = (By.CSS_SELECTOR, data_testid("account-type-tag"))
    __account_name = (By.CSS_SELECTOR, data_testid('account-name'))
    __account_id = (By.CSS_SELECTOR, data_testid('account-id'))

    __available_balance_dropdown = (By.CSS_SELECTOR, data_testid("available-balance-dropdown"))
    __available_account_amount = (By.CSS_SELECTOR, data_testid('available-balance-amount'))
    __available_balance_title = (By.CSS_SELECTOR, data_testid("available-balance-title"))

    __icon_search = (By.CSS_SELECTOR, data_testid("symbol-search-selector"))
    __txt_symbol_search = (By.CSS_SELECTOR, data_testid('symbol-input-search'))
    __item_search_result = (By.XPATH, "//div[@data-testid='symbol-input-search-items']//div[contains(text(), '{}')]")
    __items_search_result = (By.CSS_SELECTOR, data_testid('symbol-input-search-items'))
    __btn_search_cancel = (By.CSS_SELECTOR, data_testid("symbol-input-search-cancel"))
    __notification_selector = (By.CSS_SELECTOR, data_testid("notification-selector"))

    __search_history = (By.XPATH, "//*[text()='Search History']")
    __btn_delete_search_history = (By.XPATH, "//*[text()='Search History']/following-sibling::*")
    __item_search_history = (By.XPATH, "//div[text()='Search History']/ancestor::div[2]")
    __item_search_history_by_text = (By.XPATH, "//div[text()='Search History']/..//following-sibling::div[contains(normalize-space(), '{}')]")
    __empty_search_result = (By.XPATH, "//*[text()='No items available']")

    # ------------------------ ACTIONS ------------------------ #
    def is_logged_in(self):
        return self.actions.is_element_displayed(self.__account_selector, timeout=EXPLICIT_WAIT)
    
    def open_my_account(self, open=True):
        is_open = self.my_account_modal.is_open()
        if open != is_open:
            self.actions.click(self.__available_balance_dropdown)

    def click_icon_search(self):
        """Click the search icon if it is visible"""
        if self.actions.is_element_displayed(self.__icon_search):
            self.actions.click(self.__icon_search)

    def search_symbol(self, symbol: str):
        """Search symbol"""
        self.click_icon_search()
        self.actions.send_keys(self.__txt_symbol_search, symbol)

    def search_and_select_symbol(self, symbol: str):
        """Search and select the found symbol"""
        self.search_symbol(symbol)
        self.actions.click(cook_element(self.__item_search_result, symbol))

    def delete_search_history(self):
        self.click_icon_search()
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
        texts = [ele.text.strip() for ele in elements]

        for text in texts:
            logger.debug(f"Check {text!r} contains {search_text!r}")
            soft_assert(text, search_text, check_contains=True)

    def verify_empty_search_result(self):
        self.actions.verify_element_displayed(self.__empty_search_result)
        text = self.actions.get_text(self.__empty_search_result)
        if text:
            text.replace(".", "")
        soft_assert(text, UIMessages.NO_ITEM_AVAILABLE)

    def verify_search_history_deleted(self):
        time.sleep(1)
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
