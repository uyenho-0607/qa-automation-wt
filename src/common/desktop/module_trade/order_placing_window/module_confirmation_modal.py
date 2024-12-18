import re
import pandas as pd

from tabulate import tabulate

from constants.helper.element import click_element, find_element_by_testid, find_list_of_elements_by_xpath, find_list_of_elements_by_testid, find_element_by_xpath, visibility_of_element_by_xpath, get_label_of_element
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - TRADE CONFIRMATION DIALOG DETAILS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def trade_ordersConfirmationDetails(driver, trade_type):
    try:

        result = []
        
        # Ensure the confirmation modal is visible
        visibility_of_element_by_xpath(driver, "//div[contains(@data-testid, 'confirmation-modal')]")

        # Retrieve headers for trade confirmation
        trade_order_header_elements = find_list_of_elements_by_xpath(driver, "//div[contains(@data-testid, 'confirmation-label')]")

        trade_confirmation_headers = [header.text for header in trade_order_header_elements]
        
        # Handle different table headers ("Price" or "Entry Price") for consistency
        for i, header in enumerate(trade_confirmation_headers):
            if header in ("Price"):
                trade_confirmation_headers[i] = "Entry Price"
                break
            
        # Retrieve order type
        order_type_element = find_element_by_xpath(driver, "//div[contains(@data-testid, 'confirmation-order-type')]")
        trade_confirmation_headers.append("Type")

        # Retrieve symbol name
        symbol_name_element = find_element_by_xpath(driver, "//div[contains(@data-testid, 'confirmation-symbol')]")
        trade_confirmation_headers.append("Symbol")
        
        # Wait for the elements to be present and extract their text
        elements = find_list_of_elements_by_testid(driver, data_testid=f"{trade_type}-confirmation-value")

        for element in elements:
            result.append(get_label_of_element(element))

        label_order_type = get_label_of_element(order_type_element)
        result.append(label_order_type)

        label_symbol_name = get_label_of_element(symbol_name_element)
        result.append(label_symbol_name)
        
        # Handle "edit" trade type and extract order number if available
        if trade_type == "edit":

            # Check if "order_number_element" exists
            order_number_elements = find_element_by_testid(driver, data_testid=f"edit-confirmation-order-id")
            extracted_orderID = get_label_of_element(order_number_elements)

            if order_number_elements:       
                order_number = re.search(r'\d+', extracted_orderID).group()
                
                # Append the order number to the result list
                result.append(order_number)
                
                # Add the new header for order number only if it exists
                trade_confirmation_headers.append("Order No.")

        # Create a DataFrame using the data
        trade_order_details = pd.DataFrame([result], columns=trade_confirmation_headers)
        trade_order_details['Section'] = "Trade Confirmation Details"
        
        # Transpose DataFrame and format it for output
        master_df_transposed = trade_order_details.set_index('Section').T.fillna('-')
        overall = tabulate(master_df_transposed, headers='keys', tablefmt='grid', stralign='center')
        attach_text(overall, name="Trade Confirmation Details")

        # To click on the confirm button
        button_confirmation = find_element_by_testid(driver, data_testid=f"{trade_type}-confirmation-button-confirm")
        click_element(button_confirmation)

        return trade_order_details

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""