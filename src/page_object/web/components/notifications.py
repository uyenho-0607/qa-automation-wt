import re
import time

from selenium.webdriver.common.by import By

from src.data.consts import SHORT_WAIT, EXPLICIT_WAIT
from src.page_object.web.base_page import BasePage
from src.utils import DotDict
from src.utils.assert_utils import soft_assert, compare_noti_with_tolerance
from src.utils.common_utils import data_testid, cook_element
from src.utils.logging_utils import logger


class Notifications(BasePage):
    def __init__(self, actions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __noti_selector = (By.CSS_SELECTOR, data_testid('notification-selector'))
    __noti_result = (By.CSS_SELECTOR, "*[data-testid='notification-dropdown-result']")
    __noti_des = (By.CSS_SELECTOR, "*[data-testid='notification-description']")
    __noti_title = (By.CSS_SELECTOR, "*[data-testid='notification-title']")
    __noti_list = (By.CSS_SELECTOR, data_testid('notification-list-result'))
    __noti_list_items = (By.CSS_SELECTOR, data_testid('notification-list-result-item'))
    __noti_list_item_by_text = (
        By.XPATH,
        "//div[@data-testid='notification-list-result-item' "
        "and (contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{}'))]"
        # should custom with 'position closed: #order_id' or 'open position: #order_id'
    )
    __noti_by_text = (By.XPATH, "//div[contains(text(), '{}')]")
    __btn_close = (By.CSS_SELECTOR, "*[data-testid='notification-close-button']")

    #### SYSTEM ####
    __system_tab = (By.CSS_SELECTOR, data_testid('tab-notification-type-system'))

    # ------------------------ ACTIONS ------------------------ #
    def toggle_notification(self, close=False, timeout=1):
        is_open = self.actions.is_element_displayed(self.__noti_result, timeout=timeout)
        if (not close and not is_open) or (close and is_open):
            self.actions.click(self.__noti_selector)

    def close_noti_banner(self):
        if self.actions.is_element_displayed(self.__btn_close, timeout=SHORT_WAIT):
            self.actions.click(self.__btn_close)

    def get_open_position_order_id(self, trade_object: DotDict, amount=1):
        self.toggle_notification(timeout=1)

        noti_items = self.actions.find_elements(self.__noti_list_items)
        order_ids = []
        for i in range(amount):
            ord_id = re.search(r'#(\d+)', noti_items[i].text)
            order_ids.append(ord_id.group(1))

        logger.debug(f"- order_id: {order_ids}")
        trade_object.order_id = order_ids[0] if amount == 1 else order_ids
        self.toggle_notification(timeout=1, close=True)

    # ------------------------ VERIFY ------------------------ #

    def verify_notification_banner(self, expected_title, expected_des=None, close_banner=False):
        """
        Verify title and description of notification banner
        Give trade_object in case load entr_price value from noti >> trade_object
        """
        actual_title = self.actions.get_text(self.__noti_title, timeout=EXPLICIT_WAIT)
        logger.debug(f"- Check noti_title equal: {expected_title!r}")
        soft_assert(actual_title, expected_title)

        if expected_des:
            actual_des = self.actions.get_text(self.__noti_des, timeout=EXPLICIT_WAIT)
            res = compare_noti_with_tolerance(actual_des, expected_des, tolerance_percent=0.01)

            logger.debug(f"- Check noti_des equal: {expected_des!r}")
            soft_assert(res, True, error_message=f"Actual: {actual_des}, Expected: {expected_des}")

        if close_banner:
            self.close_noti_banner()

    def verify_notification_result(self, expected_result: str | list, check_contains=False, is_system=False):
        # currently, we have 2 types of noti: open position and position closed in notification box
        self.toggle_notification(timeout=2)
        if is_system:
            time.sleep(0.5)
            self.actions.click(self.__system_tab)
            for noti in expected_result:
                locator = cook_element(self.__noti_by_text, noti)
                self.actions.verify_element_displayed(locator)

            return

        prefix = "position closed"
        if "open" in expected_result.lower():
            prefix = "open position"

        ord_id = re.search(r'#(\d+)', expected_result)
        if ord_id:
            ord_id = ord_id.group(1)

        actual_res = self.actions.get_text(
            cook_element(self.__noti_list_item_by_text, f'{prefix}: #{ord_id}'), timeout=EXPLICIT_WAIT
        )

        actual_res = actual_res.split(",")[0]

        res = compare_noti_with_tolerance(actual_res, expected_result, tolerance_percent=0.01)
        soft_assert(res, True, error_message=f"Actual: {actual_res}, Expected: {expected_result}")

        self.toggle_notification(close=True)
