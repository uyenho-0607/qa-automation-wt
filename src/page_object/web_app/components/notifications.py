from contextlib import suppress

from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.data.consts import QUICK_WAIT, EXPLICIT_WAIT, SHORT_WAIT
from src.data.objects.trade_obj import ObjTrade
from src.page_object.web_app.base_page import BasePage
from src.utils.assert_utils import soft_assert, compare_noti_with_tolerance
from src.utils.common_utils import data_testid, cook_element
from src.utils.logging_utils import logger


class Notifications(BasePage):
    def __init__(self, actions: WebActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __noti_selector = (By.CSS_SELECTOR, data_testid('notification-selector', ))
    __tab_noti = (By.CSS_SELECTOR, data_testid('tab-notification-type-{}'))
    __noti_des = (By.CSS_SELECTOR, data_testid('notification-box-description'))
    __noti_title = (By.CSS_SELECTOR, data_testid('notification-box-title'))
    __noti_list_items = (By.CSS_SELECTOR, data_testid('notification-list-result-item'))
    __btn_close = (By.CSS_SELECTOR, data_testid('navigation-back-button'))
    __btn_close_banner = (By.CSS_SELECTOR, data_testid('notification-box-close'))

    __noti_result = (By.XPATH, "//div[@data-testid='notification-list-result-item' and contains(normalize-space(), '{}')]")

    # Noti order details
    __noti_details_order_type = (By.CSS_SELECTOR, data_testid('notification-order-details-modal-order-type'))
    __noti_details_symbol = (
        By.XPATH,
        "//*[@resource-id='notification-order-details-label' and @text='Symbol']/following-sibling::*[1]"
    )
    __noti_details_volume = (
        By.XPATH,
        "//*[@resource-id='notification-order-details-label' and (@text='Size' or @text='Volume')]/following-sibling::*[1]"
    )
    __noti_details_units = (
        By.XPATH,
        "//*[@resource-id='notification-order-details-label' and @text='Units']/following-sibling::*[1]"
    )
    __noti_details_stop_loss = (
        By.XPATH,
        "//*[@resource-id='notification-order-details-label' and @text='Stop Loss']/following-sibling::*[1]"
    )
    __noti_details_take_profit = (
        By.XPATH,
        "//*[@resource-id='notification-order-details-label' and @text='Take Profit']/following-sibling::*[1]"
    )

    # ------------------------ ACTIONS ------------------------ #
    def close_noti_box(self):
        if self.actions.is_element_displayed(self.__btn_close):
            self.actions.click(self.__btn_close)

    def open_noti_box(self, wait=True):
        if self.actions.is_element_displayed(self.__noti_selector):
            self.actions.click(self.__noti_selector)
        not wait or self.wait_for_spin_loader(timeout=3)

    def close_noti_banner(self):
        with suppress(Exception):
            self.actions.click(self.__btn_close, timeout=SHORT_WAIT, raise_exception=False)

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

    def verify_notification_result(self, expected_result: str | list, close=False):
        self.open_noti_box()
        if "Open Position" in expected_result:
            noti_res = self._get_open_position()

        elif "Position Closed" in expected_result:
            noti_res = self._get_position_closed()

        else:
            noti_res = self.actions.get_text(self.__noti_list_items)

        actual_res = noti_res.split(", ")[0].replace("  ", " ")
        actual_res = actual_res.split("\n")[0]

        compare_noti_with_tolerance(actual_res, expected_result, is_banner=False)
        if close:
            self.close_noti_box()

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
