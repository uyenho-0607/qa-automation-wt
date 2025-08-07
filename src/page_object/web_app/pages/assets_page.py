from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.enums import AccInfo
from src.page_object.web_app.base_page import BasePage
from src.page_object.web_app.components.trade.watch_list import WatchList
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import data_testid
from src.utils.format_utils import format_acc_balance


class AssetsPage(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)
        self.watch_list = WatchList(actions)

    # ------------------------ LOCATORS ------------------------ #
    __acc_name = (By.CSS_SELECTOR, data_testid('account-name'))
    __acc_id = (By.CSS_SELECTOR, data_testid('account-id'))
    __acc_type = (By.CSS_SELECTOR, data_testid('account-type-tag'))
    __acc_details = (By.CSS_SELECTOR, data_testid('account-detail'))

    __available_balance = (By.XPATH, "//div[text()='Available Balance']/following-sibling::div")
    __realised_profit_loss = (By.XPATH, "//div[text()='Realised Profit/Loss']/following-sibling::div")
    __credit = (By.XPATH, "//div[text()='Credit']/following-sibling::div")
    __deposit = (By.XPATH, "//div[text()='Deposit']/following-sibling::div")
    __withdrawal = (By.XPATH, "//div[text()='Withdrawal']/following-sibling::div")

    __item_watchlist = (By.CSS_SELECTOR, data_testid('watchlist-symbol'))

    # ------------------------ ACTIONS ------------------------ #
    def _get_acc_balance_info(self):
        res = {
            AccInfo.BALANCE: format_acc_balance(self.actions.get_text(self.__available_balance)),
            AccInfo.REALISED_PROFIT_LOSS: format_acc_balance(self.actions.get_text(self.__realised_profit_loss)),
            AccInfo.CREDIT: format_acc_balance(self.actions.get_text(self.__credit)),
            AccInfo.DEPOSIT: format_acc_balance(self.actions.get_text(self.__deposit)),
            AccInfo.WITHDRAWAL: format_acc_balance(self.actions.get_text(self.__withdrawal))
        }

        return res

    def get_mytrade_item(self):
        self.actions.scroll_to_element(self.__item_watchlist)
        return self.actions.get_text_elements(self.__item_watchlist)

    # ------------------------ VERIFY ------------------------ #
    def verify_account_details(self, exp_data):
        actual = {
            "name": self.actions.get_text(self.__acc_name),
            "id": self.actions.get_text(self.__acc_id),
            "type": self.actions.get_text(self.__acc_type),
            "details": self.actions.get_text(self.__acc_details)
        }

        expected = {
            "name": exp_data["name"],
            "id": exp_data["id"],
            "type": exp_data["type"],
            "details": f"{exp_data['currency']} | 1:{exp_data['leverage']}"
        }

        soft_assert(actual, expected)

    def verify_account_balance_summary(self, exp_data, tolerance_percent=None, tolerance_fields=None):
        """Verify the asset account dashboard details"""
        actual = self._get_acc_balance_info()

        for item in exp_data:
            exp_data[item] = round(exp_data[item], 2)

        soft_assert(actual, exp_data, tolerance=tolerance_percent, tolerance_fields=tolerance_fields)

    def verify_mytrade_items(self, expected: list):
        actual = self.get_mytrade_item()
        soft_assert(actual, expected)
