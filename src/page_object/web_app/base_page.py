from selenium.webdriver.common.by import By

from src.core.actions.web_actions import WebActions
from src.core.config_manager import Config
from src.data.consts import EXPLICIT_WAIT, QUICK_WAIT
from src.data.enums import Features
from src.data.enums import URLSites
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element, data_testid
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
    __alert_box = (By.CSS_SELECTOR, data_testid("notification-box"))
    __alert_title = (By.CSS_SELECTOR, data_testid("notification-box-title"))
    __alert_desc = (By.CSS_SELECTOR, data_testid("notification-box-description"))
    __alert_box_close = (By.CSS_SELECTOR, data_testid("notification-box-close"))
    __btn_nav_back = (By.CSS_SELECTOR, data_testid("navigation-back-button"))
    __spin_loader = (By.CSS_SELECTOR, data_testid("spin-loader"))
    __btn_confirm = (By.XPATH, "//*[text()='Confirm']")
    __btn_cancel = (By.XPATH, "//*[text()='Cancel']")
    __home_nav_option = (By.CSS_SELECTOR, data_testid("side-bar-option-{}"))

    # ------------------------ ACTIONS ------------------------ #
    def goto(self, site: URLSites | str = URLSites.MEMBER_SITE):
        self.actions.goto(Config.urls(site))

    def wait_for_spin_loader(self, timeout: int | float = 5):
        """Wait for the loader to be invisible."""
        logger.debug("- Waiting for spin loader...")
        if self.actions.is_element_displayed(self.__spin_loader, timeout=timeout):
            logger.debug("- Wait for spin loader to disappear")
            self.actions.wait_for_element_invisible(self.__spin_loader, timeout=30)

    def navigate_to(self, feature: Features, wait=False):
        self.actions.click(cook_element(self.__home_nav_option, feature.lower()))
        if wait:
            self.wait_for_spin_loader()

    def click_confirm_btn(self):
        self.actions.click(self.__btn_confirm)

    def click_cancel_btn(self):
        while self.actions.is_element_displayed(self.__btn_cancel):
            logger.debug("- Click cancel btn")
            self.actions.click(self.__btn_cancel, raise_exception=False, timeout=QUICK_WAIT)

    def close_alert_box(self):
        self.actions.click(self.__alert_box_close)

    # ------------------------ VERIFY ------------------------ #
    def verify_alert_error_message(self, expected_message):
        actual_err = self.actions.get_text(self.__alert_desc, timeout=EXPLICIT_WAIT)
        soft_assert(actual_err, expected_message)
        self.close_alert_box()