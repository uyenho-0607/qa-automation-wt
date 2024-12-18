from datetime import datetime
from selenium.webdriver.common.by import By

from constants.helper.element import click_element_with_wait, find_element_by_testid, find_element_by_xpath_with_wait, javascript_click
from constants.helper.error_handler import handle_exception


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - SPECIFIED DATE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def select_specified_date(driver, trade_type, expiryDate, targetMonth):
    try:    
        # Click on the input field for choosing date
        date_field = find_element_by_testid(driver, data_testid=f"{trade_type}-input-expiry-date")
        javascript_click(driver, element=date_field)
        # click_element_with_wait(driver, element=date_field)

        while True:
            year_month = find_element_by_xpath_with_wait(driver, "//button[@class='react-calendar__navigation__label']").text
            currentMonth = datetime.strptime(year_month, "%b %Y")
            if currentMonth == targetMonth:
                break
            else:
                next_btn = find_element_by_xpath_with_wait(driver, "//button[contains(@class, 'react-calendar__navigation__next-button')]")
                click_element_with_wait(driver, element=next_btn)

        start_date_picker = find_element_by_xpath_with_wait(driver, f"//div[contains(@class, 'month-view__days')]/button[not(contains(@class, 'neighboringMonth'))]/abbr[.='{expiryDate}']")
        click_element_with_wait(driver, element=start_date_picker)
        
    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - SPECIFIED TIME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def select_time_option(driver, trade_type, option_type, option_value):
    try:
        
        # Find the time options container
        time_options_container = find_element_by_testid(driver, data_testid=f"{trade_type}-input-expiry-time-{option_type}")
        
        # Find the specific time option element
        time_option = time_options_container.find_element(By.XPATH, f"//div[text()='{option_value}']")
        
        javascript_click(driver, element=time_option)
        
    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
        

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - SPECIFIED DATE AND TIME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def select_specified_date_and_time(driver, trade_type, expiryDate, targetMonth, hour_option, min_option):
    try:
        
        # Select the specified date
        select_specified_date(driver, trade_type, expiryDate, targetMonth)

        # Click on the input field for choosing time.
        time_field = find_element_by_testid(driver, data_testid=f"{trade_type}-input-expiry-time")

        javascript_click(driver, element=time_field)
        # click_element_with_wait(driver, element=time_field)

        # Find and click the hour option
        select_time_option(driver, trade_type, "hour", hour_option)

        # Find and click the minute option
        select_time_option(driver, trade_type, "minute", min_option)
        
    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - EXPIRY FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def expiry(driver, trade_type, expiryType, expiryDate, targetMonth, hour_option, min_option, specifiedDate: bool = False):
    try:

        # Click on the expiry dropdown
        expiry_dropdown = find_element_by_testid(driver, data_testid=f"{trade_type}-dropdown-expiry")
        javascript_click(driver, element=expiry_dropdown)
        # click_element_with_wait(driver, element=expiry_dropdown)

        # Select the Expiry option dropdown
        expiry_options = find_element_by_testid(driver, data_testid=f"{trade_type}-dropdown-expiry-{expiryType}")
        click_element_with_wait(driver, element=expiry_options)
        
        if specifiedDate: # IF TRUE
            if expiryType == "specified-date":
                select_specified_date(driver, trade_type, expiryDate, targetMonth)
            elif expiryType == "specified-date-and-time":
                select_specified_date_and_time(driver, trade_type, expiryDate, targetMonth, hour_option, min_option)

    except Exception as e:
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""