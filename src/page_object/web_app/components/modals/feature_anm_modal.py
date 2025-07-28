from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import SHORT_WAIT
from src.page_object.web_app.base_page import BasePage
from src.utils.logging_utils import logger
from src.utils.common_utils import data_testid


class FeatureAnnouncementModal(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    # ------------------------ LOCATORS ------------------------ #
    __btn_got_it = (By.CSS_SELECTOR, data_testid('feature-announcement-modal-got-it-button'))
    __btn_try_now = (By.CSS_SELECTOR, data_testid('feature-announcement-modal-try-it-now-button'))

    # ------------------------ ACTIONS ------------------------ #
    def got_it(self):
        """Click the 'Got it' button to dismiss the feature announcement."""
        while self.actions.is_element_displayed(self.__btn_got_it, timeout=SHORT_WAIT):
            logger.debug("- Clicking on btn Ok Got it")
            self.actions.click(self.__btn_got_it)

    def try_it_now(self):
        """Click the 'Try it now' button to try the new feature."""
        self.actions.click(self.__btn_try_now)

    # ------------------------ VERIFY ------------------------ #
