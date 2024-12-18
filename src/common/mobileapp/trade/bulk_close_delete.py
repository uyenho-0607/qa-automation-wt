import traceback

from selenium.webdriver.common.by import By

from constants.helper.screenshot import take_screenshot
from constants.helper.element import click_element_with_wait, find_element_by_testid, find_element_by_xpath_with_wait, spinner_element
from common.desktop.trade.common_function import extract_order_data_details, process_individual_orders, get_table_body, get_table_headers
from data_config.utils import append_orderIDs_to_csv
from common.desktop.chart.module_chart import get_chart_symbol_name



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                EXTRACT RGB COLOR FUNCTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def extract_rgb_from_color(color_string):
    try:

        # Extract RGB values from the color string
        rgb_values = tuple(map(int, color_string.strip('rgba()').split(',')[:3]))
        return rgb_values
    
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
                                                PROCESS THE PROFIT / LOSS DATA
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def process_profit_loss(row, order_id, options_dropdown, table_order_ids, table_row_contents, row_data):
    try:
            
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

def button_bulk_operation(driver, bulk_type, filename, section_name, options_dropdown=None, theme="dark", symbol_name_element: bool = False):
    try:

        # Locate the table body
        table_body = get_table_body(driver)
        
        # Locate the table header
        thead_data = get_table_headers(driver)
        
        # Wait till the spinner icon no longer display
        # spinner_element(driver)

        bulk_orderType = find_element_by_testid(driver, data_testid=f"bulk-{bulk_type}")
        click_element_with_wait(driver, element=bulk_orderType)
        # take_screenshot(driver, f"Confirmation_Dialog")

        if options_dropdown:
            bulk_option = find_element_by_testid(driver, data_testid=f"dropdown-bulk-close-{options_dropdown}")
            click_element_with_wait(driver, element=bulk_option)

        # Check if the Symbol element exists and retrieve its data
        chart_symbol_name = get_chart_symbol_name(driver)
        if chart_symbol_name:
            thead_data.append("Symbol")

        table_order_ids = []
        table_row_contents = []

        for row in table_body.find_elements(By.TAG_NAME, "tr"):
            cells = row.find_elements(By.XPATH, "./th[1] | ./td")
            row_data = [cell.text for cell in cells]
            
            if chart_symbol_name:
                row_data.append(chart_symbol_name)
            
            btn_close_row = row.find_element(By.XPATH, ".//div[contains(@data-testid, 'button-close')]")
            button_close_color_row = btn_close_row.value_of_css_property('color') # close button color
            closeBtn_rgb_row = extract_rgb_from_color(button_close_color_row)

            order_id_cell = row.find_element(By.CSS_SELECTOR, "td[data-testid*='-order-id']")
            order_id = order_id_cell.text.strip()
            
            if symbol_name_element: # For Asset Page
                symbol_name_row = row.find_element(driver, ".//td[contains(@data-testid, 'column-symbol')]")
                # symbol_name_row = row.find_element(By.XPATH, ".//span[contains(@class, 'sc-wfkeqv-0')]")
                symbol_color_row = symbol_name_row.value_of_css_property('color')
                symbol_rgb_row = extract_rgb_from_color(symbol_color_row)

                if theme == "dark":
                    symbol_disabled = symbol_rgb_row == (109, 119, 129)
                    close_disabled = closeBtn_rgb_row == (79, 86, 97)
                else:  # light theme
                    symbol_disabled = symbol_rgb_row == (169, 179, 179)
                    close_disabled = closeBtn_rgb_row == (180, 192, 204)

                if not symbol_disabled:
                    if not close_disabled:
                        process_profit_loss(row, order_id, options_dropdown, table_order_ids, table_row_contents, row_data)
                        # print("Symbol Name & Close button are enabled, system capturing orderID:", order_id)
                    else:
                        print("Symbol Name is enabled but Close button is disabled, prompting error for orderID:", order_id)
                        # assert False, ("Symbol Name is enabled but Close button is disabled, prompting error for orderID:", order_id)
                else:
                    print("Symbol Name and Close Button are Disabled for orderID:", order_id)
            else: # For Trade Page
                process_profit_loss(row, order_id, options_dropdown, table_order_ids, table_row_contents, row_data)

        # Create a DataFrame using the data
        orderPanel_data = extract_order_data_details(driver, table_row_contents, thead_data, section_name)

        # Process each order_id separately to create individual tables
        process_individual_orders(driver, orderPanel_data, table_order_ids)

        append_orderIDs_to_csv(table_order_ids, filename)

        # action_button_xpath = "//button[text()='Confirm']" if bulk_type == "delete" else ".//button[contains(@data-testid, 'submit')]"
        
        action_button_xpath = find_element_by_xpath_with_wait(driver, ".//button[contains(@data-testid, 'button-submit')]")

        action_button = find_element_by_xpath_with_wait(driver, action_button_xpath)
        
        click_element_with_wait(driver, element=action_button)

        return orderPanel_data

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "button_bulk_operation - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""