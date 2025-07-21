from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.enums import SettingOptions, Language, ThemeOptions
from src.data.enums.home import NotiSettingsOpts
from src.data.objects.account_obj import ObjDemoAccount
from src.page_object.web.base_page import BasePage
from src.page_object.web.components.modals.demo_account_modals import DemoAccountModal
from src.page_object.web.components.modals.notification_settings import NotificationSettingsModal
from src.page_object.web.components.modals.password_modals import PasswordModal
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element, data_testid, translate_trade
from src.utils.format_utils import locator_format


class Settings(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)
        self.change_password_modal = PasswordModal(actions)
        self.demo_account_modal = DemoAccountModal(actions)
        self.notification_settings_modal = NotificationSettingsModal(actions)

    # ------------------------ LOCATORS ------------------------ #
    __btn_setting = (By.CSS_SELECTOR, "*[data-testid='setting-button']")
    __opt_setting = (By.CSS_SELECTOR, "*[data-testid='setting-option-{}']")
    __opt_language = (By.XPATH, "//div[@data-testid='setting-option-language']//li[text()='{}']")
    __btn_switch_theme = (By.CSS_SELECTOR, data_testid('switch-theme-button'))
    __opt_theme = (By.CSS_SELECTOR, data_testid('theme-option-{}'))

    # ------------------------ ACTIONS ------------------------ #
    def __open_setting(self):
        is_opened = self.actions.is_element_displayed(cook_element(self.__opt_setting, SettingOptions.LOGOUT), show_log=False)
        if not is_opened:
            self.actions.click(self.__btn_setting)

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
        self.actions.click(cook_element(self.__opt_language, language))

    def change_password(self, old_password, new_password):
        self.__open_setting()
        self.actions.click(cook_element(self.__opt_setting, locator_format(SettingOptions.CHANGE_PASSWORD)))
        self.change_password_modal.change_password(old_password, new_password)

    def change_theme(self, theme: ThemeOptions):
        option = theme or ThemeOptions.sample_values()
        self.actions.click(self.__btn_switch_theme)
        self.actions.click(cook_element(self.__opt_theme, option))

    def logout(self):
        self.__open_setting()
        self.actions.click(cook_element(self.__opt_setting, locator_format(SettingOptions.LOGOUT)))

    def toggle_noti_settings(self, options: NotiSettingsOpts):
        self.__open_setting()
        self.actions.click(cook_element(self.__opt_setting, locator_format(SettingOptions.NOTIFICATION_SETTING)))
        self.notification_settings_modal.toggle_setting(options)

    # ------------------------ VERIFY ------------------------ #

    def verify_theme_changed(self, theme: ThemeOptions):
        # Get computed background-color using JavaScript
        js_script = """
                var body = document.body;
                return window.getComputedStyle(body).color;
                """
        body_color = self.actions._driver.execute_script(js_script)

        match theme:
            case ThemeOptions.DARK | ThemeOptions.SYSTEM:
                expected_color = "rgb(234, 236, 239)"  # Adjust this value based on your dark theme
            case ThemeOptions.LIGHT:
                expected_color = "rgb(0, 9, 9)"  # Adjust this value based on your light theme
            case _:
                raise ValueError(f"Invalid theme: {theme} !")

        soft_assert(body_color == expected_color, True,
                    error_message=f"Body background color is not {theme}. Expected {expected_color}, got {body_color}")

    def verify_language_changed(self, language: Language | str):
        self.__open_setting()
        logout = cook_element(self.__opt_setting, locator_format(SettingOptions.LOGOUT))
        actual = self.actions.get_text(logout)
        soft_assert(actual, translate_trade(language))
