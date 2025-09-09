import time

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.objects.account_obj import ObjDemoAccount
from src.data.enums import SettingOptions, NotiSettingsOpts, Language, ThemeOptions
from src.page_object.android.base_screen import BaseScreen
from src.page_object.android.components.modals.demo_acc_modals import DemoAccountModal
from src.page_object.android.components.modals.password_modals import PasswordModal
from src.page_object.android.components.modals.notification_settings import NotificationSettingsModal
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element, translate_trade
from src.utils.format_utils import locator_format
from src.utils.logging_utils import logger


class Settings(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)
        self.demo_account_modal = DemoAccountModal(actions)
        self.__change_password_modal = PasswordModal(actions)
        self.notification_settings_modal = NotificationSettingsModal(actions)

    # ------------------------ LOCATORS ------------------------ #
    __btn_account_selector = (AppiumBy.XPATH, "//*[@resource-id='account-selector']")
    __txt_account_name = (AppiumBy.XPATH, "//*[@resource-id='account-name']")
    __txt_account_id = (AppiumBy.XPATH, "//*[@resource-id='account-id']")
    __txt_account_detail = (AppiumBy.XPATH, "//*[@resource-id='account-detail']")

    # Settings
    __opt_setting = (AppiumBy.XPATH, "//*[@resource-id='setting-option-{}']")
    __switch_one_click_trading = (AppiumBy.XPATH, "//*[@resource-id='setting-option-oct']//android.widget.Switch")
    __opt_language = (AppiumBy.XPATH, "//*[@content-desc='{}']")
    __opt_theme = (AppiumBy.XPATH, "//*[contains(@content-desc, '{}')]")
    __demo_acc = (AppiumBy.XPATH, "//android.widget.TextView[@text='Demo Account']")
    __btn_help_support = (AppiumBy.XPATH, "//*[@resource-id='setting-option-help-support']")
    __btn_about = (AppiumBy.XPATH, "//*[@resource-id='setting-option-about']")
    __btn_logout = (AppiumBy.XPATH, "//*[@resource-id='account-logout']")

    # ------------------------ ACTIONS ------------------------ #
    def __open_setting(self):
        logger.info(f"- Click on the profile icon to open setting")
        time.sleep(2)
        self.actions.click(self.__btn_account_selector)

    def toggle_one_click_trading(self):
        self.__open_setting()
        self.actions.click(self.__switch_one_click_trading)

    def link_switch_account(self, account: SettingOptions = SettingOptions.LINK_SWITCH_TO_LIVE):
        self.__open_setting()
        self.actions.click(cook_element(self.__opt_setting, locator_format(account)))

    def switch_to_account(self, account: SettingOptions = SettingOptions.SWITCH_TO_LIVE):
        self.__open_setting()
        self.actions.click(cook_element(self.__opt_setting, locator_format(account)))

    def open_demo_account(self, account_info: ObjDemoAccount):
        self.__open_setting()
        self.actions.click(cook_element(self.__opt_setting, locator_format(SettingOptions.OPEN_DEMO_ACCOUNT)))
        self.demo_account_modal.fill_demo_account_creation_form(account_info)

    def change_language(self, language: Language):
        self.__open_setting()
        self.actions.click(cook_element(self.__opt_setting, locator_format(SettingOptions.CHANGE_LANGUAGE)))
        time.sleep(2)
        self.actions.click(cook_element(self.__opt_language, language))

    def change_theme(self, theme: ThemeOptions):
        self.__open_setting()
        option = theme or ThemeOptions.sample_values()
        self.actions.click(cook_element(self.__opt_setting, locator_format(SettingOptions.APPEARANCE)))
        self.actions.click(cook_element(self.__opt_theme, option.capitalize()))

    def toggle_noti_settings(self, options: NotiSettingsOpts):
        self.__open_setting()
        self.actions.click(cook_element(self.__opt_setting, locator_format(SettingOptions.NOTIFICATION_SETTING)))
        self.notification_settings_modal.toggle_setting(options)

    def change_password(self, old_password, new_password):
        self.__open_setting()
        self.actions.click(cook_element(self.__opt_setting, locator_format(SettingOptions.CHANGE_PASSWORD)))
        self.__change_password_modal.change_password(old_password, new_password)

    def logout(self):
        self.__open_setting()
        self.actions.scroll_down()
        self.actions.click(self.__btn_logout)

    # ------------------------ VERIFY ------------------------ #

    def verify_language_changed(self, language: Language | str):
        self.go_back()
        actual = self.actions.get_content_desc(self.__btn_logout)
        soft_assert(actual, translate_trade(language).upper())
