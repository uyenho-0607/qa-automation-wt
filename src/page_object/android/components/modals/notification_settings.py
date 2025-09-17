from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.enums.home import NotiSettingsOpts
from src.page_object.android.base_screen import BaseScreen
from src.utils.common_utils import cook_element


class NotificationSettingsModal(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __opt_setting = (AppiumBy.XPATH, "//android.widget.TextView[@text='{}']/following-sibling::android.widget.Switch[1]")

    # ------------------------ ACTIONS ------------------------ #

    def toggle_setting(self, options: NotiSettingsOpts, enable: bool = True):
        options = options if isinstance(options, list) else [options]

        for option in options:
            locator = cook_element(self.__opt_setting, option)
            is_checked = self.actions.get_attribute(locator, "checked") == "true"

            # If the current state does not match the desired state, click
            if is_checked != enable:
                self.actions.click(locator)

        self.go_back()
