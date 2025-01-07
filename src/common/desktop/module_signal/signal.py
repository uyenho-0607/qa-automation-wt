import random
import pandas as pd

from tabulate import tabulate
from selenium.webdriver.common.by import By

from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, spinner_element, visibility_of_element_by_testid, visibility_of_element_by_xpath, get_label_of_element
from constants.helper.screenshot import attach_text

from common.desktop.module_trade.order_placing_window.utils import input_size_volume, button_trade_action
from common.desktop.module_subMenu.utils import menu_button
from common.desktop.module_chart.utils import get_chart_symbol_name




"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SKIP CLOSED LOSS STATUS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def skip_closed_loss_and_click(driver):
    """
    Skips the rows with the status 'Closed Loss' in the Signal table and clicks on the first row 
    with a different status. This is used to automate the selection of a valid trade signal.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        
        # Navigate to the 'Signal' menu using a helper function
        menu_button(driver, menu="signal")
        
        # Wait for any spinner element to disappear
        spinner_element(driver)
        
        # Wait for the signal list table to load
        tbody = visibility_of_element_by_xpath(driver, "//tbody[@class='sc-18g2plp-7 iyflGe']")
        
        # Get all rows in the table
        rows = tbody.find_elements(By.XPATH, ".//tr")

        # Loop through the rows and find a row that doesn't have the status 'Closed Loss'
        for row in rows:
            # Find the status column for the current row
            row_status = row.find_element(By.XPATH, ".//td[@class='sc-18g2plp-8 hbmUBA']//span")
            label_status = get_label_of_element(row_status)
            
            # If the status is not 'Closed Loss', click the row and exit the loop
            if "Closed Loss" not in label_status:
                row.click()
                break

    except Exception as e:
        # Handle any exceptions that occur during the execution
        print("Error occurred while skipping 'Closed Loss' rows and clicking.")
        handle_exception(driver, e)


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
        # Skip closed losses and proceed
        skip_closed_loss_and_click(driver)
        
        delay(0.5)

        # Lists to store extracted labels and corresponding headers
        copyTrade_elements = []
        copyTrade_headers = []
        
        # Define two possible options for selecting trade details
        options = [
            {
                "button_xpath": "(//button[contains(normalize-space(text()), 'Copy to order')])[1]",
                "take_profit_xpath": "(//div[normalize-space(@class)='sc-hm0akf-9 lnouFc'])[1]"
            },
            {
                "button_xpath": "(//button[contains(normalize-space(text()), 'Copy to order')])[2]",
                "take_profit_xpath": "(//div[normalize-space(@class)='sc-hm0akf-9 lnouFc'])[2]"
            }
        ]
        
        # Randomly select one of the defined options
        selected_option = random.choice(options)
        
        # Find and click the 'Copy to order' button using the selected option
        btn_copyTrade = visibility_of_element_by_xpath(driver, selected_option["button_xpath"])
        click_element(btn_copyTrade)
        
        # Extract the trade symbol and add to the report
        chart_symbol_name = get_chart_symbol_name(driver)
        copyTrade_elements.append(chart_symbol_name)
        copyTrade_headers.append("Symbol")
        
        # Extract the order status and determine which details to fetch
        orderStatus = visibility_of_element_by_xpath(driver, "(//div[@class='sc-1r2b698-4 iBdecC']/span)[2]")
        label_OrderStatus = get_label_of_element(orderStatus).upper()

        # Determine the XPath for orderDetails based on order status
        if label_OrderStatus == "LIVE MARKET":
            # Use first element if order status is "Live Market"
            orderDetails_xpath = "(//div[@class='sc-1r2b698-4 iBdecC']/span)[1]"
        else:
            # Use second element if order status is not "Live Market"
            orderDetails_xpath = "(//div[@class='sc-1r2b698-4 iBdecC']/span)[2]"

        # Extract order details based on the determined XPath
        orderDetails = visibility_of_element_by_xpath(driver, orderDetails_xpath)
        label_OrderStatus = get_label_of_element(orderDetails).upper()

        # Append the extracted value to the appropriate lists
        copyTrade_elements.append(label_OrderStatus)
        copyTrade_headers.append("Type")

        # Extract and append Entry Price
        entryPrice = visibility_of_element_by_xpath(driver, "(//div[@class='sc-hm0akf-4 liWewR'])[2]")
        label_entryPrice = get_label_of_element(entryPrice)
        copyTrade_elements.append(label_entryPrice)
        copyTrade_headers.append("Entry Price")

        # Extract and append Stop Loss
        stopLoss = visibility_of_element_by_xpath(driver, "(//div[@class='sc-hm0akf-4 liWewR'])[3]")
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
        
        # Input the trade volume
        input_size_volume(driver)
        
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