from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.core.decorators import handle_stale_element
from src.data.consts import EXPLICIT_WAIT, QUICK_WAIT, SHORT_WAIT
from src.data.project_info import StepLogs
from src.utils.allure_utils import attach_screenshot
from src.utils.assert_utils import soft_assert
from src.utils.logging_utils import logger


class BaseActions:
    DEFAULT_CONDITION = EC.visibility_of_element_located

    def __init__(self, driver):
        self._driver = driver
        self._wait = WebDriverWait(driver=self._driver, timeout=EXPLICIT_WAIT)
        # self._driver.implicitly_wait(IMPLICIT_WAIT)

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

        except (TimeoutException, NoSuchElementException) as e:
            if show_log:
                logger.warning(f"Element not found for {locator}: {type(e).__name__} after {timeout}(s)")

        except Exception as e:
            logger.error(f"Unexpected error for {locator}: {type(e).__name__}")

        if raise_exception:
            if StepLogs.test_steps:
                StepLogs.all_failed_logs.append((StepLogs.test_steps[-1], ""))
                attach_screenshot(self._driver, name="broken")  # Capture broken screenshot

            raise Exception(f"Element with locator {locator} not found")

        return None

    def find_elements(
            self, locator: tuple[str, str], timeout=EXPLICIT_WAIT
    ) -> list[WebElement]:
        """
        ------ Find list of elements using WebDriverWait using condition "presence_of_all_elements_located" ------
        :param locator: locator needs to find
        :param timeout: timeout for WebDriverWait, default is "EXPLICIT_WAIT"
        :return: list[WebElement] or empty list (case not found)
        """
        res = self.find_element(locator, timeout, EC.presence_of_all_elements_located, raise_exception=False)
        return res or []

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
        element = self.find_element(locator, timeout, raise_exception=raise_exception, show_log=show_log)
        return element.get_attribute(attribute) if element else None

    @handle_stale_element
    def get_text(
            self,
            locator: tuple[str, str],
            timeout=SHORT_WAIT,
            retry=False,
            raise_exception=False,
            show_log=True,
    ) -> str:
        """Get text from element."""
        element = self.find_element(locator, timeout, raise_exception=raise_exception, show_log=show_log)
        if retry and not element:
            # get text of element again
            element = self.find_element(locator, timeout, raise_exception=raise_exception, show_log=show_log)

        return element.text.strip() if element else ""

    def wait_for_element_invisible(
            self,
            locator: tuple[str, str],
            timeout=EXPLICIT_WAIT,
    ) -> None:
        """Wait for element to be invisible, NO exception will be raised if element is not found"""
        self.find_element(
            locator, timeout, cond=EC.invisibility_of_element_located, raise_exception=False, show_log=False
        )


    def wait_for_element_visible(
            self,
            locator: tuple[str, str],
            timeout=EXPLICIT_WAIT,
    ) -> None:
        """Wait for element to be visible, NO exception will be raised if element is not found"""
        self.find_element(
            locator, timeout, cond=EC.visibility_of_element_located, raise_exception=False, show_log=True
        )

    def is_element_displayed(self, locator: tuple[str, str], timeout=QUICK_WAIT, is_display=True, show_log=False) -> bool:
        """Check if element is displayed, NO exception will be raised if element is not found"""
        element = self.find_element(locator, timeout, raise_exception=False, show_log=show_log)
        res = bool(element)
        return res if is_display else not res

    def is_element_enabled(self, locator: tuple[str, str], timeout=EXPLICIT_WAIT) -> bool:
        """Check if element is enabled."""
        element = self.find_element(locator, timeout, raise_exception=False, show_log=False)
        return element.is_enabled() if element else False

    def execute_script(self, script: str, *args):
        """Execute JavaScript code with optional arguments."""
        return self._driver.execute_script(script, *args)

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
        for _locator in locators:
            res = self.is_element_displayed(_locator, timeout=QUICK_WAIT, is_display=is_display, show_log=is_display)
            all_res.append(res)
            if not res:
                failed_locator.append(_locator)

        soft_assert(
            all(all_res), True,
            error_message=f"Elements with locators {failed_locator} are {('not' if is_display else 'still')} displayed"
        )
