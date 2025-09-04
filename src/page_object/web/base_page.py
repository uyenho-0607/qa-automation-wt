from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.core.config_manager import Config
from src.data.consts import EXPLICIT_WAIT, SHORT_WAIT, QUICK_WAIT
from src.data.enums import Features
from src.data.enums import URLSites, URLPaths
from src.data.ui_messages import UIMessages
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import data_testid, cook_element, convert_strtime
from src.utils.logging_utils import logger


class BasePage:
    """Base class for all web pages providing common functionality.
    
    This class serves as the foundation for all page objects in the web application.
    It provides common functionality for:
    - Page navigation
    - Loading state management
    - Alert message handling
    """

    def __new__(cls, *args, **kwargs):
        actions = args[0] if args else kwargs.get('actions')
        if not isinstance(actions, WebActions):
            raise TypeError("First argument must be an instance of WebActions")

        # Create class-specific instances dictionary if it doesn't exist
        if not hasattr(cls, '_instances'):
            cls._instances = {}

        session_id = actions._driver.session_id
        if session_id not in cls._instances:
            cls._instances[session_id] = super(BasePage, cls).__new__(cls)
        return cls._instances[session_id]

    def __init__(self, actions: WebActions):
        """Initialize the base page.
        
        Args:
            actions (WebActions): The web actions instance for interacting with the page
        """
        if not hasattr(self, 'initialized'):
            self.actions = actions
            self.initialized = True

    # ------------------------ LOCATORS ------------------------ #
    __spin_loader = (By.CSS_SELECTOR, data_testid('spin-loader'))
    __alert_error = (By.CSS_SELECTOR, data_testid('alert-error'))
    __alert_success = (By.CSS_SELECTOR, data_testid('alert-success'))
    __locator_by_text = (By.XPATH, "//*[contains(text(), '{}')]")
    __empty_message = (By.CSS_SELECTOR, data_testid('empty-message'))
    __side_bar_option = (By.CSS_SELECTOR, data_testid('side-bar-option-{}'))
    __server_time = (By.XPATH, "//span[text()='Server Time' or text()='Device Time']/span")

    # ------------------------ ACTIONS ------------------------ #
    def goto(self, site: URLSites | str = URLSites.MEMBER_SITE):
        self.actions.goto(Config.urls(site))

    def navigate_to(self, feature: Features, wait=False):
        """Navigate to a specific feature using the sidebar"""
        self.actions.click(cook_element(self.__side_bar_option, feature.lower()))
        not wait or self.wait_for_spin_loader(timeout=SHORT_WAIT)

    def wait_for_spin_loader(self, timeout: int = 5):
        """Wait for the loader to be invisible."""
        if self.actions.is_element_displayed(self.__spin_loader, timeout=timeout):
            logger.debug("- Wait for loading icon to disappear...")
            self.actions.wait_for_element_invisible(self.__spin_loader, timeout=15)

    def refresh_page(self):
        logger.debug("- Refresh page...")
        self.actions.refresh()
        self.wait_for_spin_loader()

    def is_current_page(self, url_path: URLPaths):
        return f"/{url_path.lower()}" in self.actions.get_current_url()

    def get_server_device_time(self, trade_object, convert_time=True):
        server_time = self.actions.get_text(self.__server_time, timeout=QUICK_WAIT)

        logger.debug(f"- Server/ Device time: {server_time!r}")
        server_time = server_time if not convert_time else convert_strtime(server_time)

        if not trade_object.get("open_date"):
            trade_object.open_date = server_time

        else:
            trade_object.close_date = server_time

    # ------------------------ VERIFY ------------------------ #
    def verify_page_url(self, url_path: str = None, custom_url="", timeout: int = EXPLICIT_WAIT):
        """Verify that the current URL matches the expected page URL."""
        expected_url = Config.url_path(url_path) if url_path is not None else custom_url
        self.actions.verify_site_url(expected_url, timeout=timeout)

    def verify_alert_error_message(self, expected_message: UIMessages | str, other_msg=None, timeout=20):
        """Verify the error alert message."""
        actual_err = self.actions.get_text(self.__alert_error, timeout=timeout)
        if not other_msg:
            soft_assert(actual_err, expected_message)

        else:
            res = actual_err in [expected_message, other_msg]
            logger.debug(f"- Actual error msg: {actual_err!r}, expected error msg: {expected_message!r}, other expected msg: {other_msg!r}")
            soft_assert(res, True, error_message=f"Actual:{actual_err!r}, Expected: {expected_message} or {other_msg}")

    def verify_alert_success_message(self, expected_message: UIMessages):
        """Verify the success alert message."""
        actual_msg = self.actions.get_text(self.__alert_success)
        soft_assert(actual_msg, expected_message)

    def verify_text_content(self, *expected_text):
        for tex in expected_text:
            locator = cook_element(self.__locator_by_text, tex)
            self.actions.verify_element_displayed(locator)

    def verify_empty_message(self, locator=None, expected_text=""):
        locator = locator or self.__empty_message
        logger.debug("- Check empty message locator is displayed")
        self.actions.verify_elements_displayed(locator)

        if expected_text:
            logger.info(f"- Check empty message equal to: {expected_text}")
            actual = self.actions.get_text(locator).replace(".", "")
            soft_assert(actual, expected_text)
