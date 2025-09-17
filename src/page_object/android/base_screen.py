from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.consts import EXPLICIT_WAIT, SHORT_WAIT
from src.data.enums import Features
from src.data.ui_messages import UIMessages
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element
from src.utils.logging_utils import logger


class BaseScreen:
    """Base class for all web pages providing common functionality.

    This class serves as the foundation for all page objects in the web application.
    It provides common functionality for:
    - Page navigation
    - Loading state management
    - Alert message handling
    """

    def __new__(cls, *args, **kwargs):
        actions = args[0] if args else kwargs.get('actions')
        if not isinstance(actions, MobileActions):
            raise TypeError("First argument must be an instance of WebActions")

        # Create class-specific instances dictionary if it doesn't exist
        if not hasattr(cls, '_instances'):
            cls._instances = {}

        session_id = actions._driver.session_id
        if session_id not in cls._instances:
            cls._instances[session_id] = super(BaseScreen, cls).__new__(cls)
        return cls._instances[session_id]

    def __init__(self, actions: MobileActions):
        """Initialize the base page.

        Args:
            actions (WebActions): The web actions instance for interacting with the page
        """
        if not hasattr(self, 'initialized'):
            self.actions = actions
            self.initialized = True

    # ------------------------ LOCATORS ------------------------ #
    __alert_success = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("alert-success")')
    __alert_desc = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("notification-box-description")')
    __alert_box_close = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("notification-box-close")')
    __btn_nav_back = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("navigation-back-button")')
    __spin_loader = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("spin-loader")')
    __opt_home_nav = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("home-nav-option-{}")')
    __opt_side_bar = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("side-bar-option-{}")')
    __btn_confirm = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textMatches("(?i)confirm")')
    __btn_cancel = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textMatches("(?i)cancel")')
    __btn_ok = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("OK")')

    # ------------------------ ACTIONS ------------------------ #
    def click_ok_btn(self):
        self.actions.click_if_displayed(self.__btn_ok)

    def go_back(self):
        self.actions.click(self.__btn_nav_back)

    def wait_for_spin_loader(self, timeout: int = 10):
        """Wait for the loader to be invisible."""
        if self.actions.is_element_displayed(self.__spin_loader, timeout=SHORT_WAIT):
            logger.debug("- Wait for loading icon to disappear...")
            self.actions.wait_for_element_invisible(self.__spin_loader, timeout=timeout)

    def navigate_to(self, feature: Features, wait=False):
        locator = self.__opt_home_nav if feature in feature.home_nav_list() else self.__opt_side_bar
        self.actions.click(cook_element(locator, feature.lower()))
        not wait or self.wait_for_spin_loader()

    def click_confirm_btn(self):
        self.actions.click(self.__btn_confirm)

    def click_cancel_btn(self, timeout=SHORT_WAIT):
        max_retries = 5
        while self.actions.is_element_displayed(self.__btn_cancel) and max_retries:
            logger.debug("- Click cancel btn")
            self.actions.javascript_click(self.__btn_cancel, raise_exception=False, timeout=timeout, show_log=False)
            max_retries -= 1

    def close_alert_box(self):
        if self.actions.is_element_displayed(self.__alert_box_close):
            self.actions.click(self.__alert_box_close)

    # ------------------------ VERIFY ------------------------ #
    def verify_alert_error_message(self, expected_message: UIMessages):
        actual_err = self.actions.get_text(self.__alert_desc, timeout=EXPLICIT_WAIT)
        soft_assert(actual_err, expected_message)
        self.close_alert_box()

    def verify_alert_success_message(self, expected_message: UIMessages):
        actual_msg = self.actions.get_text(self.__alert_success)
        soft_assert(actual_msg, expected_message)
        self.close_alert_box()

    def verify_alert_message(self, expected_message: UIMessages):
        """Verify the success alert message.
        
        Args:
            expected_message (UIMessages): The expected success message
        """
        actual_msg = self.actions.get_text(self.__alert_desc)
        soft_assert(actual_msg, expected_message)
        self.close_alert_box()
