import re
from tabulate import tabulate
from dateutil.parser import parse

from selenium.webdriver.common.by import By

from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text
from constants.helper.element import is_element_present_by_xpath, spinner_element, javascript_click, click_element, click_element_with_wait, find_element_by_testid, find_element_by_xpath, find_element_by_xpath_with_wait, is_element_present_by_testid, visibility_of_element_by_xpath, visibility_of_element_by_testid, get_label_of_element

from common.desktop.module_trade.order_panel.op_general import extract_order_data_details, process_individual_orders, get_table_body, get_table_headers
from common.desktop.module_chart.chart import get_chart_symbol_name
from common.desktop.module_assets.account_info import get_server_local_time
from common.desktop.module_setting.setting_general import button_setting
from common.desktop.module_subMenu.sub_menu import menu_button
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ASSET - SYMBOL NAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def asset_symbolName(driver, row_number):
    """
    Verifies that the symbol name in the asset table matches the symbol name in the chart.

    Arguments:
    - row_number: The row number in the asset table to check the symbol name. (e.g. row_number=[1])

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
                
        # Ensure the table body and headers are visible
        get_table_body(driver)
        get_table_headers(driver)

        # Wait till the spinner icon no longer display
        spinner_element(driver)

        # Locate the symbol name from the specified row in the table
        symbol_name = find_element_by_xpath_with_wait(driver, f"(//td[@data-testid='asset-open-column-symbol'])[{row_number}]")

        # Extract the symbol name from the table
        asset_symbolName = get_label_of_element(symbol_name)
        
        # Click on the symbol to view the chart
        click_element_with_wait(driver, element=symbol_name)
        
        # Small delay to ensure the chart loads
        delay(1)

        # Retrieve the symbol name from the chart
        chart_symbolName = get_chart_symbol_name(driver)

        # Check if the symbol name in the table matches the chart symbol name
        if asset_symbolName == chart_symbolName:
            attach_text(asset_symbolName, name="Symbol Name")
            assert True # Assert True if the names match
        else:
            assert False, f"Invalid Symbol Name: {chart_symbolName}. Expected: {asset_symbolName}"

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                COUNT THE LABEL
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Retrieve the total count for order type (Open Position / Pending Order)

def count_orderPanel(driver):
    try:
        def process_tabs(menu_name):
            current_tab = menu_button(driver, menu=menu_name)
            counts = {}  # Dictionary to store counts for each tab
            
            for tab in ["open-positions", "pending-orders"]:
                _, button_name = type_orderPanel(driver, tab_order_type=tab)
                
                # Extract the number using regex
                count = int(re.search(r'\d+', button_name).group())
                counts[tab] = count  # Store the count for the tab
            
            return current_tab, counts  # Return both tab name and counts
        
        # Process "trade" menu
        current_tab, trade_counts = process_tabs("trade")
        if current_tab == "trade":
            print(f"Total counts for 'Trade': {trade_counts}")
            
            # Check if any tab in "trade" exceeds 30 orders
            for tab, count in trade_counts.items():
                if count > 30:
                    assert False, f"Trade - {tab} should not have more than 30 orders (current count: {count})"
        
        # Process "assets" menu
        current_tab, asset_counts = process_tabs("assets")
        if current_tab == "assets":
            # Since no max count is defined for assets, just print or log the counts
            print(f"Total counts for 'Assets': {asset_counts}")

    except Exception as e:
        # Handle any exceptions that occur during execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER PANEL TYPE (OPEN POSITION / PENDING ORDER / ORDER HISTORY)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Choose order type (Open Position / Pending Order / Order History)
def type_orderPanel(driver, tab_order_type, sub_tab=None, position: bool = False):
    """
    Switches between different tabs in the asset order panel.

    Arguments:
    - tab_order_type: The order type tab to select (e.g., 'open-positions', 'pending-orders', 'order-history').
    - sub_tab: The sub-tab to select within the order history section (e.g., 'orders-and-deals'). Default is None.
    - position: If True, it clicks on the position sub-tab within the history section. Default is False.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Introduce a small delay to ensure elements are loaded
        delay(1)
        
        # Locate and click on the main order panel type tab
        orderPanel_type = visibility_of_element_by_testid(driver, data_testid=f"tab-asset-order-type-{tab_order_type}")
        label_count = get_label_of_element(orderPanel_type)
        javascript_click(driver, element=orderPanel_type)
        
        # If position is True, navigate to the position sub-tab within the order history
        if tab_order_type == "history":
            if position:
                # Find and click on the specific sub-tab within the order history section
                # data-testid="tab-asset-order-type-history-positions-history"
                # data_testid="tab-asset-order-type-history-orders-and-deals"
                orderHistory_position = find_element_by_testid(driver, data_testid=f"tab-asset-order-type-history-{sub_tab}")
                click_element(orderHistory_position)
        
        return tab_order_type, label_count
    
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER PANEL BUTTON (TRACK / CLOSE (DELETE) / EDIT)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# order panel - Track / Close (Delete) / Edit button
def button_orderPanel_action(driver, order_action, row_number):
    """
    Performs actions (edit, close, delete) on specified rows in the order panel.

    Arguments:
    - order_action (str): The action to perform on the order (e.g., 'track', 'edit', 'close').
    - row_number (list or int): The row(s) to perform the action on (can be a single row number or a list of row numbers).

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        
        # Ensure row_number is a list, even if a single row number is passed
        # if isinstance(row_number, int):
        #     row_number = [row_number]
                
        # Loop through the provided row numbers to click the action button for each row
        for row in row_number:
            # Find the action button (e.g., edit, close) for the specified row
            action_button = find_element_by_xpath(driver, f"(//div[contains(@data-testid, 'button-{order_action}')])[{row}]")
            click_element(action_button)
        
        delay(0.2)
        
        # Handle order-specific confirmation modals based on the order_action
        match = is_element_present_by_xpath(driver, "//div[contains(@data-testid, 'confirmation-modal')]")
        if match:
            visibility_of_element_by_xpath(driver, "//div[contains(@data-testid, 'confirmation-modal')]")
        
        
        # If delete_button is True, click the delete order button (For OCT)
        if is_element_present_by_testid(driver, data_testid="confirmation-modal-button-submit"):
            delete_button = find_element_by_testid(driver, data_testid="confirmation-modal-button-submit")
            click_element(delete_button)
   
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                RETRIEVE ORDERIDs
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_orderID(driver, row_number):
    """
    Extracts order IDs from the specified rows in the order table.

    Arguments:
    - driver: The Selenium WebDriver instance.
    - row_number (list or int): The row(s) from which the order ID(s) should be extracted.

    Returns:
    - order_ids (list): A list of extracted order IDs from the specified rows.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    
    # Initialize an empty list to hold the data
    order_ids = []
    try:
        
        # Ensure row_number is a list, even if a single row number is passed
        # if isinstance(row_number, int):
        #     row_number = [row_number]
            
        # Locate the table body
        table_body = get_table_body(driver)
        
        # Wait till the spinner icon no longer display
        spinner_element(driver)
        
        # Iterate through specified row numbers
        for row in row_number:
            # Locate the specific table row
            table_row = table_body.find_element(By.XPATH, f".//tr[{row}]")
            
            # Find the order ID element within the row
            order_id_element = table_row.find_element(By.XPATH, ".//*[contains(@data-testid, 'order-id')]")
            
            # Append the extracted order ID to the list
            order_ids.append(order_id_element.text)

        # Attach the order ID to the report for visibility
        attach_text(order_id_element.text, name="orderID")
        
        return order_ids

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                EXTRACT TABLE ORDERs INFO (WITH ORDERIDs PRINT SEPERATELY TABLE)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Extract the order table
def extract_order_info(driver, tab_order_type, section_name, row_number, sub_tab=None, position: bool = False):
    """
    Optimized function to extract order information including order IDs and details.
    """
    
    order_ids = []
    table_row_contents = []

    try:
        # Navigate to tab
        type_orderPanel(driver, tab_order_type, sub_tab, position)
        
        # Wait for spinner once
        spinner_element(driver)

        # Get table body and headers
        table_body = get_table_body(driver)
        thead_data = get_table_headers(driver)

        # Check if Symbol element exists
        chart_symbol_name = get_chart_symbol_name(driver)
        if chart_symbol_name:
            thead_data.append("Symbol")

        # Extract rows efficiently
        for row in row_number:
            table_row = table_body.find_element(By.XPATH, f".//tr[{row}]")
            
            # Extract Order ID
            order_id_element = table_row.find_element(By.XPATH, ".//*[contains(@data-testid, 'order-id')]")
            order_id_text = order_id_element.text.strip()
            order_ids.append(order_id_text)

            # Extract row data
            cells = table_row.find_elements(By.XPATH, ".//th[1] | .//th[2] | .//td")
            row_data = [re.sub(r'\s*/\s*', ' / ', cell.text.strip()) for cell in cells]
            
            # row_data = []
            # for cell in cells:
            #     wait_for_element_visibility(driver, cell)
            #     # row_data.append(cell.text.strip())
            #     text = cell.text.strip()
            #     # Ensure spaces around '/'
            #     normalized_text = re.sub(r'\s*/\s*', ' / ', text)
            #     row_data.append(normalized_text)
            
            # Append symbol if present
            if chart_symbol_name:
                row_data.append(chart_symbol_name)

            table_row_contents.append(row_data)

        # Attach extracted order IDs
        attach_text("\n".join(order_ids), name="orderID")

        # Process data into a DataFrame
        orderPanel_data = extract_order_data_details(driver, table_row_contents, thead_data, section_name)
        overall = tabulate(orderPanel_data.set_index('Section').T.fillna('-'), headers='keys', tablefmt='grid', stralign='center')
        attach_text(overall, name=section_name)

        return order_ids, orderPanel_data

    except Exception as e:
        handle_exception(driver, e)


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER PANNEL NAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Helper function to map order panel data_testid to a descriptive name
def get_order_panel_name(order_panel):
    """
    Maps a given order panel identifier to a human-readable name.

    Arguments:
    - order_panel: The order panel identifier (e.g., "tab-asset-order-type-history").

    Returns:
    - The human-readable name of the order panel. If no mapping is found, returns "Order Panel".
    """
    
    order_panel_names = {
        "history": "Order History / Position",
        "tab-asset-order-type-history-orders-and-deals": "Order History (Order & Deals)",
        "pending-orders": "Pending Orders",
        "open-positions": "Open Positions",
        # Add more mappings as needed
    }
    return order_panel_names.get(order_panel, "Order Panel")

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                REVIEW ORDERIDs FROM CSV
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def review_pending_orderIDs(driver, order_ids, sub_tab=None, position: bool = False):
    """
    Reviews the pending order IDs across the "Open Positions", "Pending Orders", and "Order History" tabs,
    comparing them with the provided order IDs.

    Arguments:
    - order_ids (list): The list of order IDs to check.

    Returns:
    - list: A list of order IDs that were not found in any tab.
    """
    tabs = ["open-positions", "pending-orders", "history"]
    failed_order_ids = order_ids.copy()  # Start with all order IDs as failed
    result_message = ""

    try:
        for tab_order_type in tabs:
            # If no failed order IDs are left, break out of the loop early
            if not failed_order_ids:
                break

            # Click the appropriate tab (if needed)
            menu_button(driver, menu="assets")
            type_orderPanel(driver, tab_order_type, sub_tab, position)

            # Wait for the table body to load and the spinner to disappear
            table_body = get_table_body(driver)
            spinner_element(driver)

            # Get the order IDs displayed in the table
            rows = table_body.find_elements(By.XPATH, ".//tr")
            spinner_element(driver)

            # For each order ID still in the failed list, check if it exists in the table
            for order_id in failed_order_ids[:]:  # Iterate over a copy of the list to allow modification

                # Convert the strings to datetime objects
                # datetime_format = '%Y-%m-%d %H:%M:%S'
                dateTime = get_server_local_time(driver)
                # Automatically parse any valid datetime format
                current_datetime = parse(dateTime)

                # Loop through each row to find a matching order ID
                for row in rows:
                    # spinner_element(driver)
                    order_id_cell = row.find_element(By.XPATH, ".//*[contains(@data-testid, 'order-id')]")
                    if order_id in order_id_cell.text:
                        
                        if tab_order_type == "open-positions":
                            print(f"Switching to Open Position tab, {order_id} found")

                        # Check if we're dealing with the "pending-orders" tab
                        elif tab_order_type == "pending-orders":
                            print("Switching to Pending Order tab")
                            # Extract the 'Expiry' column text from the same row
                            expiry_cell = row.find_element(By.XPATH, ".//td[contains(@data-testid, 'column-expiry')]")
                            expiry_text = expiry_cell.text
                            print(f"Expiry text for Order ID {order_id}: {expiry_text}")
                            
                            # Extract the 'Expiry' column text from the same row
                            expiry_date_cell = row.find_element(By.XPATH, ".//td[contains(@data-testid, 'column-expiry-date')]")
                            # expiry_date_text = expiry_date_cell.text
                            expiry_date = get_label_of_element(element=expiry_date_cell)
                            
                            # Automatically parse any valid datetime format
                            expiry_date_text = parse(expiry_date)

                            print(f"Expiry Date text for Order ID {order_id}: {expiry_date_text}")

                            if expiry_text == "Good Till Cancelled":
                                print(f"Expected to be remain from table {order_id}")
                                result_message += f"Order ID {order_id}: Remains in the table as expected (Good Till Cancelled)\n"
                            elif expiry_text == "Good Till Day":
                                print(f"Expected to be removed from table {order_id}")
                                result_message += f"Order ID {order_id}: Expected to be removed from table (Good Till Day)\n"
                            elif expiry_text == "Specified Date":
                                # Compare the datetime objects
                                if expiry_date_text > current_datetime:
                                    print(f"{expiry_date_text} is later than {current_datetime}")
                                elif expiry_date_text < current_datetime:
                                    print(f"{expiry_date_text} is earlier than {current_datetime}")
                                    result_message += f"Order ID {order_id}: Expected to be removed from table (Specified Date)\n"
                                    assert False, f"Order ID {order_id}: Expected to be removed from table (Specified Date)"
                                else:
                                    print(f"{expiry_date_text} is the same as {current_datetime}")
                            elif expiry_text == "Specified Date and Time":
                                # Compare the datetime objects
                                if expiry_date_text > current_datetime:
                                    print(f"{expiry_date_text} is later than {current_datetime}")
                                elif expiry_date_text < current_datetime:
                                    print(f"{expiry_date_text} is earlier than {current_datetime}")
                                    result_message += f"Order ID {order_id}: Expected to be removed from table (Specified Date and Time)\n"
                                    assert False, f"Order ID {order_id}: Expected to be removed from table (Specified Date and Time)"
                                else:
                                    print(f"{expiry_date_text} is the same as {current_datetime}")

                        # Check if we're dealing with the "order-history" tab
                        elif tab_order_type == "history":
                            print("Switching to Order History tab")
                            # Extract the 'Status' column text from the same row
                            status_cell = row.find_element(By.XPATH, ".//td[contains(@data-testid, 'column-status')]")
                            status_text = status_cell.text
                            print(f"Status text for Order ID {order_id}: {status_text}")
                            if status_text in ["CANCELLED", "Canceled"]:
                                print("cancel")
                                result_message += f"Order ID {order_id}: Status is Cancelled as expected\n"
                            elif status_text in ["EXPIRED", "Expired"]:
                                print("expired")
                                result_message += f"Order ID {order_id}: Status is Expired as expected\n"
                            else:
                                result_message += f"Order ID {order_id}: Unexpected status: {status_text}\n"
                                assert False, f"Unexpected status: {status_text}"

                        # Remove the found order_id from the failed list
                        # if order_id in failed_order_ids:
                        #     failed_order_ids.remove(order_id)

                        failed_order_ids.remove(order_id)
                        break  # Stop searching after finding the first match

        # If there are any order IDs that were not found, add to the result message
        for order_id in failed_order_ids:
            result_message += f"No Data match for {order_id}\n"

        # Attach the result message for reporting
        attach_text(result_message.strip(), name="Order Result for All Tabs")
        
        button_setting(driver, setting_option="logout")

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CHECK ORDERIDs IN TABLE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def check_orderIDs_in_table(driver, order_ids, tab_order_type, section_name: str, sub_tab = None, position : bool = False):
    """
    Checks if the specified order IDs exist in the given order panel and extracts relevant data for processing.

    Arguments:
    - order_ids (list): The list of order IDs to check.
    - order_panel (str): The data-testid of the order panel to check.
    - section_name (str): The name of the section for extracting order data.
    - sub_tab: The sub-tab to select within the order history section (e.g., 'orders-and-deals'). Default is None.
    - position (bool, optional): Whether to click on the position tab.

    Returns:
    - DataFrame: The extracted order panel data in a DataFrame format.
    """
    
    try:
        
        # spinner_element(driver)
        delay(2)
        
        type_orderPanel(driver, tab_order_type, sub_tab, position)
            
        # Locate the table body and wait for the spinner to disappear
        table_body = get_table_body(driver)
        
        spinner_element(driver)

        # Extract rows and order IDs from the table
        table_rows = table_body.find_elements(By.XPATH, ".//tr")
        table_order_ids = [element.text for element in table_body.find_elements(By.XPATH, ".//*[contains(@data-testid, 'order-id')]")]
        
        # Extract headers and check for chart symbol
        thead_data = get_table_headers(driver)

        # Check if the Symbol element exists and retrieve its data
        chart_symbol_name = get_chart_symbol_name(driver)
        if chart_symbol_name:
            thead_data.append("Symbol")

        table_row_contents = []

        # Check each provided order_id against the table order IDs
        for order_id in order_ids:
            if order_id in table_order_ids:
                # Find the index of the order_id in table_order_ids
                index = table_order_ids.index(order_id)
                row = table_rows[index]
                cells = row.find_elements(By.XPATH, ".//th[1] | .//th[2] | .//td")
                row_data = [cell.text for cell in cells]
                
                # Add chart symbol if applicable
                if chart_symbol_name:
                    row_data.append(chart_symbol_name)
                
                table_row_contents.append(row_data)
            else:
                # Log or handle the missing order ID
                assert False, f"Order ID {order_id} not found in the table."

        # If no order data was found, log this
        if not table_row_contents:
            assert False, "No matching order data found."
        
        # Create a DataFrame using the data
        orderPanel_data = extract_order_data_details(driver, table_row_contents, thead_data, section_name)
        process_individual_orders(driver, orderPanel_data, order_ids)
        return orderPanel_data

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""