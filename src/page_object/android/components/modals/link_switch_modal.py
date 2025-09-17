from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.enums import AccountType
from src.page_object.android.base_screen import BaseScreen
from src.utils.common_utils import cook_element


class LinkSwitchModal(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __btn_add_account = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("{} Account")')
    __txt_user_id = (AppiumBy.XPATH,
                     "(//android.widget.TextView[@text='Account ID']/following-sibling::android.view.ViewGroup/android.widget.EditText)[1]")
    __txt_password = (AppiumBy.XPATH,
                      "(//android.widget.TextView[@text='Account ID']/following-sibling::android.view.ViewGroup/android.widget.EditText)[2]")
    __btn_confirm = (AppiumBy.XPATH,
                     "//*[translate(@content-desc, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='confirm']")
    __btn_close = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("modal-close-button")')

    # ------------------------ ACTIONS ------------------------ #

    def link_account(self, account_type: AccountType):
        self.actions.click(cook_element(self.__btn_add_account, account_type.capitalize()))
        self.actions.send_keys(self.__txt_user_id, "188888888")
        self.actions.send_keys(self.__txt_password, "Asd123")
        self.actions.click(self.__btn_confirm)

    # ------------------------ VERIFY ------------------------ #
