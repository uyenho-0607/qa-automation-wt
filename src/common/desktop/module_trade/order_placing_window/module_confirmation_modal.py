import re
import pandas as pd

from tabulate import tabulate

from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, find_element_by_testid, find_list_of_elements_by_xpath, find_list_of_elements_by_testid, find_element_by_xpath, visibility_of_element_by_xpath, get_label_of_element



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - TRADE CONFIRMATION DIALOG DETAILS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def trade_ordersConfirmationDetails(driver, trade_type):
    """
    This function handles the extraction of trade confirmation details, processes headers and values
    from the confirmation modal, and creates a DataFrame with the extracted data.

    Arguments:
    - trade_type: The type of trade (e.g.,  "trade", "edit") to adjust the logic for extraction.

    Returns:
    - trade_order_details (DataFrame): A DataFrame containing the trade confirmation details extracted from the modal.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        
        # Validate trade_type input
        if trade_type not in ["trade", "edit"]:
            raise ValueError(f"Invalid trade_type '{trade_type}' provided. Expected 'trade' or 'edit'.")
        
        # Initialize an empty list to store extracted values
        result = []
        
        # Ensure the trade confirmation modal is visible before proceeding
        visibility_of_element_by_xpath(driver, "//div[contains(@data-testid, 'confirmation-modal')]")

        # Retrieve all the headers from the trade confirmation modal
        trade_order_header_elements = find_list_of_elements_by_xpath(driver, "//div[contains(@data-testid, 'confirmation-label')]")
        trade_confirmation_headers = [header.text for header in trade_order_header_elements]
        
        # Handle different headers to ensure consistency in naming (e.g., changing "Price" to "Entry Price")
        for i, header in enumerate(trade_confirmation_headers):
            if header in ("Price"): # Update the header if found
                trade_confirmation_headers[i] = "Entry Price"
                break
            
        # Retrieve order type and symbol name, then append to headers
        order_type_element = find_element_by_xpath(driver, "//div[contains(@data-testid, 'confirmation-order-type')]")
        trade_confirmation_headers.append("Type")

        # Retrieve symbol name
        symbol_name_element = find_element_by_xpath(driver, "//div[contains(@data-testid, 'confirmation-symbol')]")
        trade_confirmation_headers.append("Symbol")
        
        # Retrieve the list of elements containing trade values based on the trade type (e.g., "edit" or "create")
        elements = find_list_of_elements_by_testid(driver, data_testid=f"{trade_type}-confirmation-value")

        # Extract text from each element and append to the result list
        for element in elements:
            result.append(get_label_of_element(element))

        # Extract and append the order type and symbol name to the result
        label_order_type = get_label_of_element(order_type_element)
        result.append(label_order_type)

        label_symbol_name = get_label_of_element(symbol_name_element)
        result.append(label_symbol_name)
        
        # If the trade type is "edit", attempt to extract the order number from the confirmation modal
        if trade_type == "edit":

            # Locate the order number element and extract its value if available
            order_number_elements = find_element_by_testid(driver, data_testid=f"edit-confirmation-order-id")
            extracted_orderID = get_label_of_element(order_number_elements)

            # If the order number element exists, process it
            if order_number_elements:
                order_number = re.search(r'\d+', extracted_orderID).group() # Extract numerical order ID
                result.append(order_number) # Append the order number to the result list
                
                # Add "Order No." header to trade_confirmation_headers if order number exists
                trade_confirmation_headers.append("Order No.")

        # Create a DataFrame with the extracted trade details
        trade_order_details = pd.DataFrame([result], columns=trade_confirmation_headers)
        trade_order_details['Section'] = "Trade Confirmation Details"  # Add section label for clarity
        
        # Transpose the DataFrame for better readability and fill missing values with "-"
        overall = tabulate(trade_order_details.set_index('Section').T.fillna('-'), headers='keys', tablefmt='grid', stralign='center')
        attach_text(overall, name="Trade Confirmation Details") # Attach the formatted grid as text in the report

        # Locate and click the confirmation button to finalize the trade confirmation
        button_confirmation = find_element_by_testid(driver, data_testid=f"{trade_type}-confirmation-button-confirm")
        click_element(button_confirmation)

        # Return the DataFrame containing the trade order details
        return trade_order_details

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""