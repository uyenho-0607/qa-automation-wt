import re

from tabulate import tabulate

from constants.helper.driver import delay
from enums.main import SectionName
from constants.element_ids import DataTestID

from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element_android_app import click_element, find_element_by_testid_with_wait, find_list_of_elements_by_xpath, get_label_of_element, find_element_by_testid, find_list_of_elements_by_testid, find_visible_element_by_testid, spinner_element

from common.mobileapp.module_notification.noti_general import notification_bell
from common.mobileapp.module_trade.order_panel.op_general import extract_order_data_details, get_table_headers



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NOTIFICATION - RETRIEVE THE ORDER MESSAGE CONTENT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_order_notification_msg(driver, order_id, noti_bell: bool):
    try:
        
        if noti_bell:
            # Click on the notification bell
            notification_bell(driver)

        # Ensure the element is visible
        find_element_by_testid_with_wait(driver, data_testid=DataTestID.NOTIFICATION_LIST_RESULT_ITEM)
        
        noti_messages = find_list_of_elements_by_testid(driver, data_testid=DataTestID.NOTIFICATION_LIST_RESULT_ITEM)
        
        # Extract data using regular expressions
        order_data = [] 
        
        for msg in noti_messages:
            message = get_label_of_element(element=msg)
            print(message)
            if order_id in message:
                attach_text(message, name="Order Notification Message")

                # Order No.
                order_data.append(re.search(r"#(\d+)", message).group(1))

                # Symbol
                symbol_match = re.search(r"\b[A-Z]+\d*(?:\.[A-Za-z]+)?\b", message)
                order_data.append(symbol_match.group())
                
                # Size or Volume
                size_or_volume_match = re.search(r"(Size|Volume) (\d+(\.\d+)?)", message)
                if size_or_volume_match:
                    size_or_volume_label = size_or_volume_match.group(1) # label
                    
                    value = float(size_or_volume_match.group(2)) # value as float
                    size_or_volume_value = "{:.2f}".format(value).rstrip('0').rstrip('.') # Format value as desired
                    order_data.append(size_or_volume_value)
                    
                # Extract the Units
                order_data.append(re.search(r"Units ([\d,]+(?:\.\d+)?)", message).group(1))
                
                # Extract the Entry / Close Price
                order_data.append(re.search(r"@ ([\d,]+(?:\.\d+)?)", message).group(1))

                # Create DataFrame and return
                headers = ["Order No.", "Symbol", size_or_volume_label, "Units"]
    
                # Close price and Profit/Loss (optional)
                pnl_header_present = "of" in message
                if pnl_header_present:
                    headers.append("Close Price")
                    # pnl_match = re.search(r"of\s([+-]?[\d.]+)", message)
                    pnl_match = re.search(r"of\s([+-]?[0-9,]+\.?\d*)", message)                  
                    order_data.append(pnl_match.group(1)) #if pnl_match else None)
                    headers.append("Profit/Loss")

                else:
                    headers.append("Entry Price")
                
                # Create a DataFrame using the data
                order_Notification_Message = extract_order_data_details(driver, order_data, headers, section_name=SectionName.NOTIFICATION_ORDER_MESSAGE)

                master_df_transposed = order_Notification_Message.set_index('Section').T.fillna('-')
                overall = tabulate(master_df_transposed, headers='keys', tablefmt='grid', stralign='center')
                attach_text(overall, name=SectionName.NOTIFICATION_ORDER_MESSAGE)

                # Click on the matching notification message
                click_element(msg)
                
                return order_Notification_Message 
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NOTIFICATION - RETRIEVE THE NOTIFICATION ORDER DETAILS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_notification_order_details_msg(driver):

    # Define header mapping outside the method for better performance
    header_mapping = {
        "Open Date": "Order Time",
        "Order Time": "Open Date",
        "Close Date": "Close Time",
        "Close Time": "Close Date",
    }

    result = []

    try:
        
        spinner_element(driver)
        
        delay(1)

        # To retrieve the text of each element in the list,
        # iterate through the list and access the text attribute for each element individually.
        noti_order_headers = get_table_headers(driver)

        # Map equivalent headers to a common name
        for i in range(len(noti_order_headers)):
            if noti_order_headers[i] in header_mapping:
                noti_order_headers[i] = header_mapping[noti_order_headers[i]]

        elements = find_list_of_elements_by_xpath(driver, DataTestID.APP_NOTIFICATION_ORDER_DETAILS_VALUE)
        
        for element in elements:
            # Extract the text from the element
            result.append(get_label_of_element(element=element).replace("$", "").strip())

        # Extract the Buy or Sell text 
        order_type = find_visible_element_by_testid(driver, data_testid=DataTestID.NOTIFICATION_ORDER_DETAILS_MODAL_ORDDER_TYPE)
        type = get_label_of_element(element=order_type)

        order_type_result = re.search(r'\b(BUY|SELL)\b', type).group()
        result.append(order_type_result)
        noti_order_headers.append("Type")
        
        # Create a DataFrame using the data
        noti_order_details = extract_order_data_details(driver, result, noti_order_headers, section_name=SectionName.NOTIFICATION_ORDER_DETAIL)

        master_df_transposed = noti_order_details.set_index('Section').T.fillna('-')
        overall = tabulate(master_df_transposed, headers='keys', tablefmt='grid', stralign='center')
        attach_text(overall, name=SectionName.NOTIFICATION_ORDER_DETAIL)

        modal_close = find_element_by_testid(driver, data_testid=DataTestID.APP_NAVIGATION_BACK_BUTTON)
        click_element(modal_close)

        return noti_order_details

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NOTIFICATIONS - PROCESS ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def process_order_notifications(driver, order_ids, noti_bell: bool = True):
    try:
        
        notification_msgs_list = []  # List to store notification messages dataframes
        order_details_list = []  # List to store order details dataframes

        # Check if order_ids is a list
        if isinstance(order_ids, list):
            order_ids = dict(enumerate(order_ids)) # Convert list to dictionary with indices as keys

        # Handle multiple order IDs
        for order_id in order_ids.values():
            noti_msg = get_order_notification_msg(driver, order_id, noti_bell)
            notification_msgs_list.append(noti_msg)

            order_details = get_notification_order_details_msg(driver)
            order_details_list.append(order_details)

        return notification_msgs_list, order_details_list

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)