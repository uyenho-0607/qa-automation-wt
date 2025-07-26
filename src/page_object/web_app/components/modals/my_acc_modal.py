from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.web_actions import WebActions
from src.data.consts import SHORT_WAIT
from src.data.enums import AccSummary
from src.page_object.web_app.base_page import BasePage
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element, resource_id
from src.utils.format_utils import format_acc_balance


class MyAccountModal(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __items = (AppiumBy.XPATH, "//android.widget.TextView[@text='{}']/following-sibling::android.widget.TextView[1]")
    __drp_balance = (AppiumBy.XPATH, "//android.widget.TextView[@text='Balance']/following-sibling::android.widget.TextView[1]")
    __drp_note = (AppiumBy.XPATH, "//android.widget.TextView[@text='Note']/following-sibling::android.widget.TextView[1]")
    __btn_close = (AppiumBy.XPATH, resource_id('modal-close-button'))

    # ------------------------ ACTIONS ------------------------ #

    def is_open(self):
        return self.actions.is_element_displayed(cook_element(self.__items, AccSummary.STOP_OUT_LEVEL))

    def close(self):
        if self.actions.is_element_displayed(self.__btn_close):
            self.actions.click(self.__btn_close)

    def toggle_balance(self, open=True):
        is_open = self.actions.is_element_displayed(cook_element(self.__items, AccSummary.BALANCE))
        if is_open != open:
            self.actions.click(self.__drp_balance)

    def toggle_note(self, open=True):
        is_open = self.actions.is_element_displayed(cook_element(self.__items, AccSummary.STOP_OUT_LEVEL))
        if is_open != open:
            self.actions.click(self.__drp_note)

    def get_account_info(self):
        # get actual all value
        res = {}
        for item in AccSummary.list_values():
            value = self.actions.get_text(cook_element(self.__items, item))
            res[item] = format_acc_balance(value)
        return res

    # ------------------------ VERIFY ------------------------ #

    def verify_account_info(self, exp_dict):
        actual = self.get_account_info()
        soft_assert(actual, exp_dict, tolerance=0.05, tolerance_fields=AccSummary.list_values(except_val=AccSummary.BALANCE))


    def verify_balance_items_displayed(self, is_display=True):
        locators = [cook_element(self.__items, item) for item in AccSummary.checkbox_list()]
        self.actions.verify_elements_displayed(locators, is_display=is_display, timeout=SHORT_WAIT)

    def verify_note_items_displayed(self, is_display=True):
        locators = [cook_element(self.__items, item) for item in AccSummary.note_list()]
        self.actions.verify_elements_displayed(locators, is_display=is_display, timeout=SHORT_WAIT)


