
from selenium.webdriver.common.by import By

from constants.helper.error_handler import handle_exception
from constants.helper.element_android_app import get_label_of_element, spinner_element, find_visible_element_by_xpath, find_element_by_xpath, wait_for_text_to_be_present_in_element_by_xpath

from common.mobileapp.module_sub_menu.utils import menu_button
from enums.main import Menu


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SECTION MY TRADE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def inspect_my_trade_orders(driver, symbol_name, order_type):
    try:
        # Redirect to the Markets page
        menu_button(driver, menu=Menu.MARKET)
        
        # Wait till the spinner icon no longer displays
        spinner_element(driver)
        
        # Wait until the rows in 'My Trade' section are loaded
        top_row = find_visible_element_by_xpath(driver, "//div[@class='sc-1g7mcs0-0 iiKKcu'][1]")
        
        # Validate symbol name in the top row
        displayed_symbol = top_row.find_element(By.XPATH, "//div[@data-testid='portfolio-row-symbol']").text.strip()
        
        if displayed_symbol != symbol_name:
            raise AssertionError(f"Symbol '{symbol_name}' is not found in the top row, instead found '{displayed_symbol}'")
        
        # Validate order type (BUY/SELL)
        displayed_order_type = top_row.find_element(By.XPATH, "//span[@data-testid='portfolio-row-order-type']").text.strip()
        
        if displayed_order_type.upper() != order_type.upper():
            raise AssertionError(f"Order type '{order_type}' does not match displayed type '{displayed_order_type}'")
        
        print(f"Order for symbol '{symbol_name}' with order type '{order_type}' is correctly displayed in the top row.")
        assert True
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)



def verify_no_orders_in_my_trades(driver):
    try:
        # Redirect to the Markets page
        menu_button(driver, menu=Menu.MARKET)
        
        # Wait till the spinner icon no longer displays
        spinner_element(driver)
        
        # Wait until the rows in 'My Trade' section are loaded
        match = wait_for_text_to_be_present_in_element_by_xpath(driver, "//div[contains(text(), 'You do not have any trades here')]", text="You do not have any trades here")
        if match:
            text = find_element_by_xpath(driver, "//div[contains(text(), 'You do not have any trades here')]")
            print(get_label_of_element(element=text))
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""