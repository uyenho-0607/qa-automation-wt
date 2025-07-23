import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import QUICK_WAIT, EXPLICIT_WAIT, SHORT_WAIT
from src.data.objects.trade_obj import ObjTrade
from src.page_object.ios.base_screen import BaseScreen
from src.utils import DotDict
from src.utils.assert_utils import soft_assert, compare_noti_with_tolerance
from src.utils.common_utils import resource_id, log_page_source
from src.utils.logging_utils import logger


class Notifications(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #

    __noti_selector = (AppiumBy.XPATH, "//*[@name='notification-selector']")
    __tab_noti = (AppiumBy.ACCESSIBILITY_ID, "tab-notification-type-{}")
    __noti_des = (AppiumBy.ACCESSIBILITY_ID, "notification-box-description")
    __noti_title = (AppiumBy.ACCESSIBILITY_ID, "notification-box-title")
    __noti_list_items = (AppiumBy.ACCESSIBILITY_ID, "notification-list-result-item")
    __btn_close = (AppiumBy.ACCESSIBILITY_ID, "notification-box-close")

    # Noti order details
    __noti_details_order_type = (AppiumBy.ACCESSIBILITY_ID, "notification-order-details-modal-order-type")

    __noti_details_symbol = (
        AppiumBy.XPATH, "//*[@name='notification-order-details-label' and @label='Symbol']/following-sibling::*[1]"
    )
    __noti_details_volume = (
        AppiumBy.XPATH,
        "//*[@name='notification-order-details-label' and @label='Size' or @label='Volume']/following-sibling::*[1]"
    )
    __noti_details_units = (
        AppiumBy.XPATH,
        "//*[@name='notification-order-details-label' and @label='Units']/following-sibling::*[1]"
    )
    __noti_details_stop_loss = (
        AppiumBy.XPATH,
        "//*[@name='notification-order-details-label' and @label='Stop Loss']/following-sibling::*[1]"
    )
    __noti_details_take_profit = (
        AppiumBy.XPATH,
        "//*[@name='notification-order-details-label' and @label='Take Profit']/following-sibling::*[1]"
    )

    # ------------------------ ACTIONS ------------------------ #
    def open_notification_box(self):
        if self.actions.is_element_displayed(self.__noti_selector):
            self.actions.click(self.__noti_selector)

    def close_noti_banner(self):
        if self.actions.is_element_displayed(self.__btn_close, timeout=QUICK_WAIT):
            try:
                self.actions.click(self.__btn_close, show_log=False, raise_exception=False)

            except TimeoutException:
                logger.debug("- Close button is not displayed, skip clicking")

    # ------------------------ VERIFY ------------------------ #

    def verify_notification_banner(self, expected_title, expected_des=None):
        """Verify title and description of notification banner"""
        title = self.actions.find_element(self.__noti_title, raise_exception=False, timeout=SHORT_WAIT)
        des = self.actions.find_element(self.__noti_des, raise_exception=False, timeout=SHORT_WAIT)

        actual_title = title.text.strip() if title else ""
        actual_des = des.text.strip() if des else ""

        logger.debug(f"- Check noti_title equal: {expected_title!r}")
        soft_assert(actual_title, expected_title)

        if expected_des:
            logger.debug(f"- Check noti_des equal: {expected_des!r}")
            compare_noti_with_tolerance(actual_des, expected_des)

    def verify_notification_result(self, expected_result: str | list, go_back=True):
        self.open_notification_box()
        actual_res = self.actions.get_content_desc(self.__noti_list_items).split(", ")[0].replace("  ", " ")
        compare_noti_with_tolerance(actual_res, expected_result, is_banner=False)
        not go_back or self.go_back()

    def verify_notification_details(self, trade_object: ObjTrade):
        self.actions.click(self.__noti_list_items)

        actual = {
            "order_type": self.actions.get_text(self.__noti_details_order_type),
            "symbol": self.actions.get_text(self.__noti_details_symbol),
            "volume": self.actions.get_text(self.__noti_details_volume),
            "units": self.actions.get_text(self.__noti_details_units),
            "stop_loss": self.actions.get_text(self.__noti_details_stop_loss),
            "take_profit": self.actions.get_text(self.__noti_details_take_profit),
        }

        expected = {k: v for k, v in trade_object.items() if k in actual}
        expected["order_type"] = f"{trade_object.trade_type.upper()} ORDER"

        logger.debug("- Verify notification item details")
        soft_assert(actual, expected)
        self.go_back()
        time.sleep(0.5)
        self.go_back()
