import random
import pytest
import pandas as pd

from tabulate import tabulate
from selenium.webdriver.common.by import By

from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, spinner_element, is_element_present_by_xpath, find_element_by_xpath, find_element_by_testid, visibility_of_element_by_xpath, visibility_of_element_by_testid, invisibility_of_element_by_testid, get_label_of_element, wait_for_text_to_be_present_in_element_by_xpath, is_element_disabled_by_cursor, populate_element
from constants.helper.screenshot import attach_text

from common.desktop.module_subMenu.utils import menu_button
from common.desktop.module_chart.utils import get_chart_symbol_name
from common.desktop.module_trade.order_placing_window.utils import input_size_volume, button_trade_action




"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CLOSED FLAT / CLOSED LOSS / CLOSED PROFIT - COPY TO ORDER BUTTON DISABLED
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def signal_search_feature(driver, input_search: str):
    try:
        
        # Navigate to the 'Signal' menu using a helper function
        menu_button(driver, menu="signal")
        
        # Wait for any spinner element to disappear
        spinner_element(driver)
        
        input_signal_search = find_element_by_xpath(driver, "//div[@class='sc-1mh8ki8-0 bvKpbO']//input")
        populate_element(element=input_signal_search, text=input_search)
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
    
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                EXPRESS INTEREST
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def express_interest(driver, click_submit: bool = True):
    try:

        # Navigate to the 'Signal' menu using a helper function
        menu_button(driver, menu="signal")
        
        # Wait for any spinner element to disappear
        spinner_element(driver)
        
        wait_for_text_to_be_present_in_element_by_xpath(driver, "//div[@class='sc-1ovmeyf-2 yQpTC']", text="Curious about additional trade signals?")
        
        btn_express_interest = find_element_by_xpath(driver, "//button[normalize-space(text())='Express interest']")
        click_element(element=btn_express_interest)
        
        wait_for_text_to_be_present_in_element_by_xpath(driver, "//div[@class='sc-1mpscps-2 iUoyTa']", text="Express Your Interest")
        content = get_label_of_element(element=find_element_by_xpath(driver, "(//div[@data-testid='confirmation-modal']//div)[4]")).strip()
        if content != "Let us know if you're interested in more trade analysis and plans. Your input helps us prioritise features that matter to you!":
            raise AssertionError("Content does not match the expected result")
        
        if click_submit:
            btn_submit = find_element_by_xpath(driver, "//button[normalize-space(text())='Submit']")
            click_element(element=btn_submit)
            
            # Wait for snackbar message and extract header & description
            visibility_of_element_by_testid(driver, "notification-box")
            message_header = visibility_of_element_by_testid(driver, "notification-title")
            extracted_header = get_label_of_element(message_header)
        
            # Validate message header
            if extracted_header != "Your interest has been submitted":
                raise AssertionError(f"Invalid message header: {extracted_header}")
            
            result = invisibility_of_element_by_testid(driver, data_testid="confirmation-modal")
            if not result:
                raise AssertionError("Confirmation dialog should not be visible")
        else:
            btn_cancel = find_element_by_xpath(driver, "//button[normalize-space(text())='Cancel']")
            click_element(element=btn_cancel)
            
            result = invisibility_of_element_by_testid(driver, data_testid="confirmation-modal")
            if not result:
                raise AssertionError("Confirmation dialog should not be visible")
            
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CLOSED FLAT / CLOSED LOSS / CLOSED PROFIT - COPY TO ORDER BUTTON DISABLED
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def verify_copy_to_order_is_disabled(driver):
    try:
        # Navigate to the 'Signal' menu using a helper function
        menu_button(driver, menu="signal")
        
        # Wait for any spinner element to disappear
        spinner_element(driver)
        
        delay(2)
        
        # Wait for the signal list table to load
        tbody = visibility_of_element_by_testid(driver, data_testid="signal-list")
        
        # Get all rows in the table
        rows = tbody.find_elements(By.XPATH, ".//tr")

        found_valid_status = False  # Flag to check if any valid status is found

        # Loop through the rows to find a valid tradable symbol
        for row in rows:
            row_status = row.find_element(By.XPATH, ".//span[@data-testid='signal-row-order-status']")
            label_status = get_label_of_element(row_status)
            print(f"Checking row with status: {label_status}")
            
            if label_status in ["Closed Flat", "Closed Loss", "Closed Profit"]:
                print(f"'{label_status}' status found.")
                found_valid_status = True  # Set flag to True
                click_element(element=row)        
                break
        
        # If no valid status is found, mark the test as skipped
        if not found_valid_status:
            pytest.skip("Skipping test as no 'Closed Flat', 'Closed Loss', or 'Closed Profit' status was found.")
        
        delay(1)
    
        # Verify 'Copy to Order' buttons are disabled
        for i in range(1, 3):
            btn_copy_trade = visibility_of_element_by_testid(driver, data_testid=f"copy-to-order-{i}")
            is_disabled = is_element_disabled_by_cursor(driver, element=btn_copy_trade)
            print(f"\nCopy To Order Button {i} is Disabled: {is_disabled}")
            assert is_disabled, f"Expected 'Copy To Order {i}' button to be disabled"
        
    except Exception as e:
        handle_exception(driver, e)


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

    
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SKIP CLOSED LOSS STATUS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def select_valid_signal_to_trade(driver):
    """
    Skips the rows with the status 'Closed Loss' in the Signal table and clicks on the first row 
    with a different status that does not display the view-only message. This automates the selection of a valid trade signal.
    
    Selects the first available trade signal that is not in a 'Closed' state and does not display a 'This symbol is for view only.' or 'Market Closed' message.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Navigate to the 'Signal' menu using a helper function
        menu_button(driver, menu="signal")
        
        # Wait for any spinner element to disappear
        spinner_element(driver)
        
        delay(2)
        
        # Wait for the signal list table to load
        tbody = visibility_of_element_by_testid(driver, data_testid="signal-list")
        
        # Get all rows in the table
        rows = tbody.find_elements(By.XPATH, ".//tr")

        valid_row_found = False  # Flag to track if we find a tradable row

        # Loop through the rows to find a valid tradable symbol
        for row in rows:
            # Find the status column for the current row
            row_status = row.find_element(By.XPATH, ".//span[@data-testid='signal-row-order-status']")
            label_status = get_label_of_element(row_status)
            print(f"Checking row with status: {label_status}")
            
            # Skip rows with 'Closed Loss' status
            if label_status in ["Closed Flat", "Closed Loss", "Closed Profit"]:
                print(f"Skipping '{label_status}' row.")
                continue
            
            # Click the row as it is not 'Closed Loss'
            row.click()
            print("Clicked on the row. Checking for view-only message...")
            
            delay(1)
            
            # Check for 'View Only' or 'Market Closed' statuses
            if is_element_present_by_xpath(driver, "//div[@class='sc-xc0b2i-1 XQXKK']"):
                print("Symbol is for view only, selecting another...")
                continue  # Skip to the next row
            elif find_element_by_testid(driver, data_testid="trade-button-order").text == "Market Closed":
                print("Symbol is Market Closed, selecting another...")
                continue  # Skip to the next row
            else:
                # If no view-only message, the symbol is tradable
                print("Tradable symbol found!")
                valid_row_found = True
                break  # Exit the loop once a valid symbol is selected
        
        # If no valid row was found, handle the case
        if not valid_row_found:
            assert False, "No valid tradable signal found."
            # Handle this case as needed, e.g., logging, raising an exception, etc.

    except Exception as e:
        # Handle any exceptions that occur during the execution
        print("Error occurred while skipping 'Closed Loss' rows and clicking.")
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                COPY TO TRADE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_copyTrade(driver):
    """
    Automates the process of copying trade details from a web platform, extracts relevant trade information, 
    and executes the trade action. A table is generated with the extracted details.

    Returns:
    - copyTrade_details (DataFrame): A DataFrame containing extracted trade details.
    - label_OrderStatus (str): The order status (e.g., 'Live Market' or 'Other').
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Skip closed loss and proceed
        select_valid_signal_to_trade(driver)
        
        delay(0.5)
        
        # Input the trade volume
        input_size_volume(driver)

        # Lists to store extracted labels and corresponding headers
        copyTrade_elements = []
        copyTrade_headers = []
        
        # Define two possible options for selecting trade details
        options = [
            {
                "button_xpath": "copy-to-order-1",
                "take_profit_xpath": "(//div[@data-testid='analysis-action-value'])[4]"
            },
            {
                "button_xpath": "copy-to-order-2",
                "take_profit_xpath": "(//div[@data-testid='analysis-action-value'])[5]"
            }
        ]
        
        # Randomly select one of the defined options
        selected_option = random.choice(options)
        
        # Find and click the 'Copy to order' button using the selected option
        btn_copyTrade = visibility_of_element_by_testid(driver, data_testid=selected_option["button_xpath"])
        click_element(btn_copyTrade)
        
        # Extract the trade symbol and add to the report
        chart_symbol_name = get_chart_symbol_name(driver)
        copyTrade_elements.append(chart_symbol_name)
        copyTrade_headers.append("Symbol")
        
        # Extract the order status and determine which details to fetch
        orderStatus = visibility_of_element_by_xpath(driver, "(//span[@data-testid='analysis-description-value'])[2]")
        label_OrderStatus = get_label_of_element(orderStatus).upper()

        # Determine the XPath for orderDetails based on order status
        if label_OrderStatus == "LIVE MARKET":
            # Use first element if order status is "Live Market"
            orderDetails_xpath = "(//span[@data-testid='analysis-description-value'])[1]"
        else:
            # Use second element if order status is not "Live Market"
            orderDetails_xpath = "(//span[@data-testid='analysis-description-value'])[2]"

        # Extract order details based on the determined XPath
        orderDetails = visibility_of_element_by_xpath(driver, orderDetails_xpath)
        label_OrderStatus = get_label_of_element(orderDetails).upper()

        # Append the extracted value to the appropriate lists
        copyTrade_elements.append(label_OrderStatus)
        copyTrade_headers.append("Type")

        # Extract and append Entry Price
        entryPrice = visibility_of_element_by_xpath(driver, "(//div[@data-testid='analysis-action-value'])[2]")
        label_entryPrice = get_label_of_element(entryPrice)
        copyTrade_elements.append(label_entryPrice)
        copyTrade_headers.append("Entry Price")

        # Extract and append Stop Loss
        stopLoss = visibility_of_element_by_xpath(driver, "(//div[@data-testid='analysis-action-value'])[3]")
        label_stopLoss = get_label_of_element(stopLoss)
        copyTrade_elements.append(label_stopLoss)
        copyTrade_headers.append("Stop Loss")

        # Extract the 'Take Profit' label using the take_profit_xpath of the selected option
        takeProfit = visibility_of_element_by_xpath(driver, selected_option["take_profit_xpath"])
        label_takeProfit = get_label_of_element(takeProfit)
        copyTrade_elements.append(label_takeProfit)
        copyTrade_headers.append("Take Profit")

        # Create a DataFrame with the extracted copy trade details
        copyTrade_details = pd.DataFrame([copyTrade_elements], columns=copyTrade_headers)
        copyTrade_details['Section'] = "Copy Trade Details"

        # Transpose the DataFrame for better readability and format it using tabulate
        overall = tabulate(copyTrade_details.set_index('Section').T.fillna('-'), headers='keys', tablefmt='grid', stralign='center')
        # Attach the formatted table to the report for documentation purposes
        attach_text(overall, name="Copy Trade Details")
        
        # Perform the trade action (e.g., 'trade')
        button_trade_action(driver, trade_type="trade")
        
        # Return the transposed DataFrame containing trade details
        return copyTrade_details, label_OrderStatus
    
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                HANDLE ORDER TYPE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Function to handle order type and click the appropriate tab
def handle_order_type(driver, order_type: str):
    """
    Navigates to the appropriate tab based on the given order type and returns the tab name.

    This function classifies order types into two categories:
    - Pending orders (e.g., "BUY LIMIT", "SELL LIMIT")
    - Open positions (e.g., "BUY", "SELL")
    
    The function clicks on the correct tab and returns the tab name for further processing.

    Arguments:
    - order_type: The type of the order (e.g., 'BUY', 'BUY LIMIT' etc).

    Returns:
    - tab (str): The name of the clicked tab ('open-positions' or 'pending-orders').
    - title (str): The title of the tab (human-readable form).
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        
        # Define order type categories
        pending_order_types = [
            "BUY LIMIT", "SELL LIMIT",
            "BUY STOP", "SELL STOP",
            "BUY STOP LIMIT", "SELL STOP LIMIT"
        ]

        open_positions_types = ["BUY", "SELL"]

        # Navigate to assets menu
        menu_button(driver, menu="assets")

        # Determine tab based on order type
        order_tabs = {
            "pending-orders": pending_order_types,
            "open-positions": open_positions_types
        }

        # Determine the correct tab to click based on the order type
        for tab, order_list in order_tabs.items():
            if order_type in order_list:
                # Click on the appropriate tab for the given order type
                visibility_of_element_by_testid(driver, data_testid=f"tab-asset-order-type-{tab}")
                print(f"Clicked on the {tab.replace('-', ' ').title()} tab for order type: {order_type}")
                return tab, tab.replace('-', ' ').title()

    except Exception as e:
        print(f"Unrecognized order type: {order_type}")
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""