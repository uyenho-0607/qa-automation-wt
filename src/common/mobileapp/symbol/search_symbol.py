import random
import traceback

from constants.helper.screenshot import take_screenshot
from constants.helper.element_android_app import click_element_with_wait, find_element_by_xpath, wait_for_text_to_be_present_in_element_by_xpath, populate_element_with_wait, visibility_of_element_by_testid, get_label_of_element
from data_config.file_handler import read_symbol_file


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                INPUT SYMBOL
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def input_symbol(driver, filename, desired_symbol_name=None):
    try:

        # Load symbols from file
        symbols = read_symbol_file(filename)
        
        # If a specific symbol is provided, use it; otherwise, select a random one
        if desired_symbol_name is None:
            desired_symbol_name = random.choice(symbols)
        else:
            # Check if the desired symbol is in the list of symbols
            if desired_symbol_name not in symbols:
                raise ValueError(f"The desired symbol '{desired_symbol_name}' is not in the list of available symbols.")

        search_magnifying_glass = visibility_of_element_by_testid(driver, data_testid="symbol-search-selector")
        click_element_with_wait(driver, element=search_magnifying_glass)
        
        search_input = visibility_of_element_by_testid(driver, data_testid="symbol-input-search")
        
        # Enter the random symbol into the search input
        populate_element_with_wait(driver, element=search_input, text=desired_symbol_name)
        
        # Simulate pressing the Enter key or other key codes
        driver.press_keycode(66) # Keycode 66 is for Enter on Android
        # if driver.capabilities['platformName'].lower() == 'android':
        #     driver.press_keycode(66) # Android Enter key
        # else:
        #     element.send_keys("\n") # iOS Enter key

        dropdown = find_element_by_xpath(driver, f"//*[@resource-id='symbol-input-search-items']//android.widget.TextView[contains(@text, '{desired_symbol_name}')]")

        click_element_with_wait(driver, element=dropdown)

        chart_symbol_name = wait_for_text_to_be_present_in_element_by_xpath(driver, "//android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.TextView[2]", text=desired_symbol_name)
        if chart_symbol_name:
            assert True
            return
        else:
            chart_symbol_name = find_element_by_xpath(driver, "//android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.TextView[2]")
            chart_symbolName = get_label_of_element(element=chart_symbol_name)
            assert False, f"Invalid Symbol Name: {chart_symbolName}"
    
    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, f"Exception Screenshot: Invalid Symbol Name:{desired_symbol_name}")
        # Log the full exception message and stacktrace
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""