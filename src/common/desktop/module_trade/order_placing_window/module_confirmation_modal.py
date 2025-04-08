import re
import pandas as pd

from tabulate import tabulate

from enums.main import ButtonModuleType, SectionName
from constants.element_ids import DataTestID

from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, find_element_by_testid, find_list_of_elements_by_testid, find_visible_element_by_testid, get_label_of_element


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - TRADE CONFIRMATION DIALOG DETAILS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def trade_orders_confirmation_details(driver, trade_type: ButtonModuleType):
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
        
        # Initialize an empty list to store extracted values
        result = []
        
        # Determine the data-testid based on the button type
        button_testids = {
            ButtonModuleType.TRADE: DataTestID.TRADE_CONFIRMATION_MODAL,
            ButtonModuleType.EDIT: DataTestID.EDIT_CONFIRMATION_MODAL,
        }
        
        button_testid = button_testids.get(trade_type)
        
        # Ensure the trade confirmation modal is visible before proceeding
        find_visible_element_by_testid(driver, data_testid=button_testid)

        # Define trade type mappings
        trade_type_mappings = {
            "header_label": {
                ButtonModuleType.TRADE: DataTestID.TRADE_CONFIRMATION_LABEL,
                ButtonModuleType.EDIT: DataTestID.EDIT_CONFIRMATION_LABEL,
            },
            "confirmation_type": {
                ButtonModuleType.TRADE: DataTestID.TRADE_CONFIRMATION_ORDER_TYPE,
                ButtonModuleType.EDIT: DataTestID.EDIT_CONFIRMATION_ORDER_TYPE,
            },
            "symbol_name": {
                ButtonModuleType.TRADE: DataTestID.TRADE_CONFIRMATION_SYMBOL,
                ButtonModuleType.EDIT: DataTestID.EDIT_CONFIRMATION_SYMBOL,
            },
            "confirmation_value": {
                ButtonModuleType.TRADE: DataTestID.TRADE_CONFIRMATION_VALUE,
                ButtonModuleType.EDIT: DataTestID.EDIT_CONFIRMATION_VALUE,
            },
            "confirm_button":{
                ButtonModuleType.TRADE: DataTestID.TRADE_CONFIRMATION_BUTTON_CONFIRM,
                ButtonModuleType.EDIT: DataTestID.EDIT_CONFIRMATION_BUTTON_CONFIRM,
            }
        }
        
        header_title = trade_type_mappings["header_label"][trade_type]
        button_confirmation = trade_type_mappings["confirmation_type"][trade_type]
        symbol_name_label = trade_type_mappings["symbol_name"][trade_type]
        confirmation_value_data = trade_type_mappings["confirmation_value"][trade_type]
        btn_confirm = trade_type_mappings["confirm_button"][trade_type]
        
        # Retrieve headers for trade confirmation
        trade_order_header_elements = find_list_of_elements_by_testid(driver, header_title)
        trade_confirmation_headers = [get_label_of_element(header) if get_label_of_element(header) != "Price" else "Entry Price" for header in trade_order_header_elements]
        
        # Retrieve and append order type
        order_type_element = find_element_by_testid(driver, button_confirmation)
        trade_confirmation_headers.append("Type")

        # Retrieve and append symbol name
        symbol_name_element = find_element_by_testid(driver, symbol_name_label)
        trade_confirmation_headers.append("Symbol")        
        
        # Retrieve confirmation values
        elements = find_list_of_elements_by_testid(driver, confirmation_value_data)
        result.extend(get_label_of_element(element) for element in elements)

        # Extract and append the order type and symbol name to the result
        result.append(get_label_of_element(order_type_element))  # Order Type
        result.append(get_label_of_element(symbol_name_element))  # Symbol Name
        
        
        # If the trade type is "edit", attempt to extract the order number from the confirmation modal
        if trade_type == ButtonModuleType.EDIT:
            # Locate the order number element and extract its value if available
            order_number_elements = find_element_by_testid(driver, data_testid=DataTestID.EDIT_CONFIRMATION_ORDER_ID)
            extracted_orderID = get_label_of_element(order_number_elements)

            # If the order number element exists, process it
            extracted_order_id = re.search(r'\d+', extracted_orderID).group() # Extract numerical order ID
            
            # Append the order number to the result list
            result.append(extracted_order_id)
            
            # Add "Order No." header to trade_confirmation_headers if order number exists
            trade_confirmation_headers.append("Order No.")

        # Create a DataFrame with the extracted trade details
        trade_order_details = pd.DataFrame([result], columns=trade_confirmation_headers)
        trade_order_details['Section'] = SectionName.TRADE_CONFIRMATION_DETAILS  # Add section label for clarity
        
        # Transpose the DataFrame for better readability and fill missing values with "-"
        overall = tabulate(trade_order_details.set_index('Section').T.fillna('-'), headers='keys', tablefmt='grid', stralign='center')
        attach_text(overall, name=SectionName.TRADE_CONFIRMATION_DETAILS) # Attach the formatted grid as text in the report
        
        confirm_button = find_element_by_testid(driver, data_testid=btn_confirm)
        click_element(element=confirm_button)

        # Return the DataFrame containing the trade order details
        return trade_order_details

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""