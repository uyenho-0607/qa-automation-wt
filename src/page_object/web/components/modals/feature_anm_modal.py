from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import SHORT_WAIT
from src.page_object.web.base_page import BasePage
from src.utils.common_utils import data_testid


class FeatureAnnouncementModal(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __btn_got_it = (By.CSS_SELECTOR, data_testid('feature-announcement-modal-got-it-button'))
    __btn_try_now = (By.CSS_SELECTOR, data_testid('feature-announcement-modal-try-it-now-button'))

    # ------------------------ ACTIONS ------------------------ #
    def got_it(self):
        """
        Clicks the 'Got it' button on the feature announcement modal.
        Will continue clicking if multiple announcements are present.
        """
        while self.actions.is_element_displayed(self.__btn_got_it, timeout=SHORT_WAIT):
            self.actions.click(self.__btn_got_it)

    def try_it_now(self):
        """Clicks the 'Try it now' button on the feature announcement modal."""
        self.actions.click(self.__btn_try_now)

    # ------------------------ VERIFY ------------------------ #
