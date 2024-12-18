from __future__ import annotations

import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


from constants.helper.element import spinner_element
from constants.main import DRIVER_WAIT_DURATION

def access_url(driver: WebDriver, url: str) -> None:
    # Execute JavaScript to optimize page load
    # driver.execute_script("window.stop();") # Stop loading resources
    
    # Route browser to the specified URL
    driver.get(url)
    

def get_current_url(driver: WebDriver) -> str:
   return driver.current_url


def wait_for_url(driver, success_urls):

    spinner_element(driver)
    
    initial_url = driver.current_url  # Get the initial URL to detect changes
    
    try:
        WebDriverWait(driver, timeout=2).until(
            lambda d: d.current_url != initial_url or d.current_url in success_urls
        )
        # URL has changed or matched
        if driver.current_url in success_urls:
            return driver.current_url  # Return the matched URL
        else:
            return False  # URL changed but did not match success URLs
    except:
        return False  # Timeout or no URL change

    
# WebDriver instance polls the HTML DOM for a certain duration when trying to find any element.
# This is used when certain elements on the webpage are not available immediately and need some time to load.
def wait(driver: WebDriver, duration: int | None = None) -> None:
    wait_duration = duration if duration is not None else DRIVER_WAIT_DURATION
    driver.implicitly_wait(wait_duration)


# Adds delay of code execution using python's time plugin
def delay(duration: int) -> None:
    time.sleep(duration)


# If new browser window is spawned, this function helps to switch focus onto the newly spawned browser window
def switch_to_new_window(driver) -> None:
    driver.switch_to.window(driver.window_handles[1])
    

def wait_for_page_load(driver, duration: int | None = None):
    wait_duration = wait(duration)
    WebDriverWait(driver, wait_duration).until(lambda d: d.execute_script("return document.readyState") == "complete")


def shutdown(driver: WebDriver) -> None:
    driver.quit()