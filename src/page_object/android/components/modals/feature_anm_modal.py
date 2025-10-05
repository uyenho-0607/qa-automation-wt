from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import SHORT_WAIT
from src.page_object.android.base_screen import BaseScreen
from src.utils.logging_utils import logger


class FeatureAnnouncementModal(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __btn_got_it = (AppiumBy.ID, 'feature-announcement-modal-got-it-button')

    # ------------------------ ACTIONS ------------------------ #
    def got_it(self):
        """Click the 'Got it' button to dismiss the feature announcement."""
        while self.actions.is_element_displayed(self.__btn_got_it, timeout=3):
            logger.debug("- Clicking on btn Ok Got it")
            self.actions.click(self.__btn_got_it)

    # ------------------------ VERIFY ------------------------ #
