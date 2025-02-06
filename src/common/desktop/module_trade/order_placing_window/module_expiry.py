from datetime import datetime

from constants.helper.element import click_element, find_element_by_testid, find_element_by_xpath, find_element_by_xpath_with_wait, javascript_click
from constants.helper.error_handler import handle_exception



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - SPECIFIED DATE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def select_specified_date(driver, trade_type, expiryDate, targetMonth):
    """
    This function selects a specified expiry date from a calendar widget on the webpage.
    It ensures the calendar is navigated to the target month and then selects the expiry date.

    Arguments:
    - trade_type: The type of trade (e.g., "trade", "edit") to locate the expiry date field.
    - expiryDate: The expiry date to be selected (e.g., "15").
    - targetMonth (datetime): The target month (e.g., datetime object for "Dec 2025").

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        
        # Locate and click on the date input field for choosing the expiry date
        date_field = find_element_by_testid(driver, data_testid=f"{trade_type}-input-expiry-date")
        javascript_click(driver, element=date_field)

        # Loop until the calendar navigates to the target month
        while True:
            # Get the current month and year displayed on the calendar
            year_month = find_element_by_xpath_with_wait(driver, "//button[@class='react-calendar__navigation__label']").text
            currentMonth = datetime.strptime(year_month, "%b %Y")
            # If the current month matches the target month, break the loop
            if currentMonth == targetMonth:
                break
            else:
                # Click the "next" button to move to the next month
                next_btn = find_element_by_xpath_with_wait(driver, "//button[contains(@class, 'react-calendar__navigation__next-button')]")
                click_element(next_btn)
        
        # Locate and select the expiry date from the calendar
        start_date_picker = find_element_by_xpath_with_wait(driver, f"//div[contains(@class, 'month-view__days')]/button[not(contains(@class, 'neighboringMonth'))]/abbr[.='{expiryDate}']")
        click_element(start_date_picker)
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
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
    """
    This function selects a specific time option from a dropdown or selection list
    for the given trade type and option type (e.g., expiry time, start time, etc.).

    Arguments:
    - trade_type: The type of trade (e.g., "trade", "edit") that helps locate the time option.
    - option_type: The type of option (e.g., "expiry", "start") for which we are selecting the time.
    - option_value: The time value to select (e.g., "10:00 AM", "14:30").

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        
        # Build the XPath to find the specific time option element based on trade type, option type, and value
        time_option = find_element_by_xpath(driver, f"//div[@data-testid='{trade_type}-input-expiry-time-{option_type}']/div[text()='{option_value}']")
        javascript_click(driver, element=time_option)
        
        # Find the time options container
        # time_options_container = find_element_by_testid(driver, data_testid=f"{trade_type}-input-expiry-time-{option_type}")
        
        # Find the specific time option element
        # time_option = time_options_container.find_element(By.XPATH, f"//div[text()='{option_value}']")
        # click_element(time_option)
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
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

def select_specified_date_and_time(driver, trade_type: str, expiryDate: str, targetMonth, hour_option: str, min_option: str):
    """
    This function selects a specific expiry date and time (hour and minute) for a trade.

    Arguments:
    - trade_type: The type of trade (e.g., 'trade', 'edit') to help locate the specific elements.
    - expiryDate: The expiry date to be selected (e.g., "15").
    - targetMonth (datetime): The target month to navigate to in the date picker.
    - hour_option: The hour option to select (e.g., '10', '14').
    - min_option: The minute option to select (e.g., '30', '45').

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        
        # Step 1: Select the specified expiry date by navigating through the month and clicking the correct date
        select_specified_date(driver, trade_type, expiryDate, targetMonth)

        # Step 2: Click on the time input field to open the time picker
        time_field = find_element_by_testid(driver, data_testid=f"{trade_type}-input-expiry-time")
        javascript_click(driver, element=time_field)

        # Step 3: Select the hour option from the available options
        select_time_option(driver, trade_type, "hour", hour_option)

        # Step 3: Select the minute option from the available options
        select_time_option(driver, trade_type, "minute", min_option)
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
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

def expiry(driver, trade_type: str, expiryType: str, expiryDate: str, targetMonth, hour_option: str, min_option: str, specifiedDate: bool = False):
    """
    This function handles the expiry selection for a trade, including options for expiry type, date, and time.

    Arguments:
    - trade_type: The type of trade (e.g., "trade", "edit") to help locate the specific elements.
    - expiryType: The expiry type to select (e.g., 'good-till-date', 'good-till-day', 'specified-date', 'specified-date-and-time').
    - expiryDate: The expiry date to be selected (e.g., "15").
    - targetMonth (datetime): The target month to navigate to in the date picker (for date selection).
    - hour_option: The hour option to select (e.g., '10', '14').
    - min_option: The minute option to select (e.g., '30', '45').
    - specifiedDate (bool): A flag to indicate if a specific date and time need to be selected (default is False).

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        
        # Step 1: Open the expiry dropdown
        expiry_dropdown = find_element_by_testid(driver, data_testid=f"{trade_type}-dropdown-expiry")
        javascript_click(driver, element=expiry_dropdown)

        # Step 2: Select the expiry option from the dropdown
        expiry_options = find_element_by_testid(driver, data_testid=f"{trade_type}-dropdown-expiry-{expiryType}")
        click_element(expiry_options)
        
        # Step 3: If a specified date or specified date and time is required, proceed with further selection
        if specifiedDate: # IF flag TRUE
            if expiryType == "specified-date":
                select_specified_date(driver, trade_type, expiryDate, targetMonth)
            elif expiryType == "specified-date-and-time":
                select_specified_date_and_time(driver, trade_type, expiryDate, targetMonth, hour_option, min_option)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
