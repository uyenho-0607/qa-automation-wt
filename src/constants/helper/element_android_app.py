from __future__ import annotations

import time
import traceback

from selenium.webdriver.common.keys import Keys
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
# from appium.webdriver.webdriver import WebDriver

from constants.element_ids import DataTestID
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import take_screenshot
from constants.main import APP_WAIT_DURATION

clickable_element = EC.element_to_be_clickable

data_test_id_pattern = "//*[@resource-id='{}']"


def derive_wait_duration(duration: int | None = None) -> int:
    return duration if duration is not None else APP_WAIT_DURATION


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                FIND ELEMENT BY XPATH / TESTID
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Use WebDriver to find for element to according to specified xpath string
def find_element_by_xpath(driver, xpath_string) -> WebElement:
    return driver.find_element(AppiumBy.XPATH, xpath_string)

# Use WebDriver to find for element to according to specified data_testid string
def find_element_by_testid(driver, data_testid) -> WebElement:
    data_test_id_string = data_test_id_pattern.format(data_testid)
    return driver.find_element(AppiumBy.XPATH, data_test_id_string)


# def find_element_by_testid(driver, data_testid: str) -> WebElement:
#     package_name = driver.capabilities['appPackage']
#     full_resource_id = f"{package_name}:id/{data_testid}"  # Add the `id/` part
    
#     try:
#         element = driver.find_element(AppiumBy.ID, full_resource_id)
#         return element
#     except Exception as e:
#         print(f"Element with resource ID '{full_resource_id}' not found. Error: {str(e)}")
#         return None


def find_element_by_xpath_with_wait(driver, xpath_string, duration: int | None = None) -> WebElement:
    wait_duration = derive_wait_duration(duration)
    element_on_focus = WebDriverWait(driver, wait_duration).until(clickable_element((AppiumBy.XPATH, xpath_string)))
    return element_on_focus


def find_element_by_testid_with_wait(driver, data_testid, duration: int | None = None) -> WebElement:
    wait_duration = derive_wait_duration(duration)
    data_test_id_string = data_test_id_pattern.format(data_testid)
    element_on_focus = WebDriverWait(driver, wait_duration).until(clickable_element((AppiumBy.XPATH, data_test_id_string)))
    return element_on_focus


# Use WebDriver to find for element to according to specified css_selector string
def find_element_by_css(driver, css_selector) -> WebElement:
    return driver.find_element(AppiumBy.CSS_SELECTOR, css_selector)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                FIND LIST OF ELEMENT BY XPATH / TESTID
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Use WebDriver to find for list of elements to according to specified xpath string
def find_list_of_elements_by_xpath(driver, xpath_string) -> list[WebElement]:
    return driver.find_elements(AppiumBy.XPATH, xpath_string)

# Use WebDriver to find for list of elements to according to specified data_testid string
def find_list_of_elements_by_testid(driver, data_testid):
    data_test_id_string = data_test_id_pattern.format(data_testid)
    return driver.find_elements(AppiumBy.XPATH, data_test_id_string)

# Use WebDriver to find for list of elements to according to specified css_selector string
def find_list_of_elements_by_css(driver, css_selector) -> list[WebElement]:
    return driver.find_elements(AppiumBy.CSS_SELECTOR, css_selector)


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ELEMENTI IS VISIBLE / INVISIBILITY
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def is_element_present_by_testid(driver, data_testid: str) -> bool:
    try:
        # Try to find the element
        # find_element_by_testid(driver, data_testid)
        find_element_by_xpath_with_wait(driver, data_testid)
        # Use WebDriver to find for element to according to specified xpath string
        return True
    except Exception:
        # If element is not found, return False
        return False    
    

def is_element_present_by_xpath(driver, xpath: str) -> bool:
    try:
        # Try to find the element
        # find_element_by_xpath(driver, xpath)
        find_element_by_xpath_with_wait(driver, xpath)
        # Use WebDriver to find for element to according to specified xpath string
        return True
    except Exception:
        # If element is not found, return False
        return False
    

# Ensures the element is both present in the DOM and visible.
def wait_for_element_visibility(driver, locator, duration: int | None = None) -> WebElement:
    wait_duration = derive_wait_duration(duration)
    return WebDriverWait(driver, wait_duration).until(EC.visibility_of(locator)) is not None


def visibility_of_element_by_xpath(driver, xpath_string, duration: int | None = None) -> WebElement:
    wait_duration = derive_wait_duration(duration)
    return WebDriverWait(driver, wait_duration).until(EC.visibility_of_element_located((AppiumBy.XPATH, xpath_string)))


def visibility_of_element_by_testid(driver, data_testid, duration: int | None = None) -> WebElement:
    data_test_id_string = data_test_id_pattern.format(data_testid)
    wait_duration = derive_wait_duration(duration)
    visibility_of_element = WebDriverWait(driver, wait_duration).until(EC.visibility_of_element_located((AppiumBy.XPATH, data_test_id_string)))
    return visibility_of_element


def invisibility_of_element_by_xpath(driver, xpath, duration: int | None = None) -> WebElement:
    # wait_duration = derive_wait_duration(duration)
    # element = WebDriverWait(driver, wait_duration).until(EC.invisibility_of_element_located((AppiumBy.XPATH, xpath)))
    # return element
    wait_duration = derive_wait_duration(duration)
    try:
        return WebDriverWait(driver, wait_duration).until(EC.invisibility_of_element_located((AppiumBy.XPATH, xpath)))
    except:
        return False # Return False if timeout occurs


def invisibility_of_element_by_testid(driver, data_testid, duration: int | None = None) -> bool:
    data_test_id_string = data_test_id_pattern.format(data_testid)
    wait_duration = derive_wait_duration(duration)
    try:
        return WebDriverWait(driver, wait_duration).until(EC.invisibility_of_element_located((AppiumBy.XPATH, data_test_id_string)))
    except:
        return False  # Return False if timeout occurs

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ELEMENT IS PRESENT IN THE DOM
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def presence_of_element_located_by_xpath(driver, xpath, duration: int | None = None) -> WebElement:
    wait_duration = derive_wait_duration(duration)
    # Wait for the spinner to appear
    return WebDriverWait(driver, wait_duration).until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))


def presence_of_element_located_by_testid(driver, data_testid, duration: int | None = None) -> WebElement:
    data_test_id_string = data_test_id_pattern.format(data_testid)
    wait_duration = derive_wait_duration(duration)
    # Wait for the spinner to appear
    return WebDriverWait(driver, wait_duration).until(EC.presence_of_element_located((AppiumBy.XPATH, data_test_id_string)))


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                POPULATE ELEMENT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def populate_element(element: WebElement, text: str) -> None:
    element.send_keys(text)


def populate_element_with_wait(driver, element: WebElement, text: str, duration: int | None = None) -> None:
    wait_duration = derive_wait_duration(duration)

    # Use WebDriverWait to wait for the element to be clickable
    element_on_focus = WebDriverWait(driver, wait_duration).until(clickable_element(element))

    # Input value within element
    populate_element(element_on_focus, text)

    # If send_enter is True, send Enter key based on the platform
        # if send_enter:
        #     platform = driver.capabilities['platformName'].lower()

        #     if platform == 'android':
        #         driver.press_keycode(66) # Android Enter key
        #     elif platform == 'ios':
        #         element_on_focus.send_keys("\n") # iOS Enter key
        #     else:
        #         raise Exception("Unsupported platform: " + platform)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TO AUTO SCROLL INTO VIEW
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Clear the field
def clear_input_field(element):
    element.click()
    element.clear()
    # Keep attempting to clear the field until it's empty
    # while element.get_attribute("text") != "":
    #     element.send_keys(Keys.CONTROL, "a")  # Select all text
    #     element.send_keys(Keys.BACKSPACE)  # Delete selected text
    #     element.clear()
    # driver.set_value(element, "")


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CLICK ELEMENT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def click_element(element: WebElement) -> None:
    element.click()


def click_element_with_wait(driver, element: WebElement, duration: int | None = None) -> None:
    wait_duration = derive_wait_duration(duration)
    # Use WebDriverWait to wait for the element to be clickable
    element_on_focus = WebDriverWait(driver, wait_duration).until(clickable_element(element))
    # Perform the click
    click_element(element_on_focus)


def wait_for_element_clickable_xpath(driver, xpath, duration: int | None = None) -> WebElement:
    wait_duration = derive_wait_duration(duration)
    return WebDriverWait(driver, wait_duration).until(EC.element_to_be_clickable((AppiumBy.XPATH, xpath)))
    

def wait_for_element_clickable_testid(driver, data_testid, duration: int | None = None) -> WebElement:
    data_test_id_string = data_test_id_pattern.format(data_testid)
    wait_duration = derive_wait_duration(duration)
    return WebDriverWait(driver, wait_duration).until(EC.element_to_be_clickable((AppiumBy.XPATH, data_test_id_string)))

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                WAIT FOR TEXT TO BE PRESENT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def wait_for_text_to_be_present_in_element_by_xpath(driver, xpath, text, duration: int | None = None) -> bool:
    try:
        wait_duration = derive_wait_duration(duration)
        WebDriverWait(driver, wait_duration).until(EC.text_to_be_present_in_element((AppiumBy.XPATH, xpath), text))
        return True
    except:
        return False
    

def wait_for_text_to_be_present_in_element_by_testid(driver, data_testid, text, duration: int | None = None) -> bool:
    try:
        data_test_id_string = data_test_id_pattern.format(data_testid)
        wait_duration = derive_wait_duration(duration)
        WebDriverWait(driver, wait_duration).until(EC.text_to_be_present_in_element((AppiumBy.XPATH, data_test_id_string), text))
        return True
    except:
        return False
    

def wait_for_element_value(driver, element, expected_value, duration: int | None = None) -> bool:
    wait_duration = derive_wait_duration(duration)
    WebDriverWait(driver, wait_duration).until(lambda _: element.get_attribute("value") == expected_value)
    return True

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                RETRIEVE THE LABEL CONTENT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_label_of_element(element) -> str:
    # Get the class name of the element
    class_name = element.get_attribute("class")

    # For Android elements, check for known class names and retrieve text or content-desc
    if class_name in ["android.widget.TextView", "android.view.ViewGroup", "android.widget.Button", "android.widget.EditText"]:
        # For Android, use 'text' or 'content-desc'
        label = element.text or element.get_attribute("content-desc")
    
    # For iOS elements, check for common class names
    elif class_name in ["UIAStaticText", "UIAButton", "UIATextField"]:
        # For iOS, use 'label', 'name', or 'value'
        label = element.get_attribute("label") or element.get_attribute("name") or element.get_attribute("value")
        
    else:
        element.text
    
    # return label if label else ""
    return label

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                FOR LOADING ICON - Desktop
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
# Checking the loading spinner
# def spinner_element(driver):
#     try:
        
#         invisibility_of_element_by_testid(driver, data_testid="spin-loader")

#     except TimeoutError:
#         assert False, "Timeout waiting for loading icon to disappear. Check if the API is slow or the selector is correct."
        


# Checking the loading spinner
def spinner_element(driver):
    try:
        # invisibility_of_element_by_testid(driver, data_testid="spin-loader")
        invisibility_of_element_by_testid(driver, data_testid=DataTestID.SPIN_LOADER.value)
    except Exception as e:
        # Attach a screenshot with the function name in the filename
        take_screenshot(driver, f"Exception_Screenshot")
        # Handle any exceptions that occur during the execution
        raise Exception("Timeout waiting for loading icon to disappear. Check if the API is slow")
    

def bulk_spinner_element(driver, timeout=10):
    try:
        # invisibility_of_element_by_testid(driver, data_testid="spin-loader")
        # Wait for the spinner to disappear
        WebDriverWait(driver, timeout).until(EC.invisibility_of_element((AppiumBy.CSS_SELECTOR, "[data-testid='spin-loader']")))
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
        raise Exception("Timeout waiting for loading icon to disappear. Check if the API is slow")