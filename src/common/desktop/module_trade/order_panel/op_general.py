import pandas as pd

from tabulate import tabulate

from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text
from constants.helper.element import find_list_of_elements_by_xpath, visibility_of_element_by_xpath


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TABLE BODY FUNCTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_table_body(driver):
    try:
        
        return visibility_of_element_by_xpath(driver, ".//tbody[contains(@data-testid, 'list')]")
    
    except Exception as e:
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
        
        # Wait till the spinner icon no longer display
        # spinner_element(driver)

        thead_rows = find_list_of_elements_by_xpath(driver, "//thead[contains(@data-testid, 'table-header')]//th")
        thead_data = [header.text for header in thead_rows if header.text.strip() != '']
        for i, header in enumerate(thead_data):
            if header.lower() in ("price", "entry price"):
                thead_data[i] = "Entry Price"
                break
        return thead_data

    except Exception as e:
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
        
        orderPanel_data = pd.DataFrame(table_row_contents, columns=thead_data)
        orderPanel_data['Section'] = section_name

        return orderPanel_data
    
    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""