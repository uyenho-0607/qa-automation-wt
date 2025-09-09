import re
import time
from contextlib import suppress

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.enums import NotificationTab
from src.data.consts import QUICK_WAIT, EXPLICIT_WAIT, SHORT_WAIT
from src.data.objects.trade_obj import ObjTrade
from src.page_object.android.base_screen import BaseScreen
from src.utils.assert_utils import soft_assert, compare_noti_with_tolerance
from src.utils.format_utils import locator_format, extract_asset_tab_number
from src.utils.common_utils import resource_id, cook_element
from src.utils.logging_utils import logger


class Notifications(BaseScreen):
    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __btn_nav_back = (AppiumBy.XPATH, "//*[@resource-id='navigation-back-button']")

    __noti_selector = (AppiumBy.XPATH, resource_id('notification-selector', "android.view.ViewGroup"))
    __tab_noti = (AppiumBy.XPATH, resource_id('tab-notification-type-{}'))
    __tab_amount = (AppiumBy.XPATH, "//*[@resource-id='tab-notification-type-{}' and contains(@content-desc, '({})')]")

    __noti_des = (AppiumBy.XPATH, resource_id('notification-box-description'))
    __noti_title = (AppiumBy.XPATH, resource_id('notification-box-title'))
    __noti_list_items = (AppiumBy.XPATH, resource_id('notification-list-result-item'))
    __btn_close = (AppiumBy.XPATH, resource_id('notification-box-close'))

    __noti_by_text = (AppiumBy.XPATH, "//*[@resource-id='notification-list-result-item']/android.widget.TextView[@text='{}']")
    __noti_result = (AppiumBy.XPATH, "//*[@resource-id='notification-list-result-item' and contains(@content-desc, '{}')]")

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

    #### SYSTEM ####
    __system_tab = (AppiumBy.XPATH, resource_id('tab-notification-type-system'))

    # ------------------------ ACTIONS ------------------------ #

    def navigate_back_to_home(self):
        """
        Attempts to navigate back to the Home screen by pressing the back button.
        Will stop early if the Home screen is detected.
        """
        max_attempts = 3

        for attempt in range(1, max_attempts + 1):
            # Check if Home screen is visible
            if self.actions.is_element_displayed(self.__noti_selector, timeout=SHORT_WAIT):
                logger.debug(f"- Home Screen displayed, stop navigation")
                break

            # If back button is visible, click it
            if self.actions.is_element_displayed(self.__btn_nav_back, timeout=SHORT_WAIT):
                logger.debug(f"- Clicking back (<) button to return to Home tab (attempt {attempt})")
                self.actions.click(self.__btn_nav_back)

        logger.warning(f"- Failed to navigate back to Home after max {max_attempts} attempts")


    def open_notification_box(self):
        if self.actions.is_element_displayed(self.__noti_selector):
            self.actions.click(self.__noti_selector)

    def clear_notification_count(self):
        self.open_notification_box()
        self.actions.click(cook_element(self.__tab_noti))

    def wait_for_tab_amount(self, tab: NotificationTab, expected_amount: int) -> None:
        """Wait for the asset tab amount to match the expected amount."""
        self.actions.wait_for_element_visible(
            cook_element(self.__tab_amount, locator_format(tab), expected_amount)
        )

    def get_tab_amount(self, tab: NotificationTab, wait=True) -> int:
        """Get the number of items in the specified tab."""
        not wait or self.wait_for_spin_loader(timeout=3)
        amount = self.actions.get_content_desc(cook_element(self.__tab_noti, locator_format(tab)))
        return extract_asset_tab_number(amount)

    def close_noti_banner(self):
        with suppress(Exception):
            self.actions.click(self.__btn_close, timeout=SHORT_WAIT, raise_exception=False)

    def _get_open_position(self):
        noti = cook_element(self.__noti_result, "Open Position")
        return self.actions.get_content_desc(noti)

    def _get_position_closed(self):
        noti = cook_element(self.__noti_result, "Position Closed")
        return self.actions.get_content_desc(noti)

    # ------------------------ VERIFY ------------------------ #
    def verify_tab_amount(self, tab: NotificationTab, expected_amount: int) -> None:
        """Verify that the tab amount matches the expected amount."""
        self.open_notification_box()
        self.wait_for_tab_amount(tab, expected_amount)
        soft_assert(self.get_tab_amount(tab, wait=False), expected_amount)
        self.go_back()


    def verify_notification_banner(self, expected_title, expected_des, timeout=EXPLICIT_WAIT):
        """Verify title and description of notification banner"""
        # Execute sequentially instead of in parallel to avoid Device Farm connection pool issues
        logger.debug("- Fetching notification description")
        actual_des = self.actions.get_text(self.__noti_des, timeout=timeout)

        logger.debug("- Fetching notification title")
        actual_title = self.actions.get_text(self.__noti_title, timeout=QUICK_WAIT)

        logger.debug(f"- Check noti des - {expected_des!r}")
        compare_noti_with_tolerance(actual_des, expected_des)

        if actual_title:
            logger.debug(f"- Check noti title - {expected_title!r}")
            soft_assert(actual_title, expected_title)

    def verify_notification_result(self, expected_result: str | list, is_system=False, go_back=True):
        # currently, we have 2 types of noti: open position and position closed in notification box
        self.open_notification_box()

        if is_system:
            time.sleep(0.5)
            self.actions.click(self.__system_tab)
            for noti in expected_result:
                locator = cook_element(self.__noti_by_text, noti)
                self.actions.verify_element_displayed(locator)
            return

        if "Open Position" in expected_result:
            noti_res = self._get_open_position()

        elif "Position Closed" in expected_result:
            noti_res = self._get_position_closed()

        else:
            noti_res = self.actions.get_text(self.__noti_list_items)

        actual_res = noti_res.split(", ")[0].replace("  ", " ")
        actual_res = actual_res.split("\n")[0]

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
        self.navigate_back_to_home()
