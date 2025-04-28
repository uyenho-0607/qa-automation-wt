import pandas as pd

from tabulate import tabulate

from constants.element_ids import DataTestID

from constants.helper.driver import delay
from constants.helper.element_android_app import wait_for_list_of_element_visibility_by_xpath
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text
from constants.helper.element import find_list_of_elements_by_xpath, spinner_element, find_visible_element_by_testid


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TABLE BODY FUNCTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_table_body(driver):
    try:
        
        # Wait till the spinner icon no longer display
        spinner_element(driver)
        
        return find_visible_element_by_testid(driver, ".//tbody[contains(@data-testid, 'list')]")
    
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

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
        
        wait_for_list_of_element_visibility_by_xpath(driver, DataTestID.ASSET_DETAILED_LABEL)
        
        thead_rows = find_list_of_elements_by_xpath(driver, DataTestID.ASSET_DETAILED_LABEL)
        thead_data = [header.text for header in thead_rows if header.text.strip() != '']
        
        for i, header in enumerate(thead_data):
            if header.lower() in ("price", "entry price"):
                thead_data[i] = "Entry Price"
                break
        
        return thead_data

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

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
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

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
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""