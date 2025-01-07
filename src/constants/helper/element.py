from __future__ import annotations

import time
import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException


from constants.main import DRIVER_WAIT_DURATION

clickable_element = EC.element_to_be_clickable

data_test_id_pattern = "//*[@data-testid='{}']"


def derive_wait_duration(duration: int | None = None) -> int:
    return duration if duration is not None else DRIVER_WAIT_DURATION


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                FIND ELEMENT BY XPATH / TESTID
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Use WebDriver to find for element to according to specified xpath string
def find_element_by_xpath(driver, xpath_string) -> WebElement:
    return driver.find_element(By.XPATH, xpath_string)

# Use WebDriver to find for element to according to specified data_testid string
def find_element_by_testid(driver, data_testid) -> WebElement:
    data_test_id_string = data_test_id_pattern.format(data_testid)
    return driver.find_element(By.XPATH, data_test_id_string)

def find_element_by_xpath_with_wait(driver, xpath_string, duration: int | None = None) -> WebElement:
    wait_duration = derive_wait_duration(duration)
    element_on_focus = WebDriverWait(driver, wait_duration).until(clickable_element((By.XPATH, xpath_string)))
    return element_on_focus

# Use WebDriver to find for element to according to specified css_selector string
def find_element_by_css(driver, css_selector) -> WebElement:
    return driver.find_element(By.CSS_SELECTOR, css_selector)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                FIND LIST OF ELEMENT BY XPATH / TESTID
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Use WebDriver to find for list of elements to according to specified xpath string
def find_list_of_elements_by_xpath(driver, xpath_string) -> list[WebElement]:
    return driver.find_elements(By.XPATH, xpath_string)

# Use WebDriver to find for list of elements to according to specified data_testid string
def find_list_of_elements_by_testid(driver, data_testid):
    data_test_id_string = data_test_id_pattern.format(data_testid)
    return driver.find_elements(By.XPATH, data_test_id_string)

# Use WebDriver to find for list of elements to according to specified css_selector string
def find_list_of_elements_by_css(driver, css_selector) -> list[WebElement]:
    return driver.find_elements(By.CSS_SELECTOR, css_selector)


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ELEMENTI IS VISIBLE / INVISIBILITY
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def is_element_present_by_xpath(driver, xpath: str) -> bool:
    try:
        # Try to find the element
        find_element_by_xpath(driver, xpath)
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
    return WebDriverWait(driver, wait_duration).until(EC.visibility_of_element_located((By.XPATH, xpath_string)))


def visibility_of_element_by_testid(driver, data_testid, duration: int | None = None) -> WebElement:
    data_test_id_string = data_test_id_pattern.format(data_testid)
    wait_duration = derive_wait_duration(duration)
    return WebDriverWait(driver, wait_duration).until(EC.visibility_of_element_located((By.XPATH, data_test_id_string)))


# Waits for the element to either: Not be in the DOM, or be in the DOM but not visible.
def invisibility_of_element_by_xpath(driver, xpath, duration: int | None = None) -> WebElement:
    wait_duration = derive_wait_duration(duration)
    return WebDriverWait(driver, wait_duration).until(EC.invisibility_of_element_located((By.XPATH, xpath)))


def invisibility_of_element_by_testid(driver, data_testid, duration: int | None = None) -> WebElement:
    data_test_id_string = data_test_id_pattern.format(data_testid)
    wait_duration = derive_wait_duration(duration)
    return WebDriverWait(driver, wait_duration).until(EC.invisibility_of_element_located((By.XPATH, data_test_id_string)))

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ELEMENT IS PRESENT IN THE DOM
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Ensures the element exists in the DOM and does not guarantee the element is visible.
def presence_of_element_located_by_xpath(driver, xpath, duration: int | None = None) -> WebElement:
    wait_duration = derive_wait_duration(duration)
    return WebDriverWait(driver, wait_duration).until(EC.presence_of_element_located((By.XPATH, xpath)))


def presence_of_element_located_by_testid(driver, data_testid, duration: int | None = None) -> WebElement:
    data_test_id_string = data_test_id_pattern.format(data_testid)
    wait_duration = derive_wait_duration(duration)
    return WebDriverWait(driver, wait_duration).until(EC.presence_of_element_located((By.XPATH, data_test_id_string)))

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
        element.send_keys(Keys.CONTROL + 'a') # Select all text (use Keys.CONTROL for Windows/Linux)
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

def wait_for_text_to_be_present_in_element_by_xpath(driver, xpath, text, duration: int | None = None) -> bool:
    try:
        wait_duration = derive_wait_duration(duration)
        WebDriverWait(driver, wait_duration).until(EC.text_to_be_present_in_element((By.XPATH, xpath), text))
        return True
    except:
        return False
    
    
def wait_for_text_to_be_present_in_element_by_testid(driver, data_testid, text, duration: int | None = None) -> bool:
    try:
        data_test_id_string = data_test_id_pattern.format(data_testid)
        wait_duration = derive_wait_duration(duration)
        WebDriverWait(driver, wait_duration).until(EC.text_to_be_present_in_element((By.XPATH, data_test_id_string), text))
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
    
# Retrieve the label content
def get_label_of_element(element: WebElement) -> str:
    # Retrieve the tag name of element
    tag_name = element.tag_name

    # Check the tag name
    if tag_name in ["div", "span", "td"]:
        label = element.text
        
    elif tag_name in ["input", "button"]:
        # Get the label using the 'label' attribute
        label = element.get_attribute("label")

        # If 'label' is None, try getting the label using the 'aria-label' attribute
        if label is None:
            label = element.get_attribute("aria-label")
    else:
        print("Unable to retrieve label: {tag_name}")

    return label


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SWITCH TO IFRAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Switches to the iframe content
def iframe(driver, duration: int | None = None) -> None:
    try:
        wait_duration = derive_wait_duration(duration)

        # Wait until the iframe is available and switch to it
        WebDriverWait(driver, wait_duration).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "(//iframe)[1]")))

        # Wait until the element inside the iframe is visible
        element = WebDriverWait(driver, wait_duration).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="YOUR_TESTID"]')))

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


#  To check if a specific element on a web page has a cursor style of "not-allowed". 
def is_element_disabled_by_cursor(driver, element):
    return driver.execute_script("return window.getComputedStyle(arguments[0]).cursor == 'not-allowed';", element)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                FOR LOADING ICON
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Checking the loading spinner
def spinner_element(driver):
    try:
        invisibility_of_element_by_testid(driver, data_testid="spin-loader")
    except TimeoutError:
        assert False, "Timeout waiting for loading icon to disappear. Check if the API is slow or the selector is correct."

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                EXTRACT RGB COLOR FUNCTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def extract_rgb_from_color(color_string):
    # Extract RGB values from the color string
    rgb_values = tuple(map(int, color_string.strip('rgba()').split(',')[:3]))
    return rgb_values



def get_button_color(driver, button_element):
    try:
        # JavaScript to get the color of the button
        script = """
        var button = arguments[0];
        return window.getComputedStyle(button).color;
        """
        
        button_color = driver.execute_script(script, button_element)
        
        print(f"Button color: {button_color}")
        return button_color
        
    except Exception as e:
        print(f"Error retrieving button color: {str(e)}")
        return None
         
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""