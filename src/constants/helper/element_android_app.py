from __future__ import annotations

import time
import traceback

from selenium.webdriver.common.keys import Keys
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
# from appium.webdriver.webdriver import WebDriver


from constants.main import DRIVER_WAIT_DURATION

clickable_element = EC.element_to_be_clickable

data_test_id_pattern = "//*[@resource-id='{}']"


def derive_wait_duration(duration: int | None = None) -> int:
    return duration if duration is not None else DRIVER_WAIT_DURATION


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

# def visibility_of_element_by_xpath(driver, xpath_string, timeout=10) -> WebElement:
#     return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((AppiumBy.XPATH, xpath_string)))


# def visibility_of_element_by_testid(driver, data_testid, timeout=5) -> WebElement:
#     data_test_id_string = data_test_id_pattern.format(data_testid)
#     visibility_of_element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((AppiumBy.XPATH, data_test_id_string)))
#     return visibility_of_element


# def invisibility_of_element_by_xpath(driver, xpath, timeout=25):
#     # wait_duration = derive_wait_duration(duration)
#     element = WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located((AppiumBy.XPATH, xpath)))
#     return element


# def invisibility_of_element_by_testid(driver, data_testid, timeout=25):
# # def invisibility_of_element_by_testid(driver, data_testid, duration: int | None = None) -> WebElement:
#     data_test_id_string = data_test_id_pattern.format(data_testid)
#     # wait_duration = derive_wait_duration(duration)
#     invisibility_of_element = WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located((AppiumBy.XPATH, data_test_id_string)))
#     return invisibility_of_element



def visibility_of_element_by_xpath(driver, xpath_string, duration: int | None = None) -> WebElement:
    wait_duration = derive_wait_duration(duration)
    return WebDriverWait(driver, wait_duration).until(EC.visibility_of_element_located((AppiumBy.XPATH, xpath_string)))


def visibility_of_element_by_testid(driver, data_testid, duration: int | None = None) -> WebElement:
    data_test_id_string = data_test_id_pattern.format(data_testid)
    wait_duration = derive_wait_duration(duration)
    visibility_of_element = WebDriverWait(driver, wait_duration).until(EC.visibility_of_element_located((AppiumBy.XPATH, data_test_id_string)))
    return visibility_of_element



def invisibility_of_element_by_xpath(driver, xpath, duration: int | None = None) -> WebElement:
    wait_duration = derive_wait_duration(duration)
    element = WebDriverWait(driver, wait_duration).until(EC.invisibility_of_element_located((AppiumBy.XPATH, xpath)))
    return element


def invisibility_of_element_by_testid(driver, data_testid, duration: int | None = None) -> WebElement:
    data_test_id_string = data_test_id_pattern.format(data_testid)
    wait_duration = derive_wait_duration(duration)
    invisibility_of_element = WebDriverWait(driver, wait_duration).until(EC.invisibility_of_element_located((AppiumBy.XPATH, data_test_id_string)))
    return invisibility_of_element


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ELEMENT IS PRESENT IN THE DOM
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# def presence_of_element_located_by_testid(driver, data_testid, timeout=5) -> WebElement:
#     data_test_id_string = data_test_id_pattern.format(data_testid)
#     # wait_duration = derive_wait_duration(duration)
#     # Wait for the spinner to appear
#     WebDriverWait(driver, timeout).until(EC.presence_of_element_located((AppiumBy.XPATH, data_test_id_string)))


# def presence_of_element_located_by_xpath(driver, xpath, timeout=5) -> WebElement:
#     # wait_duration = derive_wait_duration(duration)
#     # Wait for the spinner to appear
#     WebDriverWait(driver, timeout).until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))


def presence_of_element_located_by_xpath(driver, xpath, duration: int | None = None) -> WebElement:
    wait_duration = derive_wait_duration(duration)
    # Wait for the spinner to appear
    WebDriverWait(driver, wait_duration).until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))


def presence_of_element_located_by_testid(driver, data_testid, duration: int | None = None) -> WebElement:
    data_test_id_string = data_test_id_pattern.format(data_testid)
    wait_duration = derive_wait_duration(duration)
    # Wait for the spinner to appear
    WebDriverWait(driver, wait_duration).until(EC.presence_of_element_located((AppiumBy.XPATH, data_test_id_string)))


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
    # Keep attempting to clear the field until it's empty
    while element.get_attribute("value") != "":
        element.send_keys(Keys.COMMAND + 'a') # Select all text (use Keys.CONTROL for Windows/Linux)
        element.send_keys(Keys.DELETE) # Delete the selected text

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


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                WAIT FOR TEXT TO BE PRESENT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# def wait_for_text_to_be_present_in_element_by_xpath(driver, xpath, text, timeout=30) -> bool:
def wait_for_text_to_be_present_in_element_by_xpath(driver, xpath, text, duration: int | None = None) -> bool:
    try:
        wait_duration = derive_wait_duration(duration)

        WebDriverWait(driver, wait_duration).until(EC.text_to_be_present_in_element((AppiumBy.XPATH, xpath), text))
        return True
    except:
        return False
    
    
# def wait_for_text_to_be_present_in_element_by_testid(driver, data_testid, text, timeout=30):
def wait_for_text_to_be_present_in_element_by_testid(driver, data_testid, text, duration: int | None = None) -> bool:
    try:
        data_test_id_string = data_test_id_pattern.format(data_testid)
        wait_duration = derive_wait_duration(duration)
        WebDriverWait(driver, wait_duration).until(EC.text_to_be_present_in_element((AppiumBy.XPATH, data_test_id_string), text))
        return True
    except:
        return False
    
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                RETRIEVE THE LABEL CONTENT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def get_label_of_element(element) -> str:
    # Retrieve the tag name of element
    tag_name = element.tag_name

    # For mobile elements, use 'text', 'label', or 'content-desc'
    if tag_name in ["android.widget.TextView", "android.widget.Button", "android.widget.EditText"]:
        # For Android elements, use 'text' or 'content-desc'
        label = element.text or element.get_attribute("content-desc")

    elif tag_name in ["XCUIElementTypeButton", "XCUIElementTypeStaticText", "XCUIElementTypeTextField"]:
        # For iOS elements, use 'label'
        label = element.get_attribute("label") or element.get_attribute("value")
    
    else:
        print(f"Unable to retrieve label for element: {tag_name}")
        label = None
    
    # label = element.text
    
    return label


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SWITCH TO IFRAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Switches to the iframe content
def iframe(driver):
    try:
        # Wait until the iframe is available and switch to it
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((AppiumBy.XPATH, "(//iframe)[1]")))

        # Wait until the element inside the iframe is visible
        element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((AppiumBy.CSS_SELECTOR, '[data-testid="YOUR_TESTID"]'))) # Replace with the actual data-testid

        # Check if the element is displayed
        is_displayed = element.is_displayed()

        # Print the result
        print(f"Element is displayed: {is_displayed}")

    finally:
        # Don't forget to switch back to the main content
        driver.switch_to.default_content()

        # Close the driver
        driver.quit()
        


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TO AUTO SCROLL INTO VIEW
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Javascript click
def javascript_click(driver, element):
    try:
   
        """Use JavaScript to click on the given web element """
        # driver.execute_script("arguments[0].click();", element)
        driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", element)
   
        # Execute JavaScript to scale the page content to 80%
        # driver.execute_script("document.body.style.zoom='75%'")
        
    except Exception as e:
        assert False, f"{str(e)}\n{traceback.format_exc()}"


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                FOR LOADING ICON - Desktop
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
# Checking the loading spinner
def spinner_element(driver):
    try:
        
        invisibility_of_element_by_testid(driver, data_testid="spin-loader")

    except TimeoutError:
        assert False, "Timeout waiting for loading icon to disappear. Check if the API is slow or the selector is correct."