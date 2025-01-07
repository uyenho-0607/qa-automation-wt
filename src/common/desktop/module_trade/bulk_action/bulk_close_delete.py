import traceback
import time

from selenium.webdriver.common.by import By

from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, find_element_by_testid, visibility_of_element_by_testid, visibility_of_element_by_xpath, spinner_element, is_element_disabled_by_cursor
from common.desktop.module_trade.order_panel.op_general import extract_order_data_details, process_individual_orders, get_table_body, get_table_headers
from common.desktop.module_chart.chart import get_chart_symbol_name
from data_config.utils import append_orderIDs_to_csv


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                PROCESS THE PROFIT / LOSS DATA
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def process_profit_loss(row, order_id, options_dropdown, table_order_ids, table_row_contents, row_data):
    """
    Processes a single row in the table and filters the data based on the selected option (profit or loss).
    If the 'options_dropdown' is 'all', 'profit' or 'loss', it checks the respective cell value in the row.
    If the value matches the condition, it appends the order ID and row data to the results.

    Arguments:
    - row (WebElement): The row element in the table to process.
    - order_id: The order ID associated with the row.
    - options_dropdown: The option selected (either "profit", "loss", or "all").
    - table_order_ids (list): The list to append the order IDs that match the condition.
    - table_row_contents (list): The list to append the row data for matching orders.
    - row_data (dict): The data to append to the table_row_contents if conditions are met.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    
    try:
        # print(f"Processing Order ID: {order_id}, options_dropdown: {options_dropdown}")

        # If no specific option is selected or 'all' is selected, include all rows
        if not options_dropdown or options_dropdown == "all":
            # If the condition matches, append the order ID and row data
            table_order_ids.append(order_id)
            table_row_contents.append(row_data)
        # If the 'profit' or 'loss' option is selected, check for the respective conditions
        elif options_dropdown in ("profit", "loss"):
            profit_cell = row.find_element(By.XPATH, ".//td[contains(@data-testid, 'column-profit')]")
            profit_value = profit_cell.text.strip() # Get the text value from the profit cell and remove extra spaces
            # Check if the profit/loss value matches the selected option ('profit' starts with '+', 'loss' starts with '-')
            if (options_dropdown == "profit" and profit_value.startswith("+")) or (options_dropdown == "loss" and profit_value.startswith("-")):
                # If the condition matches, append the order ID and row data
                table_order_ids.append(order_id)
                table_row_contents.append(row_data)
    except Exception as e:
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                BULK CLOSE / DELETE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def bulk_action_close_delete(driver, bulk_type, options_dropdown=None):
    """
    Perform a bulk action (close/delete) for orders, based on the specified bulk_type.
    If an optional dropdown option is provided, interact with it after clicking the bulk action button.

    Arguments:
    - bulk_type: The type of bulk action to perform (e.g., "close" or "delete").
    - options_dropdown: The specific dropdown option to interact with after clicking the button (e.g. "profit", "loss", or "all", default is None).

    Raises:
    - AssertionError: If the bulk action button remains disabled after a maximum wait time.
    - Any other exceptions: These are caught and handled by the `handle_exception` function.
    """
    try:
        
        # Locate the button element by test ID
        bulk_orderType = find_element_by_testid(driver, data_testid=f"bulk-{bulk_type}")

        # Set the maximum wait time to 3 seconds and start the timer
        start_time = time.time()
        max_wait = 3
        
        # Loop to repeatedly check the status of the button for 3 seconds
        while time.time() - start_time < max_wait:
            # Check if the bulk action button is disabled by inspecting the cursor's state
            is_disabled = is_element_disabled_by_cursor(driver, element=bulk_orderType)
            
            # If the button is not disabled, proceed with clicking it
            if not is_disabled:
                print("Button is enabled.")
                click_element(element=bulk_orderType)
                
                # If an optional dropdown option is provided, click the corresponding dropdown option
                if options_dropdown:
                    bulk_option = visibility_of_element_by_testid(driver, data_testid=f"dropdown-bulk-close-{options_dropdown}")
                    click_element(bulk_option)
                return
            delay(0.5) # Check every 0.5 seconds

        # If the button remains disabled after the maximum wait time, fail the test
        assert False, "Button is still disabled after waiting."
    
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                BULK CLOSE / DELETE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_bulk_operation(driver, bulk_type, filename, section_name, options_dropdown=None, symbol_name_element: bool = False):
    """
    Perform a bulk action (e.g., close/delete) on orders, process each row in the table based on the action,
    and interact with specific symbol name logic depending on whether it's an Asset or Trade page.

    Arguments:
    - bulk_type (str): The type of bulk operation (e.g., "close", "delete").
    - filename (str): The filename to append order IDs to (in CSV format).
    - section_name (str): The name of the section used for extracting order details.
    - options_dropdown (str, optional): The dropdown option to filter the results (e.g., "profit", "loss").
    - symbol_name_element (bool, optional): Whether to interact with the symbol name (used for Asset Page logic).

    Returns:
    - orderPanel_data (DataFrame): A DataFrame containing the processed order details.

    Raises:
    - Any exceptions during execution are caught and handled by the `handle_exception` function.
    """
    try:

        # Locate the table body and table headers
        table_body = get_table_body(driver)
        thead_data = get_table_headers(driver)

        # Wait till the spinner icon no longer displays
        spinner_element(driver)

        # Perform the bulk action (close/delete) and handle dropdown selection if provided
        bulk_action_close_delete(driver, bulk_type, options_dropdown)

        # Check if the Symbol element exists and retrieve its data
        chart_symbol_name = get_chart_symbol_name(driver)
        if chart_symbol_name:
            thead_data.append("Symbol")

        # Initialize lists to store order IDs and row contents
        table_order_ids = []
        table_row_contents = []

        # Loop through each row in the table body
        for row in table_body.find_elements(By.TAG_NAME, "tr"):
            cells = row.find_elements(By.XPATH, ".//th[1] | .//td")
            row_data = [cell.text for cell in cells]

            # Append the chart symbol name to the row data if applicable
            if chart_symbol_name:
                row_data.append(chart_symbol_name)

            # Extract the order ID from the row
            order_id_cell = row.find_element(By.XPATH, ".//td[contains(@data-testid, 'order-id')]")
            order_id = order_id_cell.text.strip()
            
            # Locate the close button in the row and check if it's disabled
            btn_close_row = row.find_element(By.XPATH, ".//div[contains(@data-testid, 'button-close')]")
            close_disabled = is_element_disabled_by_cursor(driver, element=btn_close_row) 

            # Check if the symbol name element exists (for Asset Page)
            if symbol_name_element:
                # Locate the symbol name cell and check if it's disabled
                symbol_name_row = row.find_element(By.XPATH, ".//td[contains(@data-testid, 'column-symbol')]/span")
                symbol_disabled = is_element_disabled_by_cursor(driver, element=symbol_name_row)
                print(f"symbol orderID: {order_id} is {symbol_disabled}")

                # Check the state of symbol name and close button and handle accordingly
                if not symbol_disabled and not close_disabled:
                    # Both buttons are enabled, process the row
                    process_profit_loss(row, order_id, options_dropdown, table_order_ids, table_row_contents, row_data)
                    print(f"Symbol Name & Close button are enabled, system capturing orderID: {order_id}")
                
                elif not symbol_disabled and close_disabled:
                    # Symbol name is enabled but close button is disabled
                    print(f"Symbol Name is enabled but Close button is disabled, prompting error for orderID: {order_id}")
                    # assert False, ("Symbol Name is enabled but Close button is disabled, prompting error for orderID:", order_id)
                
                elif symbol_disabled and close_disabled:
                    # Both buttons are disabled
                    print(f"Symbol Name and Close Button are disabled for orderID: {order_id}")
                
                elif symbol_disabled and not close_disabled:
                    # Symbol name is disabled but close button is enabled
                    print(f"Symbol Name is disabled but Close button is enabled for orderID: {order_id}")
            else:  # For Trade Page
                # Process the row regardless of the symbol name element
                process_profit_loss(row, order_id, options_dropdown, table_order_ids, table_row_contents, row_data)

        # Create a DataFrame using the data
        orderPanel_data = extract_order_data_details(driver, table_row_contents, thead_data, section_name)

        # Process each order_id separately to create individual tables
        process_individual_orders(driver, orderPanel_data, table_order_ids)

        append_orderIDs_to_csv(table_order_ids, filename)

        # Locate the submit button and click it to finalize the operation
        action_button = visibility_of_element_by_xpath(driver, ".//button[contains(@data-testid, 'button-submit')]")
        click_element(action_button)

        # Return the processed order data
        return orderPanel_data

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""