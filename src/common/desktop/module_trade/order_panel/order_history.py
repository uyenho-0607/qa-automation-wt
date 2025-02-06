import traceback

from datetime import datetime

from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text
from constants.helper.element import spinner_element, click_element, click_element_with_wait, find_list_of_elements_by_testid, find_element_by_testid, visibility_of_element_by_testid, visibility_of_element_by_xpath, get_label_of_element
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
        # Open the calendar by clicking on the calendar button
        calendar_button = visibility_of_element_by_testid(driver, data_testid="calender-button-assets")
        click_element_with_wait(driver, element=calendar_button)

        # Find the next, previous, and year-month navigation buttons
        next_btn = visibility_of_element_by_xpath(driver, "//button[contains(@class, 'react-calendar__navigation__next-button')]")

        prev_btn = visibility_of_element_by_xpath(driver, "//button[contains(@class, 'react-calendar__navigation__prev-button')]")

        year_month = visibility_of_element_by_xpath(driver, "//button[@class='react-calendar__navigation__label']")
        
        # Navigate to the target start month
        while True:
            current_startMonth = datetime.strptime(year_month.text, "%B %Y")
            print("current start month", current_startMonth)
            if current_startMonth == target_startMonth:
                print("target start month", target_startMonth)
                break
            elif current_startMonth < target_startMonth:
                next_btn.click() # Move to the next month
            else:
                prev_btn.click()  # Move to the previous month
        
        # Select the start date from the calendar
        startDate_picker = visibility_of_element_by_xpath(driver, f"//div[starts-with(@class, 'react-calendar__month-view__days')]//button[not(contains(@class, 'neighboringMonth'))]/abbr[.='{startDate}']")
        click_element(startDate_picker)
        
        # Navigate to the target end month
        while True:
            current_endMonth = datetime.strptime(year_month.text, "%B %Y")
            print("current end month", current_endMonth)
            if current_endMonth == target_endMonth:
                print("target end month", target_endMonth)
                break
            elif current_endMonth < target_endMonth:
                next_btn.click() # Move to the next month
            else:
                prev_btn.click()  # Move to the previous month
        
        # Select the end date from the calendar
        endDate_picker = visibility_of_element_by_xpath(driver, f"//div[starts-with(@class, 'react-calendar__month-view__days')]//button[not(contains(@class, 'neighboringMonth'))]/abbr[.='{endDate}']")
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
    - date_str (str): The date string to check, in the format "%Y-%m-%d %H:%M:%S".
    - start_dt (datetime): The start date of the range.
    - end_dt (datetime): The end date of the range.

    Returns:
    - bool: True if the date_str is within the range, False otherwise.
    """
    # Convert table date to datetime object
    date_dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    # Check if the date is within the datepicker range
    return start_dt.date() <= date_dt.date() <= end_dt.date()



def OH_closeDate(driver, startDate: str, endDate: str, target_startMonth: str, target_endMonth: str):
    """
    Verifies that the "Closed Date" values from the Order History table are within the specified date range.

    This function interacts with the calendar date picker to select a date range, retrieves the 
    "Close Date" values from the table, and checks if each date falls within the selected range.

    Arguments:
    - startDate (str): The start date in the format '03'.
    - endDate (str): The end date in the format '05'.
    - target_startMonth (str): The target start month for calendar selection. (e.g. datetime.strptime("October 2025", "%B %Y"))
    - target_endMonth (str): The target end month for calendar selection. (e.g. datetime.strptime("November 2025", "%B %Y"))

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Ensure the page is fully loaded and any spinner is gone
        spinner_element(driver)
        
        # Select the target date range using the date picker
        calendar_datePicker(driver, startDate, endDate, target_startMonth, target_endMonth)

        # Extract the selected date range from the calendar picker label
        label_date = find_element_by_testid(driver, data_testid="calender-button-assets-content")
        date_content = get_label_of_element(element=label_date)
        
        # Extract the date range from the content (assuming the format is DD/MM/YYYY - DD/MM/YYYY)
        start_date_str, end_date_str = date_content.split(" - ")
        
        # Convert the extracted date range into datetime objects (in the format DD/MM/YYYY)
        datepicker_start_dt = datetime.strptime(start_date_str, "%d/%m/%Y")
        datepicker_end_dt = datetime.strptime(end_date_str, "%d/%m/%Y")

        delay(2)

        # Locate the table body
        get_table_body(driver)
        
        # Locate the table header
        get_table_headers(driver)
        
        # Wait till the spinner icon no longer display
        spinner_element(driver)
        
        # Extract all elements containing the "Close Date" values
        OH_closeDate_elements = find_list_of_elements_by_testid(driver, data_testid="asset-history-column-close-date")
        
        # Iterate over each close date element
        for element in OH_closeDate_elements:
            table_date = element.text  # Extract the date text from the WebElement
            if is_within_range(table_date, datepicker_start_dt, datepicker_end_dt):
                attach_text(f"{table_date} is within the datepicker range {date_content}", name=f"Order History Date: {table_date}")
                assert True  # If the date is within range, assert True
            else:
                attach_text(f"{table_date} is outside the datepicker range {date_content}", name=f"Order History Date: {table_date}")
                assert False,  f"An exception occurred: {str(e)}\n{traceback.format_exc()}"

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)    

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""