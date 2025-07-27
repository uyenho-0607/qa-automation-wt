from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.core.config_manager import Config
from src.data.enums import AccountType, Language
from src.data.project_info import ProjectConfig
from src.data.ui_messages import UIMessages
from src.page_object.web_app.base_page import BasePage
from src.page_object.web_app.components.modals.demo_acc_modals import DemoAccountModal
from src.page_object.web_app.components.modals.password_modals import PasswordModal
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element, data_testid
from src.utils.logging_utils import logger


class LoginPage(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)
        self.demo_account_modal = DemoAccountModal(actions)
        self.password_modal = PasswordModal(actions)

    # ------------------------ LOCATORS ------------------------ #
    __drp_language = (By.CSS_SELECTOR, data_testid('language-dropdown'))
    __opt_language = (By.XPATH, "//li[@data-testid='language-option' and text()='{}']")
    __tab_account_type = (By.CSS_SELECTOR, data_testid('tab-login-account-type-{}'))
    __txt_user_id = (By.CSS_SELECTOR, data_testid('login-user-id', 'input'))
    __txt_password = (By.CSS_SELECTOR, data_testid('login-password', 'input'))
    __btn_login = (By.CSS_SELECTOR, data_testid('login-submit', ))

    __forgot_password = (By.CSS_SELECTOR, data_testid('reset-password-link'))
    __txt_forgot_password_email = (By.CSS_SELECTOR, "input[placeholder='user@gmail.com']")
    __txt_forgot_password_id = (By.CSS_SELECTOR, "input[placeholder='Enter your account ID']")
    __btn_submit = (By.XPATH, "//button[@type='submit' and text()='Submit']")

    __open_demo_account = (By.CSS_SELECTOR, data_testid('login-account-signup'))

    # ------------------------ ACTIONS ------------------------ #
    def select_account_tab(self, account_type: AccountType):
        self.actions.click(cook_element(self.__tab_account_type, account_type))

    def select_language(self, language: Language):
        self.actions.click(self.__drp_language)
        self.actions.click(cook_element(self.__opt_language, language))

    def login(self, userid="", password="", account_type: AccountType = None, language: Language = None, wait=False):

        credentials = Config.credentials()
        userid = userid or credentials.username
        password = password or credentials.password

        logger.debug(f"- Login with user: {userid!r}")

        if language:
            self.select_language(language)

        self.select_account_tab(account_type or ProjectConfig.account)
        self.actions.send_keys(self.__txt_user_id, str(userid))
        self.actions.send_keys(self.__txt_password, str(password))
        self.actions.click(self.__btn_login)

        if wait:
            self.wait_for_spin_loader()

    # ------------------------ VERIFY ------------------------ #
    def verify_account_tab_is_displayed(self):
        acc_tab_demo = cook_element(self.__tab_account_type, AccountType.DEMO)
        self.actions.verify_element_displayed(acc_tab_demo)

    def verify_account_tab_is_selected(self, account_type: AccountType):
        # verify 'selected' in class attribute of account tab
        class_attr = self.actions.get_attribute(
            cook_element(self.__tab_account_type, account_type), "class"
        )
        soft_assert(
            "selected" in class_attr, True,
            error_message=f"Demo account is not selected, class attribute: {class_attr!r}"
        )

    def verify_account_autofill_value(self, userid, password):
        actual_userid = self.actions.get_attribute(self.__txt_user_id, "value")
        soft_assert(actual_userid, str(userid))

        actual_password = self.actions.get_attribute(self.__txt_password, "value")
        soft_assert(actual_password, password)

    def verify_alert_error_message(self, account_type=None):
        account_type = account_type or ProjectConfig.account

        err_msg = UIMessages.LOGIN_INVALID
        if account_type == AccountType.DEMO:
            err_msg = UIMessages.LOGIN_INVALID_CREDENTIALS

        super().verify_alert_error_message(err_msg)
