import re
from tabulate import tabulate
from dateutil.parser import parse

from selenium.webdriver.common.by import By

from enums.main import Menu, OrderPanel, Setting
from constants.element_ids import DataTestID

from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text
from constants.helper.element import is_element_present_by_xpath, spinner_element, javascript_click, click_element, click_element_with_wait, find_element_by_testid, find_element_by_xpath, find_element_by_xpath_with_wait, is_element_present_by_testid, find_visible_element_by_xpath, find_visible_element_by_testid, get_label_of_element

from common.desktop.module_trade.order_panel.op_general import extract_order_data_details, process_individual_orders, get_table_body, get_table_headers
from common.desktop.module_chart.chart import get_chart_symbol_name
from common.desktop.module_assets.account_info import get_server_local_time
from common.desktop.module_setting.setting_general import button_setting
from common.desktop.module_sub_menu.sub_menu import menu_button
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
            """
            Processes a given menu (Trade or Assets) and counts the number of orders
            in Open Positions and Pending Orders tabs.
            """
            
            # Click on the specified menu (Trade or Assets)
            current_tab = menu_button(driver, menu=menu_name)
            counts = {}  # Dictionary to store counts for each tab
            
            for tab in [OrderPanel.OPEN_POSITIONS, OrderPanel.PENDING_ORDERS]:
                # Retrieve the label count for the given order panel type
                _, button_name = type_orderPanel(driver, tab_order_type=tab)
                
                # Extract the number using regex
                count = int(re.search(r'\d+', button_name).group())
                counts[tab] = count  # Store the count for the tab
            
            return current_tab, counts  # Return both tab name and counts
        
        # Process "Trade" menu and get the order counts
        current_tab, trade_counts = process_tabs(Menu.TRADE)
        if current_tab == "trade":
            print(f"Total counts for 'Trade': {trade_counts}")
            
            # Check if any tab in "trade" exceeds 30 orders
            for tab, count in trade_counts.items():
                if count > 30:
                    assert False, f"Trade - {tab} should not have more than 30 orders (current count: {count})"
        
        # Process "Assets" menu and get the order counts
        current_tab, asset_counts = process_tabs(Menu.ASSETS)
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
def type_orderPanel(driver, tab_order_type: OrderPanel):
    """
    Switches between different tabs in the asset order panel.

    Arguments:
    - driver: Selenium WebDriver instance.
    - tab_order_type: The order type tab to select (e.g., 'open-positions', 'pending-orders', 'order-history', 'position-history', 'orders-and-deals').

    Raises:
    - ValueError: If an invalid tab_order_type is provided.
    """
    try:
        delay(1)  # Ensure elements are loaded

        # Define the main tabs
        button_testids = {
            OrderPanel.OPEN_POSITIONS: DataTestID.TAB_ASSET_ORDER_TYPE_OPEN_POSITIONS,
            OrderPanel.PENDING_ORDERS: DataTestID.TAB_ASSET_ORDER_TYPE_PENDING_ORDERS,
            OrderPanel.HISTORY: DataTestID.TAB_ASSET_ORDER_TYPE_HISTORY,
        }

        # If the user tries to directly call POSITION_HISTORY or ORDER_AND_DEALS, we first select HISTORY
        if tab_order_type in {OrderPanel.POSITION_HISTORY, OrderPanel.ORDER_AND_DEALS}:
            # Click on HISTORY tab first
            history_tab = find_visible_element_by_testid(driver, DataTestID.TAB_ASSET_ORDER_TYPE_HISTORY)
            javascript_click(driver, element=history_tab)
            delay(1)  # Wait for sub-tabs to appear

            # Now, select the correct sub-tab
            if tab_order_type == OrderPanel.POSITION_HISTORY:
                position_history_tab = find_visible_element_by_testid(driver, DataTestID.TAB_ASSET_ORDER_TYPE_HISTORY_POSITIONS_HISTORY)
                javascript_click(driver, element=position_history_tab)
            elif tab_order_type == OrderPanel.ORDER_AND_DEALS:
                order_and_deals_tab = find_visible_element_by_testid(driver, DataTestID.TAB_ASSET_ORDER_TYPE_HISTORY_ORDERS_AND_DEALS)
                javascript_click(driver, element=order_and_deals_tab)

            # Ensure label_count is returned as None for sub-tabs
            return tab_order_type, None

        # If the tab_order_type is a main tab, locate and click it
        button_testid = button_testids.get(tab_order_type)
        if not button_testid:
            raise ValueError(f"Invalid button type: {tab_order_type}")

        # Locate and click the main tab
        order_panel_type = find_visible_element_by_testid(driver, button_testid)
        label_count = get_label_of_element(order_panel_type)
        javascript_click(driver, element=order_panel_type)
        
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
def handle_track_close_edit(driver, trade_type):
    """
    Performs actions (edit, close, delete) on specified rows in the order panel.

    Arguments:
    - order_action (str): The action to perform on the order (e.g., 'track', 'edit', 'close').
    - row_number (list or int): The row(s) to perform the action on (can be a single row number or a list of row numbers).

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        
        # Loop through the provided row numbers to click the action button for each row
        # Find the action button (e.g., edit, close) for the specified row
        action_button = find_element_by_xpath(driver, f"(//div[contains(@data-testid, 'button-{trade_type}')])[1]")
        click_element(action_button)
        
        delay(0.2)
        
        # Handle order-specific confirmation modals based on the order_action
        if is_element_present_by_xpath(driver, "//div[contains(@data-testid, 'confirmation-modal')]"):
            find_visible_element_by_xpath(driver, "//div[contains(@data-testid, 'confirmation-modal')]")
        
        
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
def extract_order_info(driver, tab_order_type: OrderPanel, section_name):
    """
    Extracts order info from the first row of the order panel table.
    """
    order_ids = []
    table_row_contents = []

    try:
        # Navigate to tab
        type_orderPanel(driver, tab_order_type)

        # Wait for spinner once
        spinner_element(driver)

        # Get table body and headers
        table_body = get_table_body(driver)
        thead_data = get_table_headers(driver)

        # Check if Symbol element exists
        chart_symbol_name = get_chart_symbol_name(driver)
        if chart_symbol_name:
            thead_data.append("Symbol")

        # Extract only the first row
        all_rows = table_body.find_elements(By.XPATH, ".//tr[1]")
        for table_row in all_rows:
            # Extract Order ID
            order_id_element = table_row.find_element(By.XPATH, ".//*[contains(@data-testid, 'order-id')]")
            order_id_text = order_id_element.text.strip()
            order_ids.append(order_id_text)

            # Extract row data
            cells = table_row.find_elements(By.XPATH, ".//th[1] | .//th[2] | .//td")
            row_data = [re.sub(r'\s*/\s*', ' / ', cell.text.strip()) for cell in cells]

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
def review_pending_orderIDs(driver, order_ids, check_extended_tabs=False):
    """
    Reviews the pending order IDs across the available order panel tabs,
    comparing them with the provided order IDs.

    Arguments:
    - driver: Selenium WebDriver instance.
    - order_ids (list): The list of order IDs to check.
    - check_extended_tabs (bool): Whether to check "Position History" and "Orders & Deals".

    Returns:
    - list: A list of order IDs that were not found in any tab.
    """
    tabs = [OrderPanel.OPEN_POSITIONS, OrderPanel.PENDING_ORDERS, OrderPanel.HISTORY]

    if check_extended_tabs:
        tabs.extend([OrderPanel.POSITION_HISTORY, OrderPanel.ORDER_AND_DEALS])

    failed_order_ids = order_ids.copy()
    result_message = ""

    try:
        for tab_order_type in tabs:
            if not failed_order_ids:
                break  # Stop checking if all order IDs are found

            menu_button(driver, menu=Menu.ASSETS)
            selected_tab, _ = type_orderPanel(driver, tab_order_type)
            
            table_body = get_table_body(driver)
            spinner_element(driver)

            rows = table_body.find_elements(By.XPATH, ".//tr")
            spinner_element(driver)

            current_datetime = parse(get_server_local_time(driver))

            for order_id in failed_order_ids[:]:
                order_id_str = str(order_id)  # Convert order_id to string for comparison
                for row in rows:
                    try:
                        order_id_cell = row.find_element(By.XPATH, ".//*[contains(@data-testid, 'order-id')]")
                        if order_id_str not in order_id_cell.text:
                            continue
                        
                        result_message += f"Order ID {order_id} found in {selected_tab}\n"

                        # Apply PENDING_ORDERS logic
                        if selected_tab == OrderPanel.PENDING_ORDERS:
                            expiry_text = get_label_of_element(row.find_element(By.XPATH, ".//td[contains(@data-testid, 'column-expiry')]"))
                            expiry_date_cells = row.find_elements(By.XPATH, ".//td[contains(@data-testid, 'column-expiry-date')]")

                            if expiry_text in ["Specified Date", "Specified Date and Time"] and expiry_date_cells:
                                expiry_date_str = get_label_of_element(expiry_date_cells[0]).strip()
                                expiry_date_text = parse(expiry_date_str)

                                if " " in expiry_date_str:  # Expiry includes time
                                    if expiry_date_text < current_datetime:
                                        result_message += f"Order ID {order_id}: Expected removal ({expiry_text})\n"
                                        # No assertion here, just log the issue
                                else:  # Expiry contains only date
                                    if expiry_date_text.date() < current_datetime.date():
                                        result_message += f"Order ID {order_id}: Expected removal ({expiry_text})\n"
                                        # No assertion here, just log the issue

                            result_message += f"Order ID {order_id}: {expiry_text} (Status Checked)\n"

                        # Apply HISTORY and ORDER_AND_DEALS logic (status check if available)
                        elif selected_tab in [OrderPanel.HISTORY, OrderPanel.ORDER_AND_DEALS]:
                            status_cells = row.find_elements(By.XPATH, ".//td[contains(@data-testid, 'column-status')]")
                            if status_cells:  # Check if status column exists
                                status_text = status_cells[0].text
                                expected_statuses = {"CANCELLED", "Canceled", "EXPIRED", "Expired"}

                                if status_text not in expected_statuses:
                                    result_message += f"Order ID {order_id}: Unexpected status: {status_text}\n"
                                    # No assertion, just log the unexpected status
                                else:
                                    result_message += f"Order ID {order_id}: Status is {status_text} as expected\n"
                            else:
                                result_message += f"Order ID {order_id}: No status column available\n"

                        # For POSITION_HISTORY, no status check is needed
                        elif selected_tab == OrderPanel.POSITION_HISTORY:
                            # Simply acknowledge it was found, no status check
                            result_message += f"Order ID {order_id}: Found in Position History (no status check)\n"

                        failed_order_ids.remove(order_id)
                        break
                    except Exception as e:
                        print(f"Error processing row in {selected_tab} for Order ID {order_id}: {str(e)}")
                        continue

        if failed_order_ids:
            result_message += f"Order IDs not found in any tab: {failed_order_ids}\n"

        attach_text(result_message.strip(), name="Order Result for All Tabs")
        button_setting(driver, setting_option=Setting.LOGOUT)

    except Exception as e:
        handle_exception(driver, e)

    return failed_order_ids

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CHECK ORDERIDs IN TABLE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def check_orderIDs_in_table(driver, order_ids, tab_order_type: OrderPanel, section_name: str):
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
        
        type_orderPanel(driver, tab_order_type)
            
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