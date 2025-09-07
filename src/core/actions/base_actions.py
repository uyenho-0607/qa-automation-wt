from selenium.common import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.core.decorators import handle_stale_element, log_requests
from src.data.consts import EXPLICIT_WAIT, QUICK_WAIT, IMPLICIT_WAIT, CHECK_ICON_COLOR, FAILED_ICON_COLOR, WARNING_ICON
from src.data.project_info import StepLogs
from src.utils.allure_utils import attach_screenshot
from src.utils.assert_utils import soft_assert
from src.utils.logging_utils import logger


class BaseActions:
    DEFAULT_CONDITION = EC.visibility_of_element_located

    def __init__(self, driver):
        self._driver = driver
        self._wait = WebDriverWait(driver=self._driver, timeout=EXPLICIT_WAIT)
        self._driver.implicitly_wait(IMPLICIT_WAIT)

    # @handle_stale_element
    def find_element(
            self,
            locator: tuple[str, str],
            timeout: float | int = EXPLICIT_WAIT,
            cond=DEFAULT_CONDITION,
            raise_exception=True,
            show_log=True
    ) -> WebElement | None:
        """
        ------ Find single element using WebDriverWait ------
        :param locator: locator needs to find
        :param timeout: timeout for WebDriverWait, default is "EXPLICIT_WAIT"
        :param cond: condition for finding element, default is "visibility_of_element_located"
        :param raise_exception:
            + True: raise Exception in case not found element, mark test step as broken and take screenshot
            + False: skip and return None
        :param show_log: if True, log warning message to console in case not found element, if False, skip logging
        :return: WebElement | None
        """

        wait = self._wait if timeout == EXPLICIT_WAIT else WebDriverWait(self._driver, timeout)

        try:
            return wait.until(cond(locator))

        except StaleElementReferenceException:
            logger.warning("- Stale element finding element, retry...")
            return wait.until(cond(locator))

        except (TimeoutException, NoSuchElementException) as e:
            if show_log:
                logger.warning(f"{WARNING_ICON} Element not found for {locator}: {type(e).__name__} after {timeout}(s)")

        except Exception as e:
            logger.error(f"Unexpected error for {locator}: {type(e).__name__}")

        if raise_exception:
            if StepLogs.test_steps:
                StepLogs.add_failed_log(StepLogs.test_steps[-1])
                attach_screenshot(self._driver, name="broken")  # Capture broken screenshot

            raise Exception(f"Element with locator {locator} not found")

        return None

    def find_elements(
            self, locator: tuple[str, str], timeout=EXPLICIT_WAIT, show_log=True
    ) -> list[WebElement]:
        """
        ------ Find list of elements using WebDriverWait using condition "presence_of_all_elements_located" ------
        :param locator: locator needs to find
        :param timeout: timeout for WebDriverWait, default is "EXPLICIT_WAIT"
        :return: list[WebElement] or empty list (case not found)
        """
        try:
            res = self.find_element(locator, timeout, EC.presence_of_all_elements_located, raise_exception=False, show_log=show_log)

        except StaleElementReferenceException:
            logger.warning("StaleElementReferenceException finding elements, retry...")
            res = self.find_element(locator, timeout, EC.presence_of_all_elements_located, raise_exception=False, show_log=show_log)

        return res or []

    @log_requests
    @handle_stale_element
    def click(
            self,
            locator: tuple[str, str],
            timeout: int | float = EXPLICIT_WAIT,
            raise_exception=True,
            show_log=True,
    ) -> None:
        """Click on an element."""
        element = self.find_element(
            locator, timeout, EC.element_to_be_clickable,
            raise_exception=raise_exception,
            show_log=show_log
        )
        if element:
            element.click()

    @log_requests
    @handle_stale_element
    def javascript_click(
            self,
            locator: tuple[str, str],
            timeout: int | float = EXPLICIT_WAIT,
            raise_exception=True,
            show_log=True,
    ):
        """Click on an element using JavaScript."""
        element = self.find_element(locator, timeout, EC.element_to_be_clickable, raise_exception=raise_exception, show_log=show_log)
        if element:
            self._driver.execute_script("arguments[0].click();", element)

    def click_if_displayed(self, locator, timeout=QUICK_WAIT):
        if self.is_element_displayed(locator, timeout):
            self.click(locator, timeout=timeout)

    def click_by_offset(self, **kwargs) -> None:
        pass

    def send_keys(self, **kwargs) -> None:
        pass

    @handle_stale_element
    def clear_field(
            self,
            locator: tuple[str, str],
            timeout=EXPLICIT_WAIT,
            raise_exception=True,
            show_log=True
    ) -> None:
        """Clear field using Ctrl+A (Cmd+A on Mac) and Delete."""
        element = self.find_element(
            locator, timeout, EC.element_to_be_clickable,
            raise_exception=raise_exception,
            show_log=show_log
        )
        if element:
            # Click to focus the element
            element.click()
            key = Keys.COMMAND if self._driver.capabilities.get('platformName').lower() == 'mac' else Keys.CONTROL
            # Select all text and delete
            element.send_keys(key + "a")
            element.send_keys(Keys.DELETE)

    @handle_stale_element
    def get_attribute(
            self,
            locator: tuple[str, str],
            attribute: str,
            timeout=EXPLICIT_WAIT,
            raise_exception=True,
            show_log=True
    ) -> str | None:
        """Get attribute value from an element."""
        element = self.find_element(
            locator, timeout, EC.presence_of_element_located,
            raise_exception=raise_exception, show_log=show_log
        )
        return element.get_attribute(attribute) if element else ""

    @handle_stale_element
    def get_text_elements(self, locator, timeout=EXPLICIT_WAIT):
        """Get text of elements having same locator"""
        elements = self.find_elements(locator, timeout)
        res = [ele.text.strip() if ele else "" for ele in elements]
        return res

    @handle_stale_element
    def get_text(
            self,
            locator: tuple[str, str],
            timeout=EXPLICIT_WAIT,
            raise_exception=False,
            show_log=True,
    ) -> str:
        """Get text from element."""
        element = self.find_element(locator, timeout, raise_exception=raise_exception, show_log=show_log)
        if not element:
            element = self.find_element(locator, QUICK_WAIT, raise_exception=raise_exception, show_log=show_log)

        return element.text.strip() if element else ""

    def wait_for_element_invisible(
            self,
            locator: tuple[str, str],
            timeout: float | int = EXPLICIT_WAIT,
    ) -> WebElement | None:
        """Wait for element to be invisible, NO exception will be raised if element is not found"""
        wait = self._wait if timeout == EXPLICIT_WAIT else WebDriverWait(self._driver, timeout=timeout)
        try:
            res = wait.until(EC.invisibility_of_element_located(locator))
            logger.debug(f"> Check invisibility of element {locator}: {CHECK_ICON_COLOR if bool(res) else FAILED_ICON_COLOR}")
            return res

        except TimeoutException:
            logger.warning(f"{WARNING_ICON} Element {locator} still display after {timeout} sec")
            return None

    @log_requests
    def wait_for_element_visible(
            self,
            locator: tuple[str, str],
            timeout=EXPLICIT_WAIT,
    ) -> bool:
        """Wait for element to be visible, NO exception will be raised if element is not found"""
        res = self.find_element(
            locator, timeout, cond=EC.visibility_of_element_located, raise_exception=False, show_log=True
        )
        return bool(res)

    def is_element_displayed(self, locator: tuple[str, str], timeout=QUICK_WAIT, is_display=True, show_log=False) -> bool:
        """Check if element is displayed, NO exception will be raised if element is not found"""
        if not is_display:
            self.wait_for_element_invisible(locator, timeout=timeout)
            timeout = QUICK_WAIT

        element = self.find_element(locator, timeout, raise_exception=False, show_log=show_log)
        res = bool(element)

        return res if is_display else not res

    def is_element_enabled(self, locator: tuple[str, str], timeout=EXPLICIT_WAIT) -> bool:
        """Check if element is enabled."""
        element = self.find_element(locator, timeout, raise_exception=False, show_log=False)
        return element.is_enabled() if element else False

    # ------- VERIFY ------ #
    def verify_element_displayed(
            self, locator: tuple[str, str], timeout: int | float = EXPLICIT_WAIT, is_display: bool = True
    ):
        """Verify whether element is displayed or not"""
        res = self.is_element_displayed(locator, timeout=timeout, is_display=is_display, show_log=is_display)
        soft_assert(
            res, True,
            error_message=f"Element with locator {locator} is {('not' if is_display else 'still')} displayed"
        )

    def verify_elements_displayed(self, locators, timeout=EXPLICIT_WAIT, is_display=True):
        all_res = []
        failed_locator = []
        locators = locators if isinstance(locators, list) else [locators]

        # wait for the first locator with full timeout
        res = self.is_element_displayed(locators[0], timeout=timeout, is_display=is_display, show_log=is_display)
        all_res.append(res)

        if not res:
            failed_locator.append(locators[0])

        # wait for the others locator with quick-wait as page already loaded
        for _locator in locators[1:]:
            res = self.is_element_displayed(_locator, timeout=QUICK_WAIT, is_display=is_display, show_log=is_display)
            all_res.append(res)
            if not res:
                failed_locator.append(_locator)

        logger.debug(f"> Check {'elements_displayed' if is_display else 'elements_not_displayed'}: {CHECK_ICON_COLOR if all(all_res) else FAILED_ICON_COLOR}")

        soft_assert(
            all(all_res), True,
            error_message=f"Elements with locators {failed_locator} are {('not' if is_display else 'still')} displayed"
        )
