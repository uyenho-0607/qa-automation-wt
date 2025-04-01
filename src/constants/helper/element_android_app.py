from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from constants.element_ids import DataTestID
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import take_screenshot
from constants.main import APP_DRIVER_WAIT_DURATION

clickable_element = EC.element_to_be_clickable

data_test_id_pattern = "//*[@resource-id='{}']"


def derive_wait_duration(duration: int | None = None) -> int:
    return duration if duration is not None else APP_DRIVER_WAIT_DURATION


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


def find_element_by_xpath_with_wait(driver, xpath, duration: int | None = None) -> WebElement:
    wait_duration = derive_wait_duration(duration)
    return WebDriverWait(driver, wait_duration).until(EC.element_to_be_clickable((AppiumBy.XPATH, xpath)))
    

def find_element_by_testid_with_wait(driver, data_testid, duration: int | None = None) -> WebElement:
    data_test_id_string = data_test_id_pattern.format(data_testid)
    wait_duration = derive_wait_duration(duration)
    return WebDriverWait(driver, wait_duration).until(EC.element_to_be_clickable((AppiumBy.XPATH, data_test_id_string)))

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
def wait_for_element_visibility(driver, locator, duration: int | None = None) -> bool:
    wait_duration = derive_wait_duration(duration)
    return WebDriverWait(driver, wait_duration).until(EC.visibility_of(locator)) is not None


def find_visible_element_by_xpath(driver, xpath_string, duration: int | None = None) -> WebElement:
    wait_duration = derive_wait_duration(duration)
    return WebDriverWait(driver, wait_duration).until(EC.visibility_of_element_located((AppiumBy.XPATH, xpath_string)))


def find_visible_element_by_testid(driver, data_testid, duration: int | None = None) -> WebElement:
    data_test_id_string = data_test_id_pattern.format(data_testid)
    wait_duration = derive_wait_duration(duration)
    visibility_of_element = WebDriverWait(driver, wait_duration).until(EC.visibility_of_element_located((AppiumBy.XPATH, data_test_id_string)))
    return visibility_of_element


def invisibility_of_element_by_xpath(driver, xpath, duration: int | None = None) -> bool:
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

def find_presence_element_by_xpath(driver, xpath, duration: int | None = None) -> WebElement:
    wait_duration = derive_wait_duration(duration)
    # Wait for the spinner to appear
    return WebDriverWait(driver, wait_duration).until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))


def find_presence_element_by_testid(driver, data_testid, duration: int | None = None) -> WebElement:
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
    
    # Will be use in search function (current phase)
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
                                                TO CLEAR INPUT FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Clear the field
def clear_input_field(element):
    element.click()
    element.clear()

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
    
    return label

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                FOR LOADING ICON - Mobile
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Checking the loading spinner
def spinner_element(driver):
    try:
        invisibility_of_element_by_testid(driver, data_testid=DataTestID.SPIN_LOADER)
    except Exception as e:
        # Attach a screenshot with the function name in the filename
        take_screenshot(driver, f"Exception_Screenshot")
        # Handle any exceptions that occur during the execution
        raise Exception("Timeout waiting for loading icon to disappear. Check if the API is slow")
    

def bulk_spinner_element(driver, timeout=10):
    try:
        # Wait for the spinner to disappear
        WebDriverWait(driver, timeout).until(EC.invisibility_of_element((AppiumBy.CSS_SELECTOR, "[data-testid='spin-loader']")))
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
        raise Exception("Timeout waiting for loading icon to disappear. Check if the API is slow")
    
    

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                               SCROLLABLE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Scroll Horizontal (Right)
def scroll_horizontally_right_scrollview(driver): 
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true).className("android.widget.HorizontalScrollView")).setAsHorizontalList().scrollForward()')

# Scroll Horizontal (Left)
def scroll_horizontally_left(driver): 
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true).className("android.widget.HorizontalScrollView")).setAsHorizontalList().scrollBackward()')

# Scrolls down
def scroll_vertically_down(driver): 
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true).className("android.widget.ScrollView")).scrollForward()')

# Scrolls up
def scroll_vertically_up(driver): 
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true).className("android.widget.ScrollView")).scrollBackward()')
    
    
def scroll_horizontally_right_scrollview(driver): 
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true)className("android.widget.ScrollView")).setAsHorizontalList().scrollForward()')


def swipe_left(driver, element, percent=0.75):
    """
    Perform a left swipe on the given element.
    
    :param driver: Appium WebDriver instance
    :param element: WebElement to swipe on
    :param percent: Percentage of the element's width to swipe (default is 75%)
    """
    driver.execute_script("mobile: swipeGesture", {
        "elementId": element.id,
        "direction": "left",
        "percent": percent
    })
