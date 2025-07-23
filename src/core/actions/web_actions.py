import builtins
import time

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.core.actions.base_actions import BaseActions
from src.core.decorators import handle_stale_element
from src.data.consts import EXPLICIT_WAIT, SHORT_WAIT, QUICK_WAIT
from src.utils.assert_utils import soft_assert
from src.utils.logging_utils import logger


class WebActions(BaseActions):
    def __init__(self, driver=None):
        super().__init__(driver or builtins.web_driver)
        self._action_chains = ActionChains(self._driver)

    # ------- ACTIONS ------ #
    @handle_stale_element
    def send_keys(self, locator: tuple[str, str], value, timeout=EXPLICIT_WAIT, raise_exception=True, show_log=True):
        """Send keys to an element."""
        element = self.find_element(locator, timeout, raise_exception=raise_exception, show_log=show_log)
        if element:
            # Double click to select all text and ensure focus
            self._action_chains.double_click(element).perform()
            element.send_keys(str(value))

    @handle_stale_element
    def click_by_offset(
            self,
            locator: tuple[str, str],
            x_offset=0, y_offset=0,
            timeout=EXPLICIT_WAIT,
            raise_exception=True,
            show_log=True
    ) -> None:
        """Click on an element by an offset of x and y coordinates."""
        element = self.find_element(
            locator, timeout, EC.element_to_be_clickable,
            raise_exception=raise_exception,
            show_log=show_log
        )
        if element:
            self._action_chains.move_to_element_with_offset(element, x_offset, y_offset).click().perform()

    @handle_stale_element
    def get_value(
            self,
            locator: tuple[str, str],
            timeout=EXPLICIT_WAIT,
            retry=False,
    ) -> str:
        """Get value from an element."""
        element = self.find_element(locator, timeout, raise_exception=False, show_log=False)
        res = element.get_attribute("value") if element else ""

        if retry and not res:
            logger.debug("- Retry getting value")
            time.sleep(1)
            element = self.find_element(locator, QUICK_WAIT, raise_exception=False, show_log=False)
            res = element.get_attribute("value") if element else ""

        return res

    def goto(self, url):
        """Navigate to a URL and wait for the page to be fully loaded."""
        self._driver.get(url)

    def refresh(self):
        self._driver.refresh()

    def get_current_url(self):
        return self._driver.current_url

    def scroll_container_down(self, locator: tuple[str, str], wait_time: float = 0.5, scroll_step: float = 0.5):
        """Scroll a container element down by a smaller step to avoid missing items
        Args:
            locator: The locator of the container to scroll
            wait_time: Time to wait after scrolling for new content to load
            scroll_step: Fraction of container height to scroll (0.5 = half height, 0.25 = quarter height)
        """
        try:
            container = self.find_element(locator)
            self.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollTop + (arguments[0].clientHeight * arguments[1]);",
                container, scroll_step
            )
            time.sleep(wait_time)
        except Exception as e:
            logger.warning(f"Error scrolling container {locator}: {e}")

    def wait_for_url(self, url: str, timeout: int = EXPLICIT_WAIT, retries=1):
        """Wait for the current URL to match the expected URL with retry mechanism."""
        wait = self._wait if timeout == EXPLICIT_WAIT else WebDriverWait(self._driver, timeout)

        for i in range(retries):
            try:
                wait.until(EC.url_to_be(url))

            except TimeoutException as e:
                logger.warning(f"Attempt {i + 1}/{retries} failed for URL '{url}': {type(e).__name__}")

            except Exception as e:
                logger.error(f"Unexpected error for URL '{url}': {type(e).__name__}")

        return self._driver.current_url

    # ------- VERIFY ------ #

    def verify_site_url(self, expected_url: str, timeout: int = EXPLICIT_WAIT, retries: int = 1):
        """Verify that the current URL matches the expected URL with retry mechanism."""
        soft_assert(self.wait_for_url(expected_url, timeout, retries), expected_url, )
