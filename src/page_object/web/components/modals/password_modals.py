from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.page_object.web.base_page import BasePage
from src.utils.common_utils import data_testid
from src.utils.random_utils import random_email, random_userid


class PasswordModal(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ======================== CHANGE PASSWORD ======================== #

    # ------------------------ LOCATORS ------------------------ #
    __txt_old_password = (By.CSS_SELECTOR, data_testid('change-password-modal-old-password', 'input'))
    __txt_new_password = (By.CSS_SELECTOR, data_testid('change-password-modal-new-password', 'input'))
    __txt_confirm_new_password = (
        By.CSS_SELECTOR, data_testid('change-password-modal-confirm-new-password', 'input')
    )
    __btn_confirm = (By.CSS_SELECTOR, data_testid('change-password-modal-confirm', 'button'))
    __btn_close = (By.CSS_SELECTOR, data_testid('change-password-modal-close'))

    # ------------------------ ACTIONS ------------------------ #
    def change_password(self, old_password, new_password, close=False):
        """
        Changes the user's password using the change password modal.
        Args:
            old_password (str): Current password
            new_password (str): New password to set
        """
        self.actions.send_keys(self.__txt_old_password, old_password)
        self.actions.send_keys(self.__txt_new_password, new_password)
        self.actions.send_keys(self.__txt_confirm_new_password, new_password)
        self.actions.click(self.__btn_confirm)
        if close:
            self.close()

    def close(self):
        self.actions.click(self.__btn_close)

    # ------------------------ VERIFY ------------------------ #

    # ======================== RESET PASSWORD ======================== #
    __txt_email = (By.XPATH, "//input[placeholder='user@gmail.com']")
    __txt_account_id = (By.XPATH, "//input[placeholder='Enter your account ID']")
    __btn_submit = (By.XPATH, "//button[text()='Submit']")

    def fill_reset_password_form(self, email=random_email(), account_id=random_userid()):
        self.actions.send_keys(self.__txt_email, email)
        self.actions.send_keys(self.__txt_account_id, account_id)
        self.actions.click(self.__btn_submit)
