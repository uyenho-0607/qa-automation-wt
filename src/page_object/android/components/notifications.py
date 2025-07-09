import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import QUICK_WAIT
from src.page_object.android.base_screen import BaseScreen
from src.utils import DotDict
from src.utils.assert_utils import soft_assert
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
    __noti_details_entry_price = (
        AppiumBy.XPATH,
        "//*[@resource-id='notification-order-details-label' and @text='Entry Price']/following-sibling::*[1]"
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
        if self.actions.is_element_displayed(self.__btn_close, timeout=QUICK_WAIT):
            try:
                self.actions.click(self.__btn_close, show_log=False, raise_exception=False)

            except TimeoutException:
                logger.debug("- Close button is not displayed, skip clicking")

    # ------------------------ VERIFY ------------------------ #

    def verify_notification_banner(self, expected_title, expected_des=None):
        """
        Verify title and description of notification banner
        Give trade_object in case load entr_price value from noti >> trade_object
        """
        actual_title = self.actions.get_text(self.__noti_title)
        actual_des = self.actions.get_text(self.__noti_des)

        logger.debug(f"- Check noti_title equal: {expected_title!r}")
        soft_assert(actual_title, expected_title)

        if expected_des:
            logger.debug(f"- Check noti_des equal: {expected_des!r}")
            soft_assert(actual_des, expected_des)

    def verify_notification_result(self, expected_result: str | list, go_back=True):
        self.open_notification_box()
        actual_res = self.actions.get_content_desc(self.__noti_list_items).replace("  ", " ")
        soft_assert(actual_res, expected_result, check_contains=True)
        not go_back or self.go_back()

    def verify_notification_details(self, trade_object: DotDict):
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
