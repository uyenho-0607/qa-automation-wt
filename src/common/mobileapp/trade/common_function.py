# Extract the RGB color
import traceback
import pandas as pd

from tabulate import tabulate


from constants.helper.screenshot import attach_text, take_screenshot
from constants.helper.element_android_app import find_element_by_testid, find_list_of_elements_by_xpath, spinner_element, visibility_of_element_by_xpath


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TABLE BODY FUNCTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_table_body(driver):
    try:
        
        # Wait till the spinner icon no longer display
        spinner_element(driver)
        
        return visibility_of_element_by_xpath(driver, ".//tbody[contains(@data-testid, 'list')]")
    
    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "get_table_body - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER PANEL - TABLE HEADER NAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_table_headers(driver):
    try:
        
        # Wait till the element is visible
        visibility_of_element_by_xpath(driver, "//div[contains(@data-testid, 'label')]")
        
        thead_rows = find_list_of_elements_by_xpath(driver, "//div[contains(@data-testid, 'label')]")
        thead_data = [header.text for header in thead_rows if header.text.strip() != '']
        
        print("table header name", thead_data)
        for i, header in enumerate(thead_data):
            if header.lower() in ("price", "entry price"):
                thead_data[i] = "Entry Price"
                break
        return thead_data

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "get_table_headers - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER PANEL - RETRIEVE EACH INDIVDIUAL ORDER ROW - ORDERID
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def process_individual_orders(driver, orderPanel_data, table_order_ids):
    try:

        for order_id in table_order_ids:
            individual_order_data = orderPanel_data[orderPanel_data['Order No.'] == order_id]
            if not individual_order_data.empty:
                individual_order_data_transposed = individual_order_data.set_index('Section').T.fillna('-')
                overall = tabulate(individual_order_data_transposed, headers='keys', tablefmt='grid', stralign='center')
                attach_text(overall, name=f"Table for Order No.: {order_id}")

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "process_individual_orders - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER PANEL - CREATE DATAFRAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def extract_order_data_details(driver, table_row_contents, thead_data, section_name):
    try:
        
        order_data_details = pd.DataFrame([table_row_contents], columns=thead_data)
        order_data_details['Section'] = section_name

        return order_data_details
    
    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "create_order_panel_data - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""