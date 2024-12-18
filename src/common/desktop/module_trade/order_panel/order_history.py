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
    try:
        
        calendar_button = visibility_of_element_by_testid(driver, data_testid="calender-button-assets")
        click_element_with_wait(driver, element=calendar_button)

        next_btn = visibility_of_element_by_xpath(driver, "//button[contains(@class, 'react-calendar__navigation__next-button')]")

        prev_btn = visibility_of_element_by_xpath(driver, "//button[contains(@class, 'react-calendar__navigation__prev-button')]")

        year_month = visibility_of_element_by_xpath(driver, "//button[@class='react-calendar__navigation__label']")

        while True:
            current_startMonth = datetime.strptime(year_month.text, "%B %Y")
            print("current start month", current_startMonth)
            if current_startMonth == target_startMonth:
                print("target start month", target_startMonth)
                break
            elif current_startMonth < target_startMonth:
                next_btn.click()
            else:
                prev_btn.click()
                
        startDate_picker = visibility_of_element_by_xpath(driver, f"//div[starts-with(@class, 'react-calendar__month-view__days')]//button[not(contains(@class, 'neighboringMonth'))]/abbr[.='{startDate}']")
        click_element(startDate_picker)

        while True:
            current_endMonth = datetime.strptime(year_month.text, "%B %Y")
            print("current end month", current_endMonth)
            if current_endMonth == target_endMonth:
                print("target end month", target_endMonth)
                break
            elif current_endMonth < target_endMonth:
                next_btn.click()
            else:
                prev_btn.click()
                
        endDate_picker = visibility_of_element_by_xpath(driver, f"//div[starts-with(@class, 'react-calendar__month-view__days')]//button[not(contains(@class, 'neighboringMonth'))]/abbr[.='{endDate}']")
        click_element(endDate_picker)

    except Exception as e:
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
    # Convert table date to datetime object
    date_dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    # Check if the date is within the datepicker range
    return start_dt.date() <= date_dt.date() <= end_dt.date()



def OH_closeDate(driver, startDate, endDate, target_startMonth, target_endMonth):
    try:

        spinner_element(driver)
        
        calendar_datePicker(driver, startDate, endDate, target_startMonth, target_endMonth)

        # calendar picker date label
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
        
        OH_closeDate_elements = find_list_of_elements_by_testid(driver, data_testid="asset-history-column-close-date")
        
        # Iterate over each close date element
        for element in OH_closeDate_elements:
            table_date = element.text  # Extract the date text from the WebElement
            if is_within_range(table_date, datepicker_start_dt, datepicker_end_dt):
                attach_text(f"{table_date} is within the datepicker range {date_content}", name=f"Order History Date: {table_date}")
                assert True
            else:
                attach_text(f"{table_date} is outside the datepicker range {date_content}", name=f"Order History Date: {table_date}")
                assert False,  f"An exception occurred: {str(e)}\n{traceback.format_exc()}"

    except Exception as e:
        handle_exception(driver, e)