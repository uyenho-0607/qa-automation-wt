import html
from typing import Optional

from selenium.common import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.core.decorators import handle_stale_element
from src.data.consts import EXPLICIT_WAIT, QUICK_WAIT, SHORT_WAIT, IMPLICIT_WAIT
from src.data.project_info import StepLogs
from src.utils.allure_utils import attach_screenshot
from src.utils.assert_utils import soft_assert
from src.utils.logging_utils import logger


class ElementNotFoundError(Exception):
    """Custom exception for element not found scenarios."""
    pass


class BaseActions:
    """Base class for all platform-specific actions."""
    
    DEFAULT_CONDITION = EC.visibility_of_element_located

    def __init__(self, driver):
        self._driver = driver
        self._wait = WebDriverWait(driver=self._driver, timeout=EXPLICIT_WAIT)
        self._driver.implicitly_wait(IMPLICIT_WAIT)

    def find_element(
            self,
            locator: tuple[str, str],
            timeout: float | int = EXPLICIT_WAIT,
            cond=DEFAULT_CONDITION,
            raise_exception: bool = True,
            show_log: bool = True
    ) -> Optional[WebElement]:
        """Find single element using WebDriverWait.
        
        Args:
            locator: Element locator tuple (By, value)
            timeout: Timeout for WebDriverWait
            cond: Expected condition for finding element
            raise_exception: Whether to raise exception if element not found
            show_log: Whether to log warning if element not found
            
        Returns:
            WebElement if found, None otherwise
        """
        wait = self._wait if timeout == EXPLICIT_WAIT else WebDriverWait(self._driver, timeout)

        try:
            return wait.until(cond(locator))
        except StaleElementReferenceException:
            logger.debug("- Stale element detected, retrying...")
            return wait.until(cond(locator))
        except (TimeoutException, NoSuchElementException) as e:
            return self._handle_element_not_found(locator, e, timeout, raise_exception, show_log)
        except Exception as e:
            safe_locator = html.escape(str(locator))
            logger.error(f"Unexpected error for {safe_locator}: {type(e).__name__}")
            if raise_exception:
                self._capture_failure_info()
                raise ElementNotFoundError(f"Element with locator {safe_locator} not found")
            return None

    def find_elements(self, locator: tuple[str, str], timeout: float | int = EXPLICIT_WAIT) -> list[WebElement]:
        """Find list of elements using WebDriverWait.
        
        Args:
            locator: Element locator tuple (By, value)
            timeout: Timeout for WebDriverWait
            
        Returns:
            List of WebElements or empty list if not found
        """
        try:
            result = self.find_element(
                locator, timeout, EC.presence_of_all_elements_located, raise_exception=False, show_log=False
            )
            return result or []
        except StaleElementReferenceException:
            logger.debug("- Stale element detected while finding elements, retrying...")
            result = self.find_element(
                locator, timeout, EC.presence_of_all_elements_located, raise_exception=False, show_log=False
            )
            return result or []

    @handle_stale_element
    def click(
            self,
            locator: tuple[str, str],
            timeout: float | int = EXPLICIT_WAIT,
            raise_exception: bool = True,
            show_log: bool = True,
    ) -> None:
        """Click on an element."""
        element = self.find_element(
            locator, timeout, EC.element_to_be_clickable, raise_exception, show_log
        )
        if element:
            element.click()

    @handle_stale_element
    def javascript_click(
            self,
            locator: tuple[str, str],
            timeout: float | int = EXPLICIT_WAIT,
            raise_exception: bool = True,
            show_log: bool = True,
    ) -> None:
        """Click on an element using JavaScript."""
        element = self.find_element(locator, timeout, EC.element_to_be_clickable, raise_exception, show_log)
        if element:
            self._driver.execute_script("arguments[0].click();", element)

    def click_if_displayed(self, locator: tuple[str, str], timeout: float | int = QUICK_WAIT) -> None:
        """Click element only if it's displayed."""
        if self.is_element_displayed(locator, timeout):
            self.click(locator, timeout=timeout)

    def click_by_offset(self, **kwargs) -> None:
        """Platform-specific implementation required."""
        raise NotImplementedError("Subclasses must implement click_by_offset")

    def send_keys(self, **kwargs) -> None:
        """Platform-specific implementation required."""
        raise NotImplementedError("Subclasses must implement send_keys")

    @handle_stale_element
    def clear_field(
            self,
            locator: tuple[str, str],
            timeout: float | int = EXPLICIT_WAIT,
            raise_exception: bool = True,
            show_log: bool = True
    ) -> None:
        """Clear field using Ctrl+A (Cmd+A on Mac) and Delete."""
        element = self.find_element(locator, timeout, EC.element_to_be_clickable, raise_exception, show_log)
        if element:
            element.click()
            key = self._get_select_all_key()
            element.send_keys(key + "a")
            element.send_keys(Keys.DELETE)

    @handle_stale_element
    def get_attribute(
            self,
            locator: tuple[str, str],
            attribute: str,
            timeout: float | int = EXPLICIT_WAIT,
            raise_exception: bool = True,
            show_log: bool = True
    ) -> Optional[str]:
        """Get attribute value from an element."""
        element = self.find_element(locator, timeout, EC.presence_of_element_located, raise_exception, show_log)
        return element.get_attribute(attribute) if element else None

    @handle_stale_element
    def get_text_elements(self, locator: tuple[str, str], timeout: float | int = SHORT_WAIT) -> list[str]:
        """Get text of elements having same locator."""
        elements = self.find_elements(locator, timeout)
        return [ele.text.strip() if ele else "" for ele in elements]

    @handle_stale_element
    def get_text(
            self,
            locator: tuple[str, str],
            timeout: float | int = SHORT_WAIT,
            raise_exception: bool = False,
            show_log: bool = True,
    ) -> str:
        """Get text from element."""
        element = self.find_element(locator, timeout, raise_exception=raise_exception, show_log=show_log)
        if not element:
            logger.debug("- Retry getting text")
            element = self.find_element(locator, QUICK_WAIT, raise_exception=raise_exception, show_log=show_log)
        return element.text.strip() if element else ""

    def wait_for_element_invisible(
            self,
            locator: tuple[str, str],
            timeout: float | int = EXPLICIT_WAIT,
    ) -> None:
        """Wait for element to be invisible."""
        wait = self._wait if timeout == EXPLICIT_WAIT else WebDriverWait(self._driver, timeout=timeout)
        element = self.find_element(locator, SHORT_WAIT, raise_exception=False, show_log=False)
        
        if element:
            try:
                wait.until(EC.invisibility_of_element_located(locator))
            except (TimeoutException, NoSuchElementException):
                logger.debug(f"Element {html.escape(str(locator))} visibility timeout - continuing")

    def wait_for_element_visible(
            self,
            locator: tuple[str, str],
            timeout: float | int = EXPLICIT_WAIT,
    ) -> None:
        """Wait for element to be visible."""
        self.find_element(locator, timeout, EC.visibility_of_element_located, raise_exception=False, show_log=True)

    def is_element_displayed(
            self, 
            locator: tuple[str, str], 
            timeout: float | int = QUICK_WAIT, 
            is_display: bool = True, 
            show_log: bool = False
    ) -> bool:
        """Check if element is displayed."""
        if not is_display:
            self.wait_for_element_invisible(locator, timeout=timeout)
            timeout = QUICK_WAIT
        
        element = self.find_element(locator, timeout, raise_exception=False, show_log=show_log)
        result = bool(element)
        return result if is_display else not result

    def is_element_enabled(self, locator: tuple[str, str], timeout: float | int = EXPLICIT_WAIT) -> bool:
        """Check if element is enabled."""
        element = self.find_element(locator, timeout, raise_exception=False, show_log=False)
        return element.is_enabled() if element else False

    # ------- VERIFY ------ #
    def verify_element_displayed(
            self, 
            locator: tuple[str, str], 
            timeout: float | int = EXPLICIT_WAIT, 
            is_display: bool = True
    ) -> None:
        """Verify whether element is displayed or not."""
        result = self.is_element_displayed(locator, timeout=timeout, is_display=is_display, show_log=is_display)
        safe_locator = html.escape(str(locator))
        display_text = "not" if is_display else "still"
        soft_assert(
            result, True,
            error_message=f"Element with locator {safe_locator} is {display_text} displayed"
        )

    def verify_elements_displayed(
            self, 
            locators: list[tuple[str, str]] | tuple[str, str], 
            timeout: float | int = EXPLICIT_WAIT, 
            is_display: bool = True
    ) -> None:
        """Verify multiple elements are displayed or not."""
        locators = locators if isinstance(locators, list) else [locators]
        all_results = []
        failed_locators = []
        
        # Check first locator with full timeout
        first_result = self.is_element_displayed(locators[0], timeout=timeout, is_display=is_display, show_log=is_display)
        all_results.append(first_result)
        if not first_result:
            failed_locators.append(locators[0])
        
        # Check remaining locators with quick timeout
        for locator in locators[1:]:
            result = self.is_element_displayed(locator, timeout=QUICK_WAIT, is_display=is_display, show_log=is_display)
            all_results.append(result)
            if not result:
                failed_locators.append(locator)
        
        safe_failed_locators = [html.escape(str(loc)) for loc in failed_locators]
        display_text = "not" if is_display else "still"
        soft_assert(
            all(all_results), True,
            error_message=f"Elements with locators {safe_failed_locators} are {display_text} displayed"
        )

    # ------- PRIVATE HELPER METHODS ------ #
    def _handle_element_not_found(
            self, 
            locator: tuple[str, str], 
            exception: Exception, 
            timeout: float | int, 
            raise_exception: bool, 
            show_log: bool
    ) -> Optional[WebElement]:
        """Handle element not found scenarios."""
        if show_log:
            safe_locator = html.escape(str(locator))
            logger.warning(f"Element not found for {safe_locator}: {type(exception).__name__} after {timeout}(s)")
        
        if raise_exception:
            self._capture_failure_info()
            safe_locator = html.escape(str(locator))
            raise ElementNotFoundError(f"Element with locator {safe_locator} not found")
        
        return None
    
    def _capture_failure_info(self) -> None:
        """Capture failure information for debugging."""
        if StepLogs.test_steps:
            StepLogs.all_failed_logs.append((StepLogs.test_steps[-1], ""))
            attach_screenshot(self._driver, name="broken")
    
    def _get_select_all_key(self) -> str:
        """Get the appropriate select-all key based on platform."""
        platform = self._driver.capabilities.get('platformName', '').lower()
        return Keys.COMMAND if platform == 'mac' else Keys.CONTROL