from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.web_actions import WebActions
from src.data.enums import AccInfo
from src.page_object.web_app.base_page import BasePage
from src.page_object.web_app.components.trade.watch_list import WatchList
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import resource_id
from src.utils.format_utils import format_acc_balance


class AssetsPage(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)
        self.watch_list = WatchList(actions)

    # ------------------------ LOCATORS ------------------------ #
    __acc_name = (AppiumBy.XPATH, resource_id('account-name'))
    __acc_id = (AppiumBy.XPATH, resource_id('account-id'))
    __acc_type = (AppiumBy.XPATH, resource_id('account-type-tag'))
    __acc_details = (AppiumBy.XPATH, resource_id('account-detail'))

    __available_balance = (AppiumBy.XPATH, "//android.widget.TextView[@text='Available Balance']/following-sibling::android.widget.TextView[2]")
    __realised_profit_loss = (AppiumBy.XPATH, "//android.widget.TextView[@text='Realised Profit/Loss']/following-sibling::android.widget.TextView[2]")
    __credit = (AppiumBy.XPATH, "//android.widget.TextView[@text='Credit']/following-sibling::android.widget.TextView[3]")
    __deposit = (AppiumBy.XPATH, "//android.widget.TextView[@text='Deposit']/following-sibling::android.widget.TextView[3]")
    __withdrawal = (AppiumBy.XPATH, "//android.widget.TextView[@text='Withdrawal']/following-sibling::android.widget.TextView[3]")

    __item_watchlist = (AppiumBy.XPATH, resource_id('watchlist-symbol'))

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
        # scroll down a bit
        self.actions.scroll_down()
        return self.actions.get_text_elements(self.__item_watchlist)

        # elements = self.actions.find_elements(self.__item_watchlist)
        # return [ele.text.strip() for ele in elements]

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
