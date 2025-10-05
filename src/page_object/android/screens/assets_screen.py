import operator

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import SHORT_WAIT
from src.data.enums import AccInfo
from src.page_object.android.base_screen import BaseScreen
from src.page_object.android.components.trade.watch_list import WatchList
from src.utils.assert_utils import soft_assert
from src.utils.format_utils import format_acc_balance


class AssetsScreen(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)
        self.watch_list = WatchList(actions)

    # ------------------------ LOCATORS ------------------------ #
    __acc_name = (AppiumBy.ID, 'account-name')
    __acc_id = (AppiumBy.ID, 'account-id')
    __acc_type = (AppiumBy.ID, 'account-type-tag')
    __acc_details = (AppiumBy.ID, 'account-detail')

    __available_balance = (AppiumBy.XPATH, "//android.widget.TextView[@text='Available Balance']/following-sibling::android.widget.TextView[2]")
    __realised_profit_loss = (AppiumBy.XPATH, "//android.widget.TextView[@text='Realised Profit/Loss']/following-sibling::android.widget.TextView[2]")
    __credit = (AppiumBy.XPATH, "//android.widget.TextView[@text='Credit']/following-sibling::android.widget.TextView[2]")
    __deposit = (AppiumBy.XPATH, "//android.widget.TextView[@text='Deposit']/following-sibling::android.widget.TextView[2]")
    __withdrawal = (AppiumBy.XPATH, "//android.widget.TextView[@text='Withdrawal']/following-sibling::android.widget.TextView[1]")
    __item_watchlist = (AppiumBy.ID, 'watchlist-symbol')
    __view_transaction = (AppiumBy.ID, 'asset-header-view-all')

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

    def get_my_trade_list(self):
        # scroll down a bit
        self.actions.scroll_down()
        return self.actions.get_text_elements(self.__item_watchlist)

    def click_view_all_transaction(self):
        self.actions.click(self.__view_transaction)

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

    def verify_account_values_changed(self, acc_item: AccInfo, amount_change, old_value):
        # todo: enhance later
        locator_map = {
            AccInfo.BALANCE: self.__available_balance,
            AccInfo.REALISED_PROFIT_LOSS: self.__realised_profit_loss
        }

        actual = format_acc_balance(self.actions.get_text(locator_map[acc_item], timeout=SHORT_WAIT), to_float=True)
        exp_op = operator.ge if amount_change > 0 else operator.le
        soft_assert(exp_op(actual, old_value + amount_change), True, error_message=f"Actual: {actual}, Expected: {old_value + amount_change}, Operator: {exp_op.__name__!r}")

    def verify_account_balance_summary(self, exp_data, tolerance_percent=None, tolerance_fields=None):
        """Verify the asset account dashboard details"""
        actual = self._get_acc_balance_info()

        for item in exp_data:
            exp_data[item] = round(exp_data[item], 2)

        soft_assert(actual, exp_data, tolerance=tolerance_percent, tolerance_fields=tolerance_fields, field_tolerances={AccInfo.REALISED_PROFIT_LOSS: 10})

    def verify_my_trade_list(self, expected: list):
        actual = self.get_my_trade_list()
        soft_assert(actual, expected)
