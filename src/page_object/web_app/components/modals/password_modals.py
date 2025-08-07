from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.web_actions import WebActions
from src.page_object.web_app.base_page import BasePage
from src.utils.random_utils import random_email, random_userid


class PasswordModal(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __txt_old_password = (AppiumBy.XPATH, "//*[@resource-id='change-password-modal-old-password']")
    __txt_new_password = (AppiumBy.XPATH, "//*[@resource-id='change-password-modal-new-password']")
    __txt_confirm_new_password = (
        AppiumBy.XPATH, "//*[@resource-id='change-password-modal-confirm-new-password']"
    )
    __btn_confirm = (AppiumBy.XPATH, "//*[@resource-id='change-password-modal-confirm']")

    # ======================== RESET PASSWORD ======================== #
    __txt_email = (AppiumBy.XPATH, "//*[@resource-id='reset-password-email']")
    __txt_account_id = (AppiumBy.XPATH, "//*[@resource-id='reset-password-account-id']")
    __btn_submit = (AppiumBy.XPATH, "//*[@resource-id='reset-password-submit']")

    # ------------------------ ACTIONS ------------------------ #
    def change_password(self, old_password, new_password):
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

    def fill_reset_password_form(self, email=random_email(), account_id=random_userid()):
        self.actions.send_keys(self.__txt_email, email)
        self.actions.send_keys(self.__txt_account_id, account_id)
        self.actions.click(self.__btn_submit)

    # ------------------------ VERIFY ------------------------ #
