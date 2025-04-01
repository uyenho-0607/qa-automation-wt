import traceback

# from datetime import datetime
from dateutil.parser import parse
from constants.helper.driver import delay
from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element import find_list_of_elements_by_xpath, spinner_element, click_element, click_element_with_wait, find_list_of_elements_by_testid, find_element_by_testid, find_visible_element_by_testid, find_visible_element_by_xpath, get_label_of_element

from common.desktop.module_trade.order_panel.op_general import get_table_body, get_table_headers


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER HISTORY - CALENDAR DATEPICKER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Order History - Calendar datepicker
def calendar_datePicker(driver, startDate, endDate, target_startMonth, target_endMonth):
    """
    Selects a date range from a calendar widget by navigating to the desired start and end months
    and selecting the specific start and end dates.

    Arguments:
    - startDate: The start date to select (in a format that matches the calendar's display, e.g., '1', '10', etc.).
    - endDate: The end date to select (similar format to startDate).
    - target_startMonth: The target month for the start date, represented as a datetime object.
    - target_endMonth: The target month for the end date, represented as a datetime object.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        spinner_element(driver)
        
        # Open the calendar by clicking on the calendar button
        calendar_button = find_visible_element_by_testid(driver, data_testid="calender-button-assets")
        click_element_with_wait(driver, element=calendar_button)

        # Find the next, previous, and year-month navigation buttons
        btn_next = find_visible_element_by_xpath(driver, "//button[contains(@class, 'react-calendar__navigation__next-button')]")

        btn_prev = find_visible_element_by_xpath(driver, "//button[contains(@class, 'react-calendar__navigation__prev-button')]")

        year_month = find_visible_element_by_xpath(driver, "//button[@class='react-calendar__navigation__label']")
        
        # Navigate to the target start month
        while True:
            current_startMonth = parse(year_month.text)
            if current_startMonth == target_startMonth:
                break
            elif current_startMonth < target_startMonth:
                btn_next.click() # Move to the next month
            else:
                btn_prev.click()  # Move to the previous month
        
        # Select the start date from the calendar
        startDate_picker = find_visible_element_by_xpath(driver, f"//div[starts-with(@class, 'react-calendar__month-view__days')]//button[not(contains(@class, 'neighboringMonth'))]/abbr[.='{startDate}']")
        click_element(startDate_picker)
        
        # Navigate to the target end month
        while True:
            current_endMonth = parse(year_month.text)
            if current_endMonth == target_endMonth:
                break
            elif current_endMonth < target_endMonth:
                btn_next.click() # Move to the next month
            else:
                btn_prev.click()  # Move to the previous month
        
        # Select the end date from the calendar
        endDate_picker = find_visible_element_by_xpath(driver, f"//div[starts-with(@class, 'react-calendar__month-view__days')]//button[not(contains(@class, 'neighboringMonth'))]/abbr[.='{endDate}']")
        click_element(endDate_picker)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)   
      
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER HISTORY - RETRIEVE THE DATE COLUMN
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



# Function to check if a table date is within the datepicker range
def is_within_range(date_str, start_dt, end_dt):
    """
    Checks if a given date string is within the specified date range.
    
    Arguments:
    - date_str (str): The date string to check.
    - start_dt (datetime): The start date of the range.
    - end_dt (datetime): The end date of the range.
    
    Returns:
    - bool: True if the date_str is within the range, False otherwise.
    """
    # Convert table date to datetime object
    date_dt = parse(date_str)
    # Check if the date is within the datepicker range
    return start_dt.date() <= date_dt.date() <= end_dt.date()


def OH_closeDate(driver, startDate: str, endDate: str, target_startMonth: str, target_endMonth: str):
    """
    Verifies that the "Closed Date" values from the Order History table are within the specified date range.
    """
    try:
        # Wait for spinner element to disappear
        spinner_element(driver)
        
        calendar_datePicker(driver, startDate, endDate, target_startMonth, target_endMonth)
        
        label_date = find_element_by_testid(driver, data_testid="calender-button-assets-content")
        date_content = get_label_of_element(element=label_date)
        
        start_date_str, end_date_str = date_content.split(" - ")
        
        # Convert the extracted date range into datetime objects
        datepicker_start_dt = parse(start_date_str)
        datepicker_end_dt = parse(end_date_str)
        
        delay(2)
        
        get_table_body(driver)
        get_table_headers(driver)
        spinner_element(driver)
        
        OH_closeDate_elements = find_list_of_elements_by_testid(driver, data_testid="asset-history-column-close-date")
        if not OH_closeDate_elements:
            empty_message_elements = find_list_of_elements_by_xpath(driver, "//tbody[contains(@data-testid, '-list')]//div[@data-testid='empty-message']")
            if empty_message_elements:
                empty_message = empty_message_elements[0].text.strip()
                assert False, f"Table is empty. Message: '{empty_message}'"
        
        for element in OH_closeDate_elements:
            table_date = element.text
            if is_within_range(table_date, datepicker_start_dt, datepicker_end_dt):
                attach_text(f"{table_date} is within the datepicker range {date_content}", name=f"Order History Date: {table_date}")
                assert True
            else:
                attach_text(f"{table_date} is outside the datepicker range {date_content}", name=f"Order History Date: {table_date}")
                assert False, f"Date {table_date} is out of range."
    
    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""