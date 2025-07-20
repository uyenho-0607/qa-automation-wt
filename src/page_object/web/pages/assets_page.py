from selenium.webdriver.common.by import By
from src.core.actions.web_actions import WebActions
from src.data.enums import URLPaths, AccInfo
from src.page_object.web.base_page import BasePage
from src.page_object.web.components.modals.trading_modals import TradingModals
from src.page_object.web.components.trade.asset_tab import AssetTab
from src.page_object.web.components.trade.watch_list import WatchList
from src.utils.assert_utils import soft_assert, compare_with_tolerance
from src.utils.common_utils import cook_element
from src.utils.format_utils import format_acc_balance
from src.utils.logging_utils import logger


class AssetsPage(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)
        self.asset_tab = AssetTab(actions)
        self.modals = TradingModals(actions)
        self.watch_list = WatchList(actions)

    # ------------------------ LOCATORS ------------------------ #

    __acc_type = (By.CSS_SELECTOR, "*[data-testid=account-type-tag]")
    __acc_name = (By.XPATH, "(//span[@data-testid='account-type-tag']/parent::div/parent::div)[2]")
    __acc_id = (By.XPATH, "//span[@data-testid='account-type-tag']/parent::div/parent::div/following-sibling::div")
    __acc_item = (By.XPATH, "//div[text()='{}']/following-sibling::div/div")

    # ------------------------ ACTIONS ------------------------ #
    def verify_page_url(self):
        super().verify_page_url(URLPaths.ASSETS)

    # ------------------------ VERIFY ------------------------ #
    def get_account_info(self):
        """ To retrieve the current account information data"""
        account_id = self.actions.get_text(self.__acc_id)
        account_details = self.actions.get_text(self.__acc_name)
        account_name = account_details.split("\n")[-1]
        account_type = account_details.split("\n")[0]

        return {
            "id": account_id,
            "name": account_name,
            "type": account_type,
        }

    # ------------------------ VERIFY ------------------------ #
    def verify_account_info(self, exp_data: dict):
        """Verify current account details, exp_data should be response from API get_account_statistics"""

        actual = self.get_account_info()
        expected = {
            "id": f"UID: {exp_data['id']} (1:{exp_data['leverage']})", "name": exp_data["name"], "type": exp_data["type"]
        }
        soft_assert(actual, expected)

    def verify_account_balance_summary(self, exp_data, acc_items: AccInfo = None, tolerance=0):
        """Verify the asset account dashboard details"""

        if acc_items:
            acc_items = acc_items if isinstance(acc_items, list) else [acc_items]
        else:
            acc_items = AccInfo.list_values()
        for item in acc_items:
            actual = format_acc_balance(self.actions.get_text(cook_element(self.__acc_item, item)))
            expected = round(exp_data.get(item), 2)

            logger.info(f"- Checking {item.value!r}")
            res = compare_with_tolerance(actual, expected, tolerance)
            soft_assert(res, True, error_message=f"Actual: {actual}, Expected: {expected}, Tolerance: {tolerance}%")
