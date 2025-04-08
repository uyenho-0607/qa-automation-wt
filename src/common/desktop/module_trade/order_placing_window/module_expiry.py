from dateutil.parser import parse
from selenium.webdriver.common.by import By

from enums.main import ButtonModuleType, ExpiryType, TimeOptionType
from constants.element_ids import DataTestID

from constants.helper.element import click_element, find_element_by_testid, find_element_by_testid_with_wait, find_element_by_xpath_with_wait, javascript_click
from constants.helper.error_handler import handle_exception



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - SPECIFIED DATE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def select_specified_date(driver, trade_type: ButtonModuleType, expiry_date, target_month):
    """
    This function selects a specified expiry date from a calendar widget on the webpage.
    It ensures the calendar is navigated to the target month and then selects the expiry date.

    Arguments:
    - trade_type: The type of trade (e.g., "trade", "edit") to locate the expiry date field.
    - expiry_date: The expiry date to be selected (e.g., "15").
    - target_month (datetime): The target month (e.g., datetime object for "Dec 2025").

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    
    # Determine the data-testid based on the button type
    button_testids = {
        ButtonModuleType.TRADE: DataTestID.TRADE_INPUT_EXPIRY_DATE,
        ButtonModuleType.EDIT: DataTestID.EDIT_INPUT_EXPIRY_DATE,
    }
    
    button_testid = button_testids.get(trade_type)
    
    # Locate and click on the date input field for choosing the expiry date
    date_field = find_element_by_testid(driver, data_testid=button_testid)
    javascript_click(driver, element=date_field)

    # Loop until the calendar navigates to the target month
    while True:
        # Get the current month and year displayed on the calendar
        year_month = find_element_by_xpath_with_wait(driver, "//button[@class='react-calendar__navigation__label']").text
        currentMonth = parse(year_month)

        # If the current month matches the target month, break the loop
        if currentMonth == target_month:
            break
        else:
            # Click the "next" button to move to the next month
            btn_next = find_element_by_xpath_with_wait(driver, "//button[contains(@class, 'react-calendar__navigation__next-button')]")
            click_element(btn_next)
    
    # Locate and select the expiry date from the calendar
    start_date_picker = find_element_by_xpath_with_wait(driver, f"//div[contains(@class, 'month-view__days')]/button[not(contains(@class, 'neighboringMonth'))]/abbr[.='{expiry_date}']")
    click_element(start_date_picker)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - SPECIFIED TIME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def select_time_option(driver, trade_type: ButtonModuleType, option_value:str, option_type: TimeOptionType):
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
    
    # Define mapping for dropdown and its options
    time_setting_map = {
        ButtonModuleType.TRADE: {
            TimeOptionType.HOUR : DataTestID.TRADE_INPUT_EXPIRY_TIME_HOUR,
            TimeOptionType.MINUTE : DataTestID.TRADE_INPUT_EXPIRY_TIME_MINUTE
        },
        ButtonModuleType.EDIT: {
            TimeOptionType.HOUR : DataTestID.EDIT_INPUT_EXPIRY_TIME_HOUR,
            TimeOptionType.MINUTE : DataTestID.EDIT_INPUT_EXPIRY_TIME_MINUTE
        }
    }
        
    time_formatter = time_setting_map[trade_type][option_type]
    
    # Find the time options container
    time_options_container = find_element_by_testid_with_wait(driver, data_testid=time_formatter)

    # Find the specific time option element
    time_option = time_options_container.find_element(By.XPATH, f".//*[normalize-space(text())='{option_value}']")
    javascript_click(driver, element=time_option)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
        

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - SPECIFIED DATE AND TIME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def select_specified_date_and_time(driver, trade_type: ButtonModuleType, expiry_date: str, target_month: str, hour_option: str, min_option: str):
    """
    This function selects a specific expiry date and time (hour and minute) for a trade.

    Arguments:
    - trade_type: The type of trade (e.g., 'trade', 'edit') to help locate the specific elements.
    - expiry_date: The expiry date to be selected (e.g., "15").
    - target_month (datetime): The target month to navigate to in the date picker.
    - hour_option: The hour option to select (e.g., '10', '14').
    - min_option: The minute option to select (e.g., '30', '45').

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    
    # Determine the data-testid based on the button type
    button_testids = {
        ButtonModuleType.TRADE: DataTestID.TRADE_INPUT_EXPIRY_TIME,
        ButtonModuleType.EDIT: DataTestID.EDIT_INPUT_EXPIRY_TIME,
    }
    
    # Step 1: Select the specified expiry date by navigating through the month and clicking the correct date
    select_specified_date(driver, trade_type, expiry_date, target_month)

    # Step 2: Click on the time input field to open the time picker
    button_testid = button_testids.get(trade_type)
    
    time_field = find_element_by_testid_with_wait(driver, data_testid=button_testid)
    javascript_click(driver, element=time_field)

    # Step 3: Select the hour option from the available options
    select_time_option(driver, trade_type, hour_option, option_type=TimeOptionType.HOUR)

    # Step 4: Select the minute option from the available options
    select_time_option(driver, trade_type, min_option, option_type=TimeOptionType.MINUTE)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - EXPIRY FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def expiry(driver, trade_type: ButtonModuleType, expiry_type: ExpiryType, expiry_date: str, target_month, hour_option: str, min_option: str):
    """
    This function handles the expiry selection for a trade, including options for expiry type, date, and time.

    Arguments:
    - trade_type: The type of trade (e.g., "trade", "edit") to help locate the specific elements.
    - expiry_type: The expiry type to select (e.g., 'good-till-date', 'good-till-day', 'specified-date', 'specified-date-and-time').
    - expiry_date: The expiry date to be selected (e.g., "15").
    - target_month (datetime): The target month to navigate to in the date picker (for date selection).
    - hour_option: The hour option to select (e.g., '10', '14').
    - min_option: The minute option to select (e.g., '30', '45').
    - specifiedDate (bool): A flag to indicate if a specific date and time need to be selected (default is False).

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        
        # Define mapping for dropdown and its options
        expiry_map = {
            ButtonModuleType.TRADE: {
                "dropdown": DataTestID.TRADE_DROPDOWN_EXPIRY,
                "options": {
                    ExpiryType.GOOD_TILL_CANCELLED: DataTestID.TRADE_DROPDOWN_EXPIRY_GOOD_TILL_CANCELLED,
                    ExpiryType.GOOD_TILL_DAY: DataTestID.TRADE_DROPDOWN_EXPIRY_GOOD_TILL_DAY,
                    ExpiryType.SPECIFIED_DATE: DataTestID.TRADE_DROPDOWN_EXPIRY_SPECIFIED_DATE,
                    ExpiryType.SPECIFIED_DATE_AND_TIME: DataTestID.TRADE_DROPDOWN_EXPIRY_SPECIFIED_DATE_AND_TIME
                }
            },
            ButtonModuleType.EDIT: {
                "dropdown": DataTestID.EDIT_DROPDOWN_EXPIRY,
                "options": {
                    ExpiryType.GOOD_TILL_CANCELLED: DataTestID.EDIT_DROPDOWN_EXPIRY_GOOD_TILL_CANCELLED,
                    ExpiryType.GOOD_TILL_DAY: DataTestID.EDIT_DROPDOWN_EXPIRY_GOOD_TILL_DAY,
                    ExpiryType.SPECIFIED_DATE: DataTestID.EDIT_DROPDOWN_EXPIRY_SPECIFIED_DATE,
                    ExpiryType.SPECIFIED_DATE_AND_TIME: DataTestID.EDIT_DROPDOWN_EXPIRY_SPECIFIED_DATE_AND_TIME
                }
            }
        }

        policy_data = expiry_map[trade_type]
        
        # Step 1: Open the expiry dropdown
        expiry_dropdown = find_element_by_testid(driver, data_testid=policy_data["dropdown"])
        click_element(element=expiry_dropdown)
        
        # # Step 2: Select the expiry option from the dropdown
        expiry_options = find_element_by_testid(driver, data_testid=policy_data["options"][expiry_type])
        click_element(element=expiry_options)
        
        # # Step 3: If a specified date or specified date and time is required, proceed with further selection
        if expiry_type == ExpiryType.SPECIFIED_DATE:
            select_specified_date(driver, trade_type, expiry_date, target_month)
        elif expiry_type == ExpiryType.SPECIFIED_DATE_AND_TIME:
            select_specified_date_and_time(driver, trade_type, expiry_date, target_month, hour_option, min_option)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""