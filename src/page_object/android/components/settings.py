from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.enums import SettingOptions, Language
from src.page_object.android.base_screen import BaseScreen
from src.page_object.android.components.modals.password_modals import PasswordModal
from src.utils.common_utils import cook_element
from src.utils.format_utils import locator_format


class Settings(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)
        self.__change_password_modal = PasswordModal(actions)

    # ------------------------ LOCATORS ------------------------ #
    __btn_account_selector = (AppiumBy.XPATH, "//*[@resource-id='account-selector']")
    __txt_account_name = (AppiumBy.XPATH, "//*[@resource-id='account-name']")
    __txt_account_id = (AppiumBy.XPATH, "//*[@resource-id='account-id']")
    __txt_account_detail = (AppiumBy.XPATH, "//*[@resource-id='account-detail']")

    # Account Settings
    __opt_setting = (AppiumBy.XPATH, "//*[@resource-id='setting-option-{}']")
    __switch_one_click_trading = (AppiumBy.XPATH, "//*[@resource-id='setting-option-oct']//android.widget.Switch")
    __opt_language = (AppiumBy.XPATH, "//*[@resource-id='setting-option-language']//android.widget.TextView[text()='{}']")

    # Support & About
    __btn_help_support = (AppiumBy.XPATH, "//*[@resource-id='setting-option-help-support']")
    __btn_about = (AppiumBy.XPATH, "//*[@resource-id='setting-option-about']")

    # Logout
    __btn_logout = (AppiumBy.XPATH, "//*[@resource-id='account-logout']")

    # ------------------------ ACTIONS ------------------------ #
    def __open_setting(self):
        self.actions.click(self.__btn_account_selector)

    def toggle_one_click_trading(self):
        self.actions.click(self.__switch_one_click_trading)

    def switch_to_live_account(self):
        self.__open_setting()
        self.actions.click(cook_element(self.__opt_setting, locator_format(SettingOptions.SWITCH_TO_LIVE)))

    def change_language(self, language: Language):
        self.__open_setting()
        self.actions.click(cook_element(self.__opt_setting, locator_format(SettingOptions.CHANGE_LANGUAGE)))
        self.actions.click(cook_element(self.__opt_language, language))

    def change_password(self, old_password, new_password):
        self.__open_setting()
        self.actions.click(cook_element(self.__opt_setting, locator_format(SettingOptions.CHANGE_PASSWORD)))
        self.__change_password_modal.change_password(old_password, new_password)

    def logout(self):
        self.__open_setting()
        self.actions.click(self.__btn_logout)

    # ------------------------ VERIFY ------------------------ #
