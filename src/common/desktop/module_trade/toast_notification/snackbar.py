import re
import pandas as pd

from tabulate import tabulate

from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element import get_label_of_element, visibility_of_element_by_testid, find_element_by_testid


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                EXTRACT THE TRADE / EDIT / CLOSE SNACKBAR MESSAGE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_trade_snackbar_banner(driver):
    """
    Extracts the snackbar trade notification message, processes its content, and returns a structured DataFrame with order details.

    Returns: 
    - pd.DataFrame: A DataFrame containing the extracted trade details from the snackbar banner.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
            
        valid_message_headers = [
            "Market Order Submitted",
            "Limit Order Submitted",
            "Stop Order Submitted",
            "Stop Limit Order Submitted",
            "Market Order Updated",
            "Limit Order Updated",
            "Stop Order Updated",
            "Stop Limit Order Updated",
            "Close Order",
            "Delete Order"
        ]

        # Wait for the snackbar message to be visible
        visibility_of_element_by_testid(driver, data_testid="notification-box")
        
        # Wait for the message header to be visible and extract it
        message_header = visibility_of_element_by_testid(driver, data_testid="notification-title")
        extracted_header = get_label_of_element(message_header)

        # Extract the message description
        label_message_description = find_element_by_testid(driver, data_testid="notification-description")
        label_message = get_label_of_element(label_message_description)
        attach_text(label_message, name="Description_Message")

        # Check if the header is valid
        if extracted_header not in valid_message_headers:
            raise AssertionError(f"Invalid message header: {extracted_header}, Message description: {label_message}")
        
        # Initialize a list to hold parts of the snackbar message
        snackbar_msg = []
        success_message_headers = ["Symbol", "Type"]
        
        # Extract Symbol Name
        symbol_match = re.search(r"\b[A-Za-z0-9.]+\b", label_message)
        if symbol_match:
            snackbar_msg.append(symbol_match.group())
        
        # Extarct order type (e.g. Buy / Sell - LIMIT / STOP / STOP LIMIT)
        order_match = re.search(r"(Buy|Sell)(?:\s(Limit|Stop(?: Limit)?)?)", label_message, re.IGNORECASE)
        if order_match:
            order_type = order_match.group(0).strip() # Remove leading/trailing spaces
            snackbar_msg.append(order_type)

        # Regular expression to match either 'Size' or 'Volume' followed by a number
        size_or_volume_match = re.search(r"(Size|Volume): (\d+(\.\d+)?)", label_message)
        if size_or_volume_match:
            label = size_or_volume_match.group(1) # This captures 'Size' or 'Volume'
            value = size_or_volume_match.group(2) # This captures the number
            snackbar_msg.append(value)
            success_message_headers.append(label)

        # Extract Units
        unit_match = re.search(r"Units:\s*([\d,]+(?:\.\d+)?)", label_message)
        if unit_match:
            snackbar_msg.append(unit_match.group(1))
            success_message_headers.append("Units")

        # Extract the Entry Price
        price_match = re.findall(r'Price:\s([\d,]+\.\d+)', label_message)
        if price_match:
            snackbar_msg.append(price_match[-1]) # Get the last occurrence
            success_message_headers.append("Entry Price")
            
        # Extract the Stop Limit Price
        stop_limit_price_match = re.search(r'Stop Limit Price: ([\d,]+\.\d+)', label_message)
        if stop_limit_price_match:
            snackbar_msg.append(stop_limit_price_match.group(1))
            success_message_headers.append("Stop Limit Price")
            
        # Extract Stop Loss
        stop_loss_match = re.search(r"Stop Loss:\s([\d,]+(\.\d+)?)", label_message)
        if stop_loss_match:
            snackbar_msg.append(stop_loss_match.group(1))
            success_message_headers.append("Stop Loss")

        # Extract Take Profit
        take_profit_match = re.search(r"Take Profit:\s([\d,]+(\.\d+)?)", label_message)
        if take_profit_match:
            snackbar_msg.append(take_profit_match.group(1))
            success_message_headers.append("Take Profit")

        closeBtn = find_element_by_testid(driver, data_testid="notification-close-button")
        driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', { bubbles: true }));", closeBtn)
        
        # Create a DataFrame with the snackbar message details
        order_notification_message = pd.DataFrame([snackbar_msg], columns=success_message_headers)
        order_notification_message['Section'] = "Snackbar Banner Message"
        overall = tabulate(order_notification_message.set_index('Section').T.fillna('-'), headers='keys', tablefmt='grid', stralign='center')
        attach_text(overall, name="Snackbar Banner Message")

        return order_notification_message  # Return DataFrame

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                EXTRACT THE NEGATIVE SNACKBAR MESSAGE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_neg_snackbar_banner(driver):
    """
    Extracts the snackbar trade notification message, processes its content, and returns a structured DataFrame with order details.

    Returns: 
    - pd.DataFrame: A DataFrame containing the extracted trade details from the snackbar banner.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        
        neg_message_headers = [
            "Invalid order",
            "Order action failed"
        ]
        
        description_messages = [
        "Invalid Stop loss or Take profit", 
        "Invalid Price submitted", 
        # "Trading general error. Please try again later."
        ]

        # Wait for the snackbar message to be visible
        visibility_of_element_by_testid(driver, data_testid="notification-box")
        
        # Wait for the message header to be visible
        message_header = visibility_of_element_by_testid(driver, data_testid="notification-title")
        extracted_header = get_label_of_element(message_header)

        # Check if the normalized header is in the list of valid headers
        if extracted_header in neg_message_headers:
            label_message_description = find_element_by_testid(driver, data_testid="notification-description")
            label_message = get_label_of_element(label_message_description)
            
            if any(msg in label_message for msg in description_messages):
                attach_text(label_message, name="Description_Message")
        else:
            assert False, f"Invalid message header: {extracted_header}" if message_header else "Message header not found"

        closeBtn = find_element_by_testid(driver, data_testid="notification-close-button")
        driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', { bubbles: true }));", closeBtn)
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                EXTRACT THE BULK SNACKBAR MESSAGE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_bulk_snackbar_banner(driver):
    """
    Extracts the snackbar trade notification message, processes its content, and returns a structured DataFrame with order details.

    Returns: 
    - pd.DataFrame: A DataFrame containing the extracted trade details from the snackbar banner.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        valid_message_headers = [
            "Bulk closure of open positions",
            "Bulk deletion of pending orders"
        ]
        
        # Wait for the snackbar message to be visible
        visibility_of_element_by_testid(driver, data_testid="notification-box")
        
        # Wait for the message header to be visible
        message_header = visibility_of_element_by_testid(driver, data_testid="notification-title")
        extracted_header = get_label_of_element(message_header)

        # Extract the message description
        label_message_description = find_element_by_testid(driver, data_testid="notification-description")
        label_message = get_label_of_element(label_message_description)
        attach_text(label_message, name="Description_Message")

        # Check if the header is valid
        if extracted_header not in valid_message_headers:
            raise AssertionError(f"Invalid message header: {extracted_header}, Message description: {label_message}")
    
        closeBtn = find_element_by_testid(driver, data_testid="notification-close-button")
        driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', { bubbles: true }));", closeBtn)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)