from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.enums.home import NotiSettingsOpts
from src.page_object.web.base_page import BasePage
from src.utils.common_utils import cook_element, data_testid


class NotificationSettingsModal(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __btn_close = (By.CSS_SELECTOR, data_testid('notification-settings-modal-close'))
    __opt_setting = (By.XPATH, "//div[@data-testid='notification-settings-title' and text()='{}']/div")

    # ------------------------ ACTIONS ------------------------ #
    def close(self):
        self.actions.click(self.__btn_close)

    def toggle_setting(self, options: NotiSettingsOpts, enable: bool = True):
        options = options if isinstance(options, list) else [options]

        custom = " unchecked" if enable else " checked"

        for option in options:
            locator = cook_element(self.__opt_setting, option)
            if custom in self.actions.get_attribute(locator, "class"):
                self.actions.click(locator)

        self.close()
