import re
from tabulate import tabulate

from constants.element_ids import DataTestID
from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, find_element_by_testid, find_list_of_elements_by_testid, find_visible_element_by_testid, spinner_element

from common.desktop.module_notification.noti_general import notification_bell
from common.desktop.module_trade.order_panel.op_general import extract_order_data_details



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NOTIFICATION - RETRIEVE THE ORDER MESSAGE CONTENT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_orderNotification_msg(driver, order_id: str):
    """
    Extracts details from the order notification message based on the provided order ID and returns
    the parsed details in a tabular format.

    Arguments:
    - order_id: The order ID to search for in the notification message.

    Returns:
    - DataFrame: A DataFrame containing the order notification details.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        
        # Click on the notification bell to open the notification area
        notification_bell(driver)

        # response = api_get_noti_message(driver)
        
        # if response.status_code == 200:
        
        # Wait until the spinner icon is no longer displayed
        spinner_element(driver)
        
        # Find all notification messages
        noti_messages = find_list_of_elements_by_testid(driver, data_testid=DataTestID.NOTIFICATION_LIST_RESULT_ITEM)

        # Initialize a list to store the parsed order data
        order_data = []
        
        for message in noti_messages:
            # Check if the order ID is present in the notification message
            if order_id in message.text:
                # Attach the message text to the report for documentation purposes
                attach_text(message.text, name="Order Notification Message")

                # Extract Order No. using regular expressions
                order_data.append(re.search(r"#(\d+)", message.text).group(1))

                # Extract Symbol using regex (e.g., "BTCUSD")
                symbol_match = re.search(r"\b[A-Z]+\d*(?:\.[A-Za-z]+)?\b", message.text)
                order_data.append(symbol_match.group())
                
                # Extract Size/Volume using regex
                size_or_volume_match = re.search(r"(Size|Volume) (\d+(\.\d+)?)", message.text)
                if size_or_volume_match:
                    size_or_volume_label = size_or_volume_match.group(1) # label
                    
                    value = float(size_or_volume_match.group(2)) # value as float
                    size_or_volume_value = "{:.2f}".format(value).rstrip('0').rstrip('.') # Format value as desired
                    order_data.append(size_or_volume_value)
                    
                # Extract Units using regular expressions
                order_data.append(re.search(r"Units ([\d,]+(?:\.\d+)?)", message.text).group(1))
                
                # Extract Entry or Close Price using regular expressions
                order_data.append(re.search(r"@ ([\d,]+(?:\.\d+)?)", message.text).group(1))

                # Prepare headers for the DataFrame
                headers = ["Order No.", "Symbol", size_or_volume_label, "Units"]
    
                # Check if Profit/Loss details are available in the message
                pnl_header_present = "of" in message.text
                if pnl_header_present:
                    headers.append("Close Price")
                    # pnl_match = re.search(r"of\s([+-]?[\d.]+)", message.text)
                    pnl_match = re.search(r"of\s([+-]?\d+(?:,\d{3})*(?:\.\d+)?)", message.text)
                    order_data.append(pnl_match.group(1)) #if pnl_match else None)
                    headers.append("Profit/Loss")
                else:
                    headers.append("Entry Price")
                
                # Click on the matching notification message for further actions
                click_element(message)
                
                # Create DataFrame with the extracted data
                order_Notification_Message = extract_order_data_details(driver, [order_data], headers, section_name="Notification Order Message")
                overall = tabulate(order_Notification_Message.set_index('Section').T.fillna('-'), headers='keys', tablefmt='grid', stralign='center')
                # Attach the formatted table to the report
                attach_text(overall, name=f"Notification Order Message - {order_id}")
                
                # Return the DataFrame containing the order notification message
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

def get_noti_ordersDetails(driver):
    """
    Fetches and processes notification order details from the UI, extracts the relevant information, 
    and returns a DataFrame with the extracted data.

    :return: DataFrame with notification order details.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    
    # Define header mapping outside the method for better performance
    header_mapping = {
        "Open Date": "Order Time",
        "Order Time": "Open Date",
        "Close Date": "Close Time",
        "Close Time": "Close Date",
    }

    result = []

    try:
        
        # Wait for the modal dialog to be present
        find_visible_element_by_testid(driver, data_testid=DataTestID.NOTIFICATION_ORDER_DETAILS_MODAL)
        
        # Wait till the spinner icon no longer display
        spinner_element(driver)
        
        # response = api_get_noti_details(driver)
        
        # if response.status_code == 200:
        
        # Retrieve the list of the data
        header_elements = find_list_of_elements_by_testid(driver, data_testid=DataTestID.NOTIFICATION_ORDER_DETAILS_LABEL)
        if not header_elements:
            raise Exception("No notification order headers found.")

        header_labels = [header_mapping.get(element.text, element.text) for element in header_elements]
        header_labels.append("Type") # Append Currency label for deposit handling

        elements = find_list_of_elements_by_testid(driver, data_testid="notification-order-details-value")

        for element in elements:
            # Extract the text from the element
            result.append(element.text)

        # Extract the Buy or Sell text 
        order_type = find_element_by_testid(driver, data_testid=DataTestID.NOTIFICATION_ORDER_DETAILS_MODAL_ORDDER_TYPE)
        result.append(order_type.text)

        # Create a DataFrame using the data
        noti_order_details = extract_order_data_details(driver, [result], header_labels, section_name="Notification Order Details")
        overall = tabulate(noti_order_details.set_index('Section').T.fillna('-'), headers='keys', tablefmt='grid', stralign='center')
        
        # Attach the formatted table to the report
        attach_text(overall, name="Notification Order Details")
        
        # Close the modal dialog
        modal_close = find_element_by_testid(driver, data_testid=DataTestID.NOTIFICATION_ORDER_DETAILS_MODAL_CLOSE)
        click_element(modal_close)

        # Return the DataFrame containing the order notification details
        return noti_order_details

        # else:
        #     assert False, f"Failed to fetch data. Status code: {response.status_code}"

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

def process_order_notifications(driver, orderIDs:str):
    """
    Processes order notifications by extracting notification messages and order details 
    for each order ID in the provided list or dictionary.

    Arguments:
    - orderIDs: (list or dict): A list or dictionary of order IDs to process.

    Returns:
    - notification_msgs_list: A list of DataFrames containing notification message details.
    - order_details_list: A list of DataFrames containing order details associated with the notifications.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    
    try:
        # Initialize lists to store notification messages and order details DataFrames
        notification_msgs_list = []  # List to store notification messages dataframes
        order_details_list = []  # List to store order details dataframes

        # Check if orderIDs is a list and convert to a dictionary if so
        if isinstance(orderIDs, list):
            orderIDs = dict(enumerate(orderIDs))

        # Handle single / multiple orderIDs
        for order_id in orderIDs.values():
            # Retrieve the notification message for the current orderID
            noti_msg = get_orderNotification_msg(driver, order_id)
            notification_msgs_list.append(noti_msg)

            # Retrieve the order details for the current orderID
            order_details = get_noti_ordersDetails(driver)
            order_details_list.append(order_details)

        # Return the lists of notification messages and order details
        return notification_msgs_list, order_details_list

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)