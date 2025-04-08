import re

from tabulate import tabulate

from enums.main import ButtonModuleType, SectionName
from constants.element_ids import DataTestID

from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element_android_app import click_element_with_wait, find_element_by_testid, find_list_of_elements_by_testid, find_visible_element_by_xpath, get_label_of_element

from common.mobileapp.module_trade.order_panel.op_general import extract_order_data_details



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - TRADE CONFIRMATION DIALOG DETAILS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def trade_orders_confirmation_details(driver, trade_type: ButtonModuleType):
    try:

        result = []

        # Ensure the confirmation modal is visible
        find_visible_element_by_xpath(driver, DataTestID.APP_TRADE_CONFIRMATION_TITLE)

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

        result.append(get_label_of_element(order_type_element))  # Order Type
        result.append(get_label_of_element(symbol_name_element))  # Symbol Name

        # Handle "edit" trade type and extract order number if available
        order_number_match = None  # Default if not an EDIT type
        if trade_type == ButtonModuleType.EDIT:
            order_number_element = find_element_by_testid(driver, data_testid=DataTestID.EDIT_CONFIRMATION_ORDER_ID)

            extracted_order_id = get_label_of_element(order_number_element)
            # Extract the orderid
            order_number_match = re.search(r'\d+', extracted_order_id).group()
            
            # Append the order number to the result list
            result.append(order_number_match)
            
            # Add the new header for order number only if it exists
            trade_confirmation_headers.append("Order No.")

        # Create a DataFrame
        trade_order_details = extract_order_data_details(driver, result, trade_confirmation_headers, section_name=SectionName.TRADE_CONFIRMATION_DETAILS)

        # Format and attach trade confirmation details
        overall = tabulate(trade_order_details.set_index('Section').T.fillna('-'), headers='keys', tablefmt='grid', stralign='center')
        attach_text(overall, name=SectionName.TRADE_CONFIRMATION_DETAILS)

        # Click on the confirm button
        confirm_button = find_element_by_testid(driver, data_testid=btn_confirm)
        click_element_with_wait(driver, element=confirm_button)

        return trade_order_details, order_number_match

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""