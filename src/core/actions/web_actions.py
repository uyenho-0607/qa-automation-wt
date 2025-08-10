import builtins
import html
import time
from typing import Literal

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.core.actions.base_actions import BaseActions
from src.core.decorators import handle_stale_element
from src.data.consts import EXPLICIT_WAIT, QUICK_WAIT
from src.utils.assert_utils import soft_assert
from src.utils.logging_utils import logger


class WebActions(BaseActions):
    """Web-specific actions implementation."""
    
    def __init__(self, driver=None):
        super().__init__(driver or builtins.web_driver)
        self._action_chains = ActionChains(self._driver)

    # ------- ACTIONS ------ #
    def _send_key_action_chains(
            self, 
            value: str, 
            locator: tuple[str, str] = None, 
            element: WebElement = None, 
            timeout: float | int = EXPLICIT_WAIT
    ) -> None:
        """Send keys using ActionChains."""
        if locator:
            element = self.find_element(locator, timeout)
        
        if element:
            self._action_chains.double_click(element).send_keys(Keys.DELETE).perform()
            self._action_chains.send_keys_to_element(element, str(value)).perform()
    
    def _send_keys(
            self, 
            value: str, 
            locator: tuple[str, str] = None, 
            element: WebElement = None, 
            timeout: float | int = EXPLICIT_WAIT
    ) -> None:
        """Send keys directly to element."""
        if locator:
            element = self.find_element(locator, timeout)
        
        if element:
            self._action_chains.double_click(element).perform()
            element.send_keys(str(value))

    @handle_stale_element
    def send_keys(
            self, 
            locator: tuple[str, str], 
            value: str, 
            use_action_chain: bool = False, 
            timeout: float | int = EXPLICIT_WAIT
    ) -> None:
        """Send keys to an element with retry mechanism."""
        element = self.find_element(locator, timeout)
        if not element:
            return
        
        send_key_func = self._send_key_action_chains if use_action_chain else self._send_keys
        send_key_func(value, element=element)
        
        # Retry mechanism for value verification
        max_retries = 3
        sent_value = element.get_attribute("value")
        while sent_value != str(value) and max_retries > 0:
            send_key_func(value, element=element)
            max_retries -= 1
            sent_value = element.get_attribute("value")

    @handle_stale_element
    def click_by_offset(
            self,
            locator: tuple[str, str],
            x_offset: int = 0, 
            y_offset: int = 0,
            timeout: float | int = EXPLICIT_WAIT,
            raise_exception: bool = True,
            show_log: bool = True
    ) -> None:
        """Click on an element by an offset of x and y coordinates."""
        element = self.find_element(locator, timeout, EC.element_to_be_clickable, raise_exception, show_log)
        if element:
            self._action_chains.move_to_element_with_offset(element, x_offset, y_offset).click().perform()

    @handle_stale_element
    def get_value(
            self,
            locator: tuple[str, str],
            timeout: float | int = EXPLICIT_WAIT,
            retry: bool = False,
    ) -> str:
        """Get value from an element."""
        element = self.find_element(locator, timeout, raise_exception=False, show_log=False)
        result = element.get_attribute("value") if element else ""
        
        if retry and not result:
            logger.debug("- Retry getting value")
            time.sleep(1)
            element = self.find_element(locator, QUICK_WAIT, raise_exception=False, show_log=False)
            result = element.get_attribute("value") if element else ""
        
        return result

    def goto(self, url: str) -> None:
        """Navigate to a URL."""
        self._driver.get(url)
    
    def refresh(self) -> None:
        """Refresh the current page."""
        self._driver.refresh()
    
    def get_current_url(self) -> str:
        """Get the current page URL."""
        return self._driver.current_url

    def scroll_to_element(self, locator: tuple[str, str], timeout: float | int = EXPLICIT_WAIT) -> None:
        """Scroll to element smoothly."""
        element = self.find_element(locator, timeout)
        if element:
            self._driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    def scroll_picker_down(self, locator: tuple[str, str], timeout: float | int = EXPLICIT_WAIT) -> None:
        """Scroll picker wheel down."""
        wheel = self.find_element(locator, timeout)
        if wheel:
            self._action_chains.click_and_hold(wheel).move_by_offset(0, -50).release().pause(0.5).perform()

    def scroll_container_down(self, locator: tuple[str, str], scroll_step: float = 0.5) -> None:
        """Scroll a container element down by a smaller step to avoid missing items."""
        try:
            container = self.find_element(locator)
            if container:
                self._driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollTop + (arguments[0].clientHeight * arguments[1]);",
                    container, scroll_step
                )
                time.sleep(0.3)
        except (TimeoutException, Exception) as e:
            safe_locator = html.escape(str(locator))
            logger.warning(f"Error scrolling container {safe_locator}: {type(e).__name__}")

    def drag_element_horizontal(
            self, 
            locator: tuple[str, str], 
            direction: Literal["left", "right"] = "left", 
            timeout: float | int = EXPLICIT_WAIT
    ) -> None:
        """Drag element horizontally."""
        x_offset = -200 if direction == "left" else 200
        element = self.find_element(locator, timeout)
        
        if element:
            finger = PointerInput("touch", "finger")
            action = ActionBuilder(self._driver, mouse=finger)
            action.pointer_action.move_to(element)
            action.pointer_action.pointer_down()
            action.pointer_action.move_by(x=x_offset, y=0)
            action.pointer_action.pointer_up()
            action.perform()

    def wait_for_url(self, url: str, timeout: float | int = EXPLICIT_WAIT, retries: int = 1) -> str:
        """Wait for the current URL to match the expected URL with retry mechanism."""
        wait = self._wait if timeout == EXPLICIT_WAIT else WebDriverWait(self._driver, timeout)
        
        for attempt in range(retries):
            try:
                wait.until(EC.url_to_be(url))
                break
            except TimeoutException:
                safe_url = html.escape(str(url))
                logger.warning(f"Attempt {attempt + 1}/{retries} failed for URL '{safe_url}': TimeoutException")
            except Exception as e:
                safe_url = html.escape(str(url))
                logger.error(f"Unexpected error for URL '{safe_url}': {type(e).__name__}")
                break
        
        return self._driver.current_url

    # ------- VERIFY ------ #
    def verify_site_url(self, expected_url: str, timeout: float | int = EXPLICIT_WAIT, retries: int = 1) -> None:
        """Verify that the current URL matches the expected URL with retry mechanism."""
        actual_url = self.wait_for_url(expected_url, timeout, retries)
        soft_assert(actual_url, expected_url)
