import time

from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import QUICK_WAIT, SHORT_WAIT
from src.data.enums import Features, URLPaths
from src.data.enums.home import AccSummary
from src.data.ui_messages import UIMessages
from src.page_object.web.base_page import BasePage
from src.page_object.web.components.modals.feature_announcement_modal import FeatureAnnouncementModal
from src.page_object.web.components.notifications import Notifications
from src.page_object.web.components.settings import Settings
from src.utils.assert_utils import soft_assert, compare_with_tolerance
from src.utils.common_utils import data_testid, cook_element
from src.utils.format_utils import remove_comma, format_acc_balance
from src.utils.logging_utils import logger


class HomePage(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)
        self.notifications = Notifications(actions)
        self.settings = Settings(actions)
        self.feature_announcement_modal = FeatureAnnouncementModal(actions)

    # ------------------------ LOCATORS ------------------------ #
    # Top Bar Elements
    __account_selector = (By.CSS_SELECTOR, data_testid('account-selector'))
    __account_name = (By.CSS_SELECTOR, data_testid('account-name'))
    __account_id = (By.CSS_SELECTOR, data_testid('account-id'))
    __account_type = (By.CSS_SELECTOR, data_testid('account-type-tag'))
    __account_details = (By.CSS_SELECTOR, data_testid('account-detail'))

    __drp_account_type = (By.CSS_SELECTOR, "div[data-testid='account-option-item'] span[data-testid='account-type-tag']")
    __drp_account_name = (By.CSS_SELECTOR, data_testid('account-option-name'))
    __drp_account_details = (By.CSS_SELECTOR, data_testid('account-option-detail'))

    __acc_balance_items = (By.XPATH, "//div[text()='{}']/following-sibling::div/div")
    __acc_note_items = (By.XPATH, "//div[text()='{}']/following-sibling::div")
    __chb_acc_summary = (By.XPATH, "//div[text()='{}']/following-sibling::div[2]")

    __account_balance_item = (By.XPATH, "//*[@data-testid='account-option-balance']/span[1]")
    __total_account_balance = (By.CSS_SELECTOR, data_testid('account-total-balance'))

    __txt_symbol_search = (By.CSS_SELECTOR, data_testid('symbol-input-search'))
    __search_history = (By.CSS_SELECTOR, data_testid('symbol-input-search-history'))
    __btn_delete_search_history = (By.CSS_SELECTOR, data_testid('symbol-input-search-history-delete'))
    __item_search_history = (By.CSS_SELECTOR, data_testid('symbol-input-search-items-symbol'))
    __item_search_history_by_text = (By.XPATH, "//*[@data-testid='symbol-input-search-items-symbol' and text()='{}']")

    __item_search_result = (By.XPATH, "//div[@data-testid='symbol-input-search-items']//div[text()='{}']")
    __items_search_result = (By.CSS_SELECTOR, data_testid('symbol-input-search-items'))
    __empty_message = (By.CSS_SELECTOR, "div[data-testid='symbol-dropdown-result'] > div[data-testid='empty-message']")
    # Side Bar Elements
    __side_bar_option = (By.CSS_SELECTOR, data_testid('side-bar-option-{}'))

    # ------------------------ ACTIONS ------------------------ #
    def toggle_account_selector(self, open=True):
        is_open = self.actions.is_element_displayed(self.__account_balance_item)
        if open != is_open:
            self.actions.click(self.__account_selector)

    def toggle_balance_summary(self, open=True):
        is_open = self.actions.is_element_displayed(cook_element(self.__acc_note_items, AccSummary.MARGIN_CALL))
        if open != is_open:
            self.actions.click_by_offset(self.__account_name, -100, 5)

    def is_account_traded(self):
        """Check if account did any trades"""
        res = self.actions.is_element_displayed(cook_element(self.__acc_balance_items, AccSummary.MARGIN_LEVEL))
        return res

    def check_uncheck_balance_items(self, account_item: AccSummary | list[AccSummary], check=True):
        self.toggle_balance_summary()
        account_item = account_item if isinstance(account_item, list) else [account_item]

        for item in account_item:
            logger.debug(f"{'Check' if check else 'Uncheck'} {item} balance summary")
            locator = cook_element(self.__chb_acc_summary, item)
            is_checked = " checked" in self.actions.get_attribute(locator, "class")

            if is_checked != check:
                self.actions.click(locator)

        self.toggle_balance_summary(open=False)

    # Navigation Actions
    def navigate_to(self, feature: Features, wait=False):
        """Navigate to a specific feature using the sidebar"""
        self.actions.click(cook_element(self.__side_bar_option, feature.lower()))
        not wait or self.wait_for_spin_loader()

    def clear_search_field(self):
        self.actions.clear_field(self.__txt_symbol_search)

    def search_symbol(self, symbol: str):
        self.clear_search_field()
        self.actions.send_keys(self.__txt_symbol_search, symbol)

    def select_item_from_search_result(self, symbol: str):
        self.actions.click(cook_element(self.__item_search_result, symbol))
        time.sleep(1)

    def search_and_select_symbol(self, symbol):
        self.search_symbol(symbol)
        self.select_item_from_search_result(symbol)

    def delete_search_history(self, check_displayed=True):
        self.actions.click(self.__txt_symbol_search)
        if check_displayed:
            self.actions.click_if_displayed(self.__btn_delete_search_history)
            return
        self.actions.click(self.__btn_delete_search_history)

    # ------------------------ VERIFY ------------------------ #
    def verify_page_url(self):
        super().verify_page_url(URLPaths.TRADE)

    def verify_acc_info_displayed(self):
        """Verify that account information is displayed"""
        self.actions.verify_element_displayed(self.__account_selector)
        self.actions.verify_element_displayed(self.__account_name)
        self.actions.verify_element_displayed(self.__account_id)

    def verify_account_details(self, exp_data):
        actual = {
            "name": self.actions.get_text(self.__account_name),
            "id": self.actions.get_text(self.__account_id),
            "type": self.actions.get_text(self.__account_type),
            "details": self.actions.get_text(self.__account_details)
        }

        expected = {
            "name": exp_data["name"],
            "id": exp_data["id"],
            "type": exp_data["type"],
            "details": f"{exp_data['currency']} | 1:{exp_data['leverage']}"
        }

        soft_assert(actual, expected)

    def verify_account_dropdown_details(self, exp_data):
        actual = {
            "name": self.actions.get_text(self.__drp_account_name),
            "id": self.actions.get_text(self.__drp_account_details),
            "type": self.actions.get_text(self.__drp_account_type)
        }
        expected = {
            "name": exp_data["name"],
            "id": f"{exp_data['id']} (1:{exp_data['leverage']})",
            "type": exp_data["type"]
        }
        soft_assert(actual, expected)

    def verify_acc_balance_items_displayed(self, account_item: AccSummary | list[AccSummary], is_display=True):
        account_item = account_item if isinstance(account_item, list) else [account_item]
        locators = [cook_element(self.__acc_balance_items, item) for item in account_item]
        self.actions.verify_elements_displayed(locators, is_display=is_display, timeout=SHORT_WAIT if len(locators) > 1 else QUICK_WAIT)

    def verify_acc_total_balance(self):
        balance_items = self.actions.find_elements(self.__account_balance_item)
        sum_balance = sum(
            [remove_comma(element.text.strip()) for element in balance_items]
        )
        total_balance = self.actions.get_text(self.__total_account_balance)
        soft_assert(sum_balance, remove_comma(total_balance.replace("USD", "")))

    def verify_acc_balance_value(self, exp_dict: dict):
        """Verify account summary item against exp_dict (should be response from API get account)"""
        actual = {key: format_acc_balance(self.actions.get_text(cook_element(self.__acc_balance_items, key))) for key in AccSummary.checkbox_list()}
        expected = {k: round(v, 2) for k, v in exp_dict.items() if k in AccSummary.checkbox_list()}
        soft_assert(actual, expected, tolerance=0.05, tolerance_fields=AccSummary.list_values(except_val=AccSummary.BALANCE))

    def verify_acc_note_values(self, exp_dict: dict):
        actual = {item: format_acc_balance(self.actions.get_text(cook_element(self.__acc_note_items, item))) for item in AccSummary.note_list()}
        soft_assert(actual, {k: v for k, v in exp_dict.items() if k in AccSummary.note_list()})

    def verify_acc_summary_dropdown(self):
        element_dict = {}

        for item in AccSummary.checkbox_list():
            element_dict[item] = self.actions.find_elements(cook_element(self.__acc_balance_items, item))

        logger.debug("- Checking enough account items are found")
        for item in AccSummary.checkbox_list():
            soft_assert(len(element_dict[item]), 2, error_message=f"Not enough values to compare, actual {len(element_dict[item])}, expected: 2")

        logger.debug("- Checking account details")
        expected = {item: format_acc_balance(element_dict[item][0].text) for item in AccSummary.checkbox_list()}
        actual = {item: format_acc_balance(element_dict[item][-1].text) for item in AccSummary.checkbox_list()}
        soft_assert(actual, expected, tolerance=0.1, tolerance_fields=AccSummary.list_values(except_val=AccSummary.BALANCE))

    def verify_search_result(self, symbol: str):
        self.actions.verify_element_displayed(cook_element(self.__item_search_result, symbol))

    def verify_wildcard_search_result(self, search_text: str):
        elements = self.actions.find_elements(self.__items_search_result)
        texts = [ele.text.strip() for ele in elements]

        for text in texts:
            logger.debug(f"Check {text!r} contains {search_text!r}")
            soft_assert(text, search_text, check_contains=True)

    def verify_not_found_search_message(self):
        self.verify_empty_message(expected_text=UIMessages.NO_ITEM_AVAILABLE)

    def verify_search_history_empty_message(self):
        self.verify_empty_message(self.__empty_message, UIMessages.TYPE_SOMETHING_TO_SEARCH)

    def verify_search_result_deleted(self):
        self.actions.verify_element_displayed(self.__item_search_history, is_display=False)
        self.actions.verify_element_displayed(self.__search_history, is_display=False)

    def verify_search_history_items(self, symbols: str | list[str]):
        symbols = symbols if isinstance(symbols, list) else [symbols]
        locator_list = [cook_element(self.__item_search_history_by_text, symbol) for symbol in symbols]
        self.actions.verify_elements_displayed(locator_list)
