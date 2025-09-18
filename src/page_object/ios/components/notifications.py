import re
from contextlib import suppress

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import QUICK_WAIT, EXPLICIT_WAIT
from src.page_object.ios.base_screen import BaseScreen
from src.utils.assert_utils import soft_assert, compare_noti_with_tolerance
from src.utils.common_utils import cook_element
from src.utils.logging_utils import logger


class Notifications(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __noti_selector = (AppiumBy.ACCESSIBILITY_ID, "notification-selector")
    __tab_noti = (AppiumBy.ACCESSIBILITY_ID, "tab-notification-type-{}")
    __noti_des = (AppiumBy.ACCESSIBILITY_ID, "notification-box-description")
    __noti_title = (AppiumBy.ACCESSIBILITY_ID, "notification-box-title")
    __noti_list_items = (AppiumBy.ACCESSIBILITY_ID, "notification-list-result-item")
    __btn_close_banner = (AppiumBy.ACCESSIBILITY_ID, "notification-box-close")
    __noti_result = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeOther[`name == "notification-list-result-item" AND label CONTAINS "{}"`]')

    # ------------------------ ACTIONS ------------------------ #
    def open_notification_box(self):
        if self.actions.is_element_displayed(self.__noti_selector):
            self.actions.click(self.__noti_selector)

    def close_noti_banner(self):
        if self.actions.is_element_displayed(self.__btn_close_banner, timeout=QUICK_WAIT):
            with suppress(Exception):
                self.actions.click(self.__btn_close_banner, show_log=False, raise_exception=False)

    def _get_open_position(self):
        noti = cook_element(self.__noti_result, "Open Position")
        return self.actions.get_text(noti)

    def _get_position_closed(self):
        noti = cook_element(self.__noti_result, "Position Closed")
        return self.actions.get_text(noti)

    # ------------------------ VERIFY ------------------------ #

    def verify_notification_banner(self, expected_title="", expected_des="", timeout=EXPLICIT_WAIT):
        """Verify title and description of notification banner"""
        if expected_des:
            logger.debug("- Fetching notification description")
            actual_des = self.actions.get_text(self.__noti_des, timeout=timeout)

            logger.debug(f"> Check noti des = {expected_des!r}")
            compare_noti_with_tolerance(actual_des, expected_des)

        if expected_title:
            timeout = EXPLICIT_WAIT if not expected_des else QUICK_WAIT
            logger.debug("- Fetching notification title")
            actual_title = self.actions.get_text(self.__noti_title, timeout=timeout)

            if not expected_des or actual_title:
                logger.debug(f"> Check noti title - {expected_title!r}")
                soft_assert(actual_title, expected_title)

    def verify_notification_result(self, expected_result: str | list, close=True):
        self.open_notification_box()

        if "Open Position" in expected_result:
            noti_res = self._get_open_position()

        elif "Position Closed" in expected_result:
            noti_res = self._get_position_closed()

        else:
            # get latest notification
            noti_res = self.actions.get_text(self.__noti_list_items)

        actual_res = noti_res.split(", ")[0].replace("  ", " ")
        actual_res = actual_res.split("\n")[0]

        pattern = r"^(.*?\d+(?:\.\d+)?)(?=\s+(?:a\s+few\s+seconds|a\s+day|an?\s+\w+|\d+\s+\w+)\s+ago)"
        match = re.search(pattern, actual_res)
        actual_res = match.group(1) if match else actual_res

        compare_noti_with_tolerance(actual_res, expected_result, is_banner=False)
        if close:
            self.go_back()
