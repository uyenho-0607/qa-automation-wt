import time
from contextlib import suppress

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import QUICK_WAIT, EXPLICIT_WAIT, SHORT_WAIT
from src.data.objects.trade_obj import ObjTrade
from src.page_object.android.base_screen import BaseScreen
from src.utils.assert_utils import soft_assert, compare_noti_with_tolerance
from src.utils.common_utils import resource_id
from src.utils.logging_utils import logger


class Notifications(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __noti_selector = (AppiumBy.XPATH, resource_id('notification-selector', "android.view.ViewGroup"))
    __tab_noti = (AppiumBy.XPATH, resource_id('tab-notification-type-{}'))
    __noti_des = (AppiumBy.XPATH, resource_id('notification-box-description'))
    __noti_title = (AppiumBy.XPATH, resource_id('notification-box-title'))
    __noti_list_items = (AppiumBy.XPATH, resource_id('notification-list-result-item'))
    __btn_close = (AppiumBy.XPATH, resource_id('notification-box-close'))

    # Noti order details
    __noti_details_order_type = (AppiumBy.XPATH, resource_id('notification-order-details-modal-order-type'))
    __noti_details_symbol = (
        AppiumBy.XPATH,
        "//*[@resource-id='notification-order-details-label' and @text='Symbol']/following-sibling::*[1]"
    )
    __noti_details_volume = (
        AppiumBy.XPATH,
        "//*[@resource-id='notification-order-details-label' and (@text='Size' or @text='Volume')]/following-sibling::*[1]"
    )
    __noti_details_units = (
        AppiumBy.XPATH,
        "//*[@resource-id='notification-order-details-label' and @text='Units']/following-sibling::*[1]"
    )
    __noti_details_stop_loss = (
        AppiumBy.XPATH,
        "//*[@resource-id='notification-order-details-label' and @text='Stop Loss']/following-sibling::*[1]"
    )
    __noti_details_take_profit = (
        AppiumBy.XPATH,
        "//*[@resource-id='notification-order-details-label' and @text='Take Profit']/following-sibling::*[1]"
    )

    # ------------------------ ACTIONS ------------------------ #
    def open_notification_box(self):
        if self.actions.is_element_displayed(self.__noti_selector):
            self.actions.click(self.__noti_selector)

    def close_noti_banner(self):
        with suppress(Exception):
            self.actions.click(self.__btn_close, timeout=SHORT_WAIT, raise_exception=False)

    # ------------------------ VERIFY ------------------------ #

    def verify_notification_banner(self, expected_title, expected_des, timeout=EXPLICIT_WAIT):
        """Verify title and description of notification banner"""
        # Execute sequentially instead of in parallel to avoid Device Farm connection pool issues
        logger.debug("- Fetching notification description")
        actual_des = self.actions.get_text(self.__noti_des, timeout=timeout)

        logger.debug("- Fetching notification title")
        actual_title = self.actions.get_text(self.__noti_title, timeout=QUICK_WAIT)

        logger.debug(f"> Check noti des = {expected_des!r}")
        compare_noti_with_tolerance(actual_des, expected_des)

        if actual_title:
            logger.debug(f"> Check noti title = {expected_title!r}")
            soft_assert(actual_title, expected_title)

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
