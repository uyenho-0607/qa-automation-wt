from tabulate import tabulate

from selenium.webdriver.common.by import By

from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text
from constants.helper.element import wait_for_element_visibility, spinner_element, javascript_click, click_element, click_element_with_wait, find_element_by_testid, find_element_by_xpath, find_element_by_xpath_with_wait, visibility_of_element_by_xpath, visibility_of_element_by_testid, get_label_of_element
from common.desktop.module_trade.order_panel.op_general import extract_order_data_details, process_individual_orders, get_table_body, get_table_headers
from common.desktop.module_chart.chart import get_chart_symbol_name


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
        javascript_click(driver, element=orderPanel_type)
        
        # If position is True, navigate to the position sub-tab within the order history
        if position:
            # Find and click on the specific sub-tab within the order history section
            # orderHistory_position = visibility_of_element_by_testid(driver, data_testid="tab-asset-order-type-history-orders-and-deals")
            orderHistory_position = find_element_by_testid(driver, data_testid=f"tab-asset-order-type-history-{sub_tab}")
            click_element(orderHistory_position)
            
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
def button_orderPanel_action(driver, order_action, row_number, delete_button: bool = False):
    """
    Performs actions (edit, close, delete) on specified rows in the order panel.

    Arguments:
    - order_action (str): The action to perform on the order (e.g., 'track', 'edit', 'close').
    - row_number (list or int): The row(s) to perform the action on (can be a single row number or a list of row numbers).
    - delete_button (bool, optional): If True, the delete button for a pending order is clicked. Default is False.

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

        # If delete_button is True, click the delete order button (For OCT)
        if delete_button:
            # local_delete_button = find_element_by_testid(driver, data_testid="close-order-button-submit")
            local_delete_button = find_element_by_xpath(driver, "//button[contains(normalize-space(text()), 'Delete Order')]")
            click_element(local_delete_button)
        
        # Handle order-specific confirmation modals based on the order_action
        if order_action == "edit":
            visibility_of_element_by_testid(driver, data_testid="edit-confirmation-modal")

        if order_action == "close":
            try:
                 # Handle the close action specifically
                visibility_of_element_by_xpath(driver, "//div[@class='sc-ur24yu-1 eqxJBS']")
            except Exception as e:
                pass
                
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
            order_id_element = table_row.find_element(By.XPATH, ".//td[contains(@data-testid, 'order-id')]")
            
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
    Extract order information including order IDs and other details from the specified rows in the order table.

    Arguments:
    - tab_order_type: The order type tab to select (e.g., 'open-positions', 'pending-orders', 'order-history').
    - section_name: The section name for logging purposes.
    - row_number: A list of row numbers to extract data from.
    - sub_tab: The sub-tab to select within the order history section (e.g., 'orders-and-deals'). Default is None.
    - position: Boolean to indicate if position-related data should be included (default is False).

    Returns:
    - order_ids: A list of extracted order IDs.
    - orderPanel_data: A DataFrame containing the extracted order details.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    
    # Initialize an empty list to hold the data
    order_ids = []
    table_row_contents = []

    try:
        # Navigate to the specified tab
        type_orderPanel(driver, tab_order_type, sub_tab, position)
        
        # if response.status_code == 200:
        spinner_element(driver)

        # Locate the table body and header
        table_body = get_table_body(driver)
        thead_data = get_table_headers(driver)

        spinner_element(driver)
        
        # Check if the Symbol element exists and retrieve its data
        chart_symbol_name = get_chart_symbol_name(driver)
        if chart_symbol_name:
            thead_data.append("Symbol")

        # Extract data from each specified row for order IDs and row details
        for row in row_number:
            table_row = table_body.find_element(By.XPATH, f".//tr[{row}]")

            # Locate and extract the order ID from the current row
            # order_id_element = visibility_of_element_by_xpath(driver, ".//td[contains(@data-testid, 'order-id')]")
            order_id_element = table_row.find_element(By.XPATH, ".//td[contains(@data-testid, 'order-id')]")
            order_ids.append(order_id_element.text)

            # Extract data from the row for the table content
            cells = table_row.find_elements(By.XPATH, ".//th[1] | .//td")

            row_data = []
            for cell in cells:            
                wait_for_element_visibility(driver, cell)
                row_data.append(cell.text)
            
            # Add the chart symbol name if it exists
            if chart_symbol_name:
                row_data.append(chart_symbol_name)
                
            table_row_contents.append(row_data)

        # Attach order IDs text
        attach_text(order_id_element.text, name="orderID")

        # else:
        #     assert False, f"Failed to fetch data. Status code: {response.status_code}"
        
        # Create a DataFrame using the data
        orderPanel_data = extract_order_data_details(driver, table_row_contents, thead_data, section_name)
        overall = tabulate(orderPanel_data.set_index('Section').T.fillna('-'), headers='keys', tablefmt='grid', stralign='center')
        attach_text(overall, name=section_name)

        return order_ids, orderPanel_data

    except Exception as e:
        # Handle any exceptions that occur during the execution
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
        "tab-asset-order-type-history": "Order History / Position",
        "tab-asset-order-type-history-orders-and-deals": "Order History (Order & Deals)",
        "tab-asset-order-type-pending-orders": "Pending Orders",
        "tab-asset-order-type-open-positions": "Open Positions",
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

# Ensure the pending order - orderIDs not in the table
def review_pending_orderIDs(driver, order_ids, order_panel):
    """
    Reviews the pending order IDs in the specified order panel and compares them with the provided order IDs.

    Arguments:
    - order_ids (list): The list of order IDs to check.
    - order_panel (str): The data-testid of the order panel to review.

    Returns:
    - list: A list of order IDs that were not found in the table.
    """
    try:
        # Find the order panel element and click it
        type_orderPanel = find_element_by_testid(driver, data_testid=order_panel)
        click_element_with_wait(driver, element=type_orderPanel)

        # Wait for the table body to load and the spinner to disappear
        table_body = get_table_body(driver)

        spinner_element(driver)

        # Get the order IDs displayed in the table
        table_order_ids = [element.text for element in table_body.find_elements(By.XPATH, ".//td[contains(@data-testid, 'order-id')]")]

        failed_order_ids = []
        
        # Generate a result message
        result_message = f"Switching to order panel: {get_order_panel_name(order_panel)}\n"
        
        # Compare the provided order IDs with those in the table
        for order_id in order_ids:
            if order_id in table_order_ids:
                result_message += f"Data match for {order_id}\n"
            else:
                result_message += f"No Data match for {order_id}\n"
                failed_order_ids.append(order_id)
        
        # Attach the result message for reporting
        attach_text(result_message.strip(), name="Order Result")

        # Return the list of failed order IDs
        return failed_order_ids

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

def check_orderIDs_in_table(driver, order_ids, order_panel, section_name, sub_tab = None, position : bool = False):
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
        type_orderPanel = find_element_by_testid(driver, data_testid=order_panel)
        click_element_with_wait(driver, element=type_orderPanel)

        # If position tab is specified, click it
        if position:
            orderHistory_position = find_element_by_testid(driver, data_testid=f"tab-asset-order-type-history-{sub_tab}")
            click_element_with_wait(driver, element=orderHistory_position)
            
        # Locate the table body and wait for the spinner to disappear
        table_body = get_table_body(driver)
        
        spinner_element(driver)

        # Extract rows and order IDs from the table
        table_rows = table_body.find_elements(By.XPATH, ".//tr")
        table_order_ids = [element.text for element in table_body.find_elements(By.XPATH, ".//td[contains(@data-testid, 'order-id')]")]
        
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
                cells = row.find_elements(By.XPATH, "./th[1] | ./td")
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