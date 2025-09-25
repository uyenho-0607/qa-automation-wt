from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.enums import AccInfo
from src.page_object.ios.base_screen import BaseScreen
from src.page_object.ios.components.trade.watch_list import WatchList
from src.utils.assert_utils import soft_assert
from src.utils.format_utils import format_acc_balance


class AssetsScreen(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)
        self.watch_list = WatchList(actions)

    # ------------------------ LOCATORS ------------------------ #
    __acc_name = (AppiumBy.ACCESSIBILITY_ID, 'account-name')
    __acc_id = (AppiumBy.ACCESSIBILITY_ID, 'account-id')
    __acc_type = (AppiumBy.ACCESSIBILITY_ID, 'account-selector')
    __acc_details = (AppiumBy.ACCESSIBILITY_ID, 'account-detail')

    __available_balance = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeOther[`name CONTAINS 'Available Balance'`]/XCUIElementTypeStaticText[-1]")
    __realised_profit_loss = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeOther[`name CONTAINS 'Realised Profit/Loss'`]/XCUIElementTypeStaticText[-1]")
    __credit = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeOther[`name CONTAINS 'Credit'`]/XCUIElementTypeStaticText[-1]")
    __deposit = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeOther[`name CONTAINS 'Deposit'`]/XCUIElementTypeStaticText[-1]")
    __withdrawal = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeOther[`name CONTAINS 'Withdrawal'`]/XCUIElementTypeStaticText[-1]")
    __item_watchlist = (AppiumBy.XPATH, "//*[@name='My Trades \uf130']/following-sibling::XCUIElementTypeOther/XCUIElementTypeOther[1]")

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

        res = self.actions.get_text_elements(self.__item_watchlist)
        
        # Get just the symbol name
        return [
            next(word for word in item.split() if word[0].isalnum())
            for item in res
        ]

    def select_last_symbol(self):
        self.actions.click(self.__item_watchlist)

    # ------------------------ VERIFY ------------------------ #
    def verify_account_details(self, exp_data):
        actual = {
            "name": self.actions.get_text(self.__acc_name),
            "id": self.actions.get_text(self.__acc_id),
            "type": self.actions.get_text(self.__acc_type).split()[-1],
            "details": self.actions.get_text(self.__acc_details)
        }

        expected = {
            "name": exp_data["name"],
            "id": exp_data["id"],
            "type": exp_data["type"],
            "details": f"{exp_data['currency']} | 1:{exp_data['leverage']}"
        }

        soft_assert(actual, expected)

    def verify_account_balance_summary(self, exp_data, tolerance_percent = None, tolerance_fields = None):
        """Verify the asset account dashboard details"""
        actual = self._get_acc_balance_info()

        for item in exp_data:
            exp_data[item] = round(exp_data[item], 2)

        soft_assert(actual, exp_data, tolerance=tolerance_percent, tolerance_fields=tolerance_fields)

    def verify_mytrade_items(self, expected: list):
        actual = self.get_mytrade_item()
        soft_assert(actual, expected)
