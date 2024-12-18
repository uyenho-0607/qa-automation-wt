import re
import traceback
import pandas as pd

from constants.helper.driver import delay
from constants.helper.screenshot import take_screenshot
from constants.helper.element import click_element, click_element_with_wait, find_element_by_testid, find_list_of_elements_by_testid, visibility_of_element_by_testid, spinner_element


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NOTIFICATION TYPE (TO SELECT THE ORDER / SYSTEM /INFORMATION BUTTON)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def notification_type(driver, notiType):
    try:

        # Find all elements matching the attribute selector
        notifcation_type = find_element_by_testid(driver, data_testid=f"tab-notification-type-{notiType}")
        # click_element_with_wait(driver, element=notifcation_type)
        click_element(notifcation_type)
        
        # take_screenshot(driver, "OrderPanel_Action_Button")

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "notification_type - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

   
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NOTIFICATION - RETRIEVE THE ORDER MESSAGE CONTENT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_orderNotification_msg(driver, order_id):
    try:
        
        # Click on the notification bell
        noti_bell = find_element_by_testid(driver, data_testid="notification-selector")
        click_element_with_wait(driver, element=noti_bell)
        
        # Wait till the spinner icon no longer display
        spinner_element(driver)
        
        # response = api_get_noti_message(driver)
        
        # if response.status_code == 200:
    
        noti_messages = find_list_of_elements_by_testid(driver, data_testid="notification-list-result-item")

        # Extract data using regular expressions
        order_data = [] 
        
        for message in noti_messages:
            if order_id in message.text:
                
                # Order No.
                order_data.append(re.search(r"#(\d+)", message.text).group(1))

                # Symbol
                symbol_match = re.search(r"\b[A-Z]+\d*(?:\.[A-Za-z]+)?\b", message.text)
                order_data.append(symbol_match.group())
                
                # Size or Volume
                size_or_volume_match = re.search(r"(Size|Volume) (\d+(\.\d+)?)", message.text)
                if size_or_volume_match:
                    size_or_volume_label = size_or_volume_match.group(1) # label
                    
                    value = float(size_or_volume_match.group(2)) # value as float
                    size_or_volume_value = "{:.2f}".format(value).rstrip('0').rstrip('.') # Format value as desired
                    order_data.append(size_or_volume_value)
                    
                # Extract the Units
                order_data.append(re.search(r"Units ([\d,]+(?:\.\d+)?)", message.text).group(1))
                
                # Extract the Entry / Close Price
                order_data.append(re.search(r"@ ([\d,]+(?:\.\d+)?)", message.text).group(1))

                # Create DataFrame and return
                headers = ["Order No.", "Symbol", size_or_volume_label, "Units"]
    
                # Close price and Profit/Loss (optional)
                pnl_header_present = "of" in message.text
                if pnl_header_present:
                    headers.append("Close Price")
                    pnl_match = re.search(r"of\s([+-]?[\d.]+)", message.text)
                    order_data.append(pnl_match.group(1)) #if pnl_match else None)
                    headers.append("Profit/Loss")

                else:
                    headers.append("Entry Price")
                
                order_Notification_Message = pd.DataFrame([order_data], columns=headers)
                order_Notification_Message['Section'] = 'Notification Order Message'

                # Click on the matching notification message
                # click_element_with_wait(driver, element=message)
                click_element(message)
                
                delay(10)
                return order_Notification_Message 
        
    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "get_orderNotification_msg - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NOTIFICATION - RETRIEVE THE NOTIFICATION ORDER DETAILS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_noti_ordersDetails(driver):

    # Define header mapping outside the method for better performance
    header_mapping = {
        "Open Date": "Order Time",
        "Order Time": "Open Date",
        "Close Date": "Close Time",
        "Close Time": "Close Date",
    }

    result = []

    try:
        
        # Execute JavaScript to hide the element
        spinner_element(driver)
        
        # response = api_get_noti_details(driver)
        
        # if response.status_code == 200:

        visibility_of_element_by_testid(driver, "notification-order-details-modal")
        
        noti_rows = find_list_of_elements_by_testid(driver, data_testid="notification-order-details-label")

        # To retrieve the text of each element in the list,
        # iterate through the list and access the text attribute for each element individually.
        noti_order_headers = [header.text for header in noti_rows]
        
        noti_order_headers.append("Type")

        # Map equivalent headers to a common name
        for i in range(len(noti_order_headers)):
            if noti_order_headers[i] in header_mapping:
                noti_order_headers[i] = header_mapping[noti_order_headers[i]]

        elements = find_list_of_elements_by_testid(driver, data_testid="notification-order-details-value")

        for element in elements:
            # Extract the text from the element
            result.append(element.text)

        # Extract the Buy or Sell text 
        order_type = find_element_by_testid(driver, data_testid="notification-order-details-modal-order-type")
        result.append(order_type.text)

        # Create a DataFrame using the data
        noti_order_details = pd.DataFrame([result], columns=noti_order_headers)
        noti_order_details['Section'] = 'Notification Order Details'

        modal_close = find_element_by_testid(driver, data_testid="notification-order-details-modal-close")
        click_element_with_wait(driver, element=modal_close)
                
        return noti_order_details

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "get_noti_ordersDetails - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NOTIFICATIONS - PROCESS ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def process_order_notifications(driver, orderIDs):
    try:
            
        notification_msgs_list = []  # List to store notification messages dataframes
        order_details_list = []  # List to store order details dataframes

        # Check if orderIDs is a list
        if isinstance(orderIDs, list):
            orderIDs = dict(enumerate(orderIDs)) # Convert list to dictionary with indices as keys
            print("noti", orderIDs)

        # Handle multiple order IDs
        for order_id in orderIDs.values():
            noti_msg = get_orderNotification_msg(driver, order_id)
            notification_msgs_list.append(noti_msg)

            order_details = get_noti_ordersDetails(driver)
            order_details_list.append(order_details)

        return notification_msgs_list, order_details_list

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "process_order_notifications - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"