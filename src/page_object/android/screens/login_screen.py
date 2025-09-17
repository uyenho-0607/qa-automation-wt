from contextlib import suppress

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.core.config_manager import Config
from src.data.consts import LONG_WAIT, EXPLICIT_WAIT
from src.data.enums import AccountType, Language
from src.data.project_info import RuntimeConfig
from src.data.ui_messages import UIMessages
from src.page_object.android.base_screen import BaseScreen
from src.page_object.android.components.modals.demo_acc_modals import DemoAccountModal
from src.page_object.android.components.modals.password_modals import PasswordModal
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element, translate_sign_in
from src.utils.logging_utils import logger


class LoginScreen(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)
        self.demo_account_modal = DemoAccountModal(actions)
        self.password_modal = PasswordModal(actions)

    # ------------------------ LOCATORS ------------------------ #
    __tab_account_type = (AppiumBy.ID, 'tab-login-account-type-{}')
    __drp_language = (AppiumBy.ID, 'language-dropdown')
    __opt_language = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("language-option").descriptionContains("{}")')
    __txt_user_id = (AppiumBy.ID, 'login-user-id')
    __txt_password = (AppiumBy.ID, 'login-password')
    __btn_eye_masked = (AppiumBy.ID, 'input-password-hidden')
    __btn_sign_in = (AppiumBy.ID, 'login-submit')
    __lnk_reset_password = (AppiumBy.ID, 'reset-password-link')
    __btn_sign_up = (AppiumBy.ID, 'login-account-signup')
    __alert_error = (AppiumBy.ID, 'alert-error')
    __btn_skip = (AppiumBy.ID, 'ads-skip-button')

    # ------------------------ ACTIONS ------------------------ #
    def select_account_tab(self, account_type: AccountType):
        self.actions.click(cook_element(self.__tab_account_type, account_type))

    def select_language(self, language: Language):
        self.actions.click(self.__drp_language)
        self.actions.click(cook_element(self.__opt_language, language))

    def click_sign_in(self):
        self.actions.click(self.__btn_sign_in)

    def click_forgot_password(self):
        self.actions.click(self.__lnk_reset_password)

    def login(self, userid="", password="", account_type: AccountType = None, language: Language = None, wait=False):
        credentials = Config.credentials()
        userid = userid or credentials.username
        password = password or credentials.password

        logger.debug(f"- Login with user: {userid!r}")
        while self.actions.is_element_displayed(self.__btn_skip, timeout=5):
            with suppress(Exception):
                self.actions.click(self.__btn_skip, raise_exception=False, show_log=False)

        if language:
            self.select_language(language)

        self.select_account_tab(account_type or RuntimeConfig.account)
        self.actions.send_keys(self.__txt_user_id, str(userid))
        self.actions.send_keys(self.__txt_password, str(password))
        self.actions.click(self.__btn_sign_in)

        if wait:
            self.wait_for_spin_loader()

    def select_open_demo_account(self):
        self.select_account_tab(AccountType.DEMO)
        self.actions.click(self.__btn_sign_up)

    # ------------------------ VERIFY ------------------------ #
    def verify_language(self, language: Language):
        actual = self.actions.get_content_desc(self.__btn_sign_in)
        soft_assert(actual, translate_sign_in(language))

    def verify_account_tab_is_displayed(self):
        acc_tab_demo = cook_element(self.__tab_account_type, AccountType.DEMO)
        self.actions.verify_element_displayed(acc_tab_demo)

    def verify_account_autofill_value(self, userid, password):
        actual_userid = self.actions.get_attribute(self.__txt_user_id, "text")
        soft_assert(actual_userid, str(userid))

        self.actions.click(self.__btn_eye_masked)
        actual_password = self.actions.get_attribute(self.__txt_password, "text")
        soft_assert(actual_password, password)
    
    def verify_alert_error_message(self, account_type=None):
        account_type = account_type or RuntimeConfig.account
        err_msg = UIMessages.LOGIN_INVALID
        if account_type == AccountType.DEMO or RuntimeConfig.is_non_oms():
            err_msg = UIMessages.LOGIN_INVALID_CREDENTIALS

        super().verify_alert_error_message(err_msg)
