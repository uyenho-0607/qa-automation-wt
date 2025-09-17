from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import SHORT_WAIT
from src.data.enums import SettingOptions
from src.page_object.web_app.base_page import BasePage
from src.page_object.web_app.components.modals.password_modals import PasswordModal
from src.utils.common_utils import cook_element, data_testid
from src.utils.format_utils import locator_format
from src.utils.logging_utils import logger


class Settings(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)
        self.__change_password_modal = PasswordModal(actions)

    # ------------------------ LOCATORS ------------------------ #
    __btn_account_selector = (By.CSS_SELECTOR, data_testid("account-selector"))
    __txt_account_id = (By.CSS_SELECTOR, data_testid("account-id"))
    __txt_account_detail = (By.CSS_SELECTOR, data_testid("account-detail"))

    # Account Settings
    __opt_setting = (By.CSS_SELECTOR, data_testid("setting-option-{}"))
    __label_oct = (By.XPATH, "//div[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') = 'one-click trading']")

    # Support & About
    __btn_help_support = (By.CSS_SELECTOR, data_testid("setting-option-help-support"))
    __btn_about = (By.CSS_SELECTOR, data_testid("setting-option-about"))

    # Logout
    __btn_logout = (By.CSS_SELECTOR, data_testid("account-logout"))

    # ------------------------ ACTIONS ------------------------ #
    def is_oct_enable(self):
        is_enable = self.actions.is_element_displayed(self.__label_oct, timeout=SHORT_WAIT)
        logger.debug(f"- OCT enabled in Admin config: {is_enable!r}")
        return is_enable

    def __open_setting(self):
        self.actions.click(self.__btn_account_selector)

    def switch_to_live_account(self):
        self.__open_setting()
        self.actions.click(cook_element(self.__opt_setting, locator_format(SettingOptions.SWITCH_TO_LIVE)))

    def change_password(self, old_password, new_password):
        self.__open_setting()
        self.actions.click(cook_element(self.__opt_setting, locator_format(SettingOptions.CHANGE_PASSWORD)))
        self.__change_password_modal.change_password(old_password, new_password)

    def logout(self):
        self.__open_setting()
        self.actions.click(self.__btn_logout)

    # ------------------------ VERIFY ------------------------ #
