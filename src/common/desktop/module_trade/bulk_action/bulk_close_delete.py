import traceback
import time

from selenium.webdriver.common.by import By

from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import take_screenshot
from constants.helper.element import click_element, find_element_by_testid, visibility_of_element_by_testid, visibility_of_element_by_xpath, spinner_element, is_element_disabled_by_cursor, extract_rgb_from_color
from common.desktop.module_trade.order_panel.op_general import extract_order_data_details, process_individual_orders, get_table_body, get_table_headers
from common.desktop.module_chart.chart import get_chart_symbol_name
from data_config.utils import append_orderIDs_to_csv




"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                PROCESS THE PROFIT / LOSS DATA
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def process_profit_loss(row, order_id, options_dropdown, table_order_ids, table_row_contents, row_data):
    try:
        # print(f"Processing Order ID: {order_id}, options_dropdown: {options_dropdown}")

        if not options_dropdown or options_dropdown == "all":
            table_order_ids.append(order_id)
            table_row_contents.append(row_data)
        elif options_dropdown in ("profit", "loss"):
            profit_cell = row.find_element(By.XPATH, ".//td[contains(@data-testid, 'column-profit')]")
            profit_value = profit_cell.text.strip()
            if (options_dropdown == "profit" and profit_value.startswith("+")) or (options_dropdown == "loss" and profit_value.startswith("-")):
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
    try:
        
        # Locate the button element by test ID
        bulk_orderType = find_element_by_testid(driver, data_testid=f"bulk-{bulk_type}")

        # Loop with a short sleep interval to check the button status
        start_time = time.time()
        max_wait = 3
        
        while time.time() - start_time < max_wait:
            is_disabled = is_element_disabled_by_cursor(driver, element=bulk_orderType)
            
            if not is_disabled:
                print("Button is enabled.")
                click_element(element=bulk_orderType)
                
                # If options dropdown is specified, interact with it
                if options_dropdown:
                    bulk_option = visibility_of_element_by_testid(driver, data_testid=f"dropdown-bulk-close-{options_dropdown}")
                    click_element(bulk_option)
                return
            delay(0.5) # Check every 0.5 seconds

        # Fail the test if the button is still disabled after waiting
        assert False, "Button is still disabled after waiting."
    
    except Exception as e:
        handle_exception(driver, e)



def button_bulk_operation(driver, bulk_type, filename, section_name, options_dropdown=None, symbol_name_element: bool = False):
    try:
        # Locate the table body
        table_body = get_table_body(driver)

        # Locate the table header
        thead_data = get_table_headers(driver)

        # Wait till the spinner icon no longer displays
        spinner_element(driver)

        bulk_action_close_delete(driver, bulk_type, options_dropdown)

        # Check if the Symbol element exists and retrieve its data
        chart_symbol_name = get_chart_symbol_name(driver)
        if chart_symbol_name:
            thead_data.append("Symbol")

        table_order_ids = []
        table_row_contents = []

        for row in table_body.find_elements(By.TAG_NAME, "tr"):
            cells = row.find_elements(By.XPATH, ".//th[1] | .//td")
            row_data = [cell.text for cell in cells]

            if chart_symbol_name:
                row_data.append(chart_symbol_name)

            order_id_cell = row.find_element(By.XPATH, ".//td[contains(@data-testid, 'order-id')]")
            order_id = order_id_cell.text.strip()
            
            # Locate the close button in the row and check if it's disabled
            btn_close_row = row.find_element(By.XPATH, ".//div[contains(@data-testid, 'button-close')]")
            close_disabled = is_element_disabled_by_cursor(driver, element=btn_close_row) 

            if symbol_name_element:  # For Asset Page
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
                process_profit_loss(row, order_id, options_dropdown, table_order_ids, table_row_contents, row_data)

        # Create a DataFrame using the data
        orderPanel_data = extract_order_data_details(driver, table_row_contents, thead_data, section_name)

        # Process each order_id separately to create individual tables
        process_individual_orders(driver, orderPanel_data, table_order_ids)

        append_orderIDs_to_csv(table_order_ids, filename)

        action_button = visibility_of_element_by_xpath(driver, ".//button[contains(@data-testid, 'button-submit')]")

        click_element(action_button)

        return orderPanel_data

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""