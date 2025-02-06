

import random
from selenium.webdriver.common.by import By

from constants.helper.driver import delay
from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element import find_element_by_xpath, spinner_element, visibility_of_element_by_xpath, click_element, click_element_with_wait, find_list_of_elements_by_xpath, wait_for_text_to_be_present_in_element_by_xpath

from common.desktop.module_subMenu.sub_menu import menu_button
from common.desktop.module_markets.markets_watchlist import handle_alert_success
from common.desktop.module_trade.order_panel.utils import get_table_headers, type_orderPanel, OH_closeDate

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TABLE BODY FUNCTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def update_column_visibility(driver, tab_order_type: str, sub_tab: str = None, set_menu: bool = False, position: bool = False):
    try:
        if set_menu:
            current_tab = menu_button(driver, menu="assets")
        else:
            current_tab = menu_button(driver, menu="trade")
            
        type_orderPanel(driver, tab_order_type, sub_tab, position)
        
        spinner_element(driver)
        
        before_table_header = get_table_headers(driver)
        print("Original table:", before_table_header)
        
        sort_column = visibility_of_element_by_xpath(driver, "//div[@class='sc-ew7enm-0 kCTcGI bordered']")
        click_element(element=sort_column)
        
        wait_for_text_to_be_present_in_element_by_xpath(driver, "//div[text()='Select the columns you would like to see']", text="Select the columns you would like to see")
        
        delay(1)
        
        unchecked_checkboxes = find_list_of_elements_by_xpath(driver, "(//div[@class='sc-1byafbj-1 gdFGzr'])[1]")
        checked_checkboxes = find_list_of_elements_by_xpath(driver, "(//div[contains(@class, 'sc-1byafbj-1 dTVOzk')])[1]")
        
        all_checkboxes = unchecked_checkboxes + checked_checkboxes
        random_checkbox = random.choice(all_checkboxes)
        
        if random_checkbox in unchecked_checkboxes:
            click_element(element=random_checkbox)
            action = "checked"
            expected_symbol_visibility = True
        else:
            click_element(element=random_checkbox)
            action = "unchecked"
            expected_symbol_visibility = False

        filter_header_name = random_checkbox.find_element(By.XPATH, ".//ancestor::div[contains(@class, 'sc-1byafbj-0 KiIAV')]")
        filter_name = filter_header_name.text.strip()
        print(f"\nCheckbox for Show / Hide filter '{filter_name}' {action}.")

        if filter_name == 'Show all':
            filter_header = find_list_of_elements_by_xpath(driver, "//div[@class='sc-maosa0-0 fbUvmH']")
            filter_header_list = [header.text.strip() for header in filter_header]
            print(f"Full list of header name: {filter_header_list} {action}\n")
        else:
            filter_header_list = [filter_name]
        
        # Replace 'Price' with 'Entry Price' in the filter_header_list
        filter_header_list = ["Entry Price" if header == "Price" else header for header in filter_header_list]
        
        save_button = find_element_by_xpath(driver, "//button[text()='Save Changes']")
        click_element(element=save_button)

        alert_msg = handle_alert_success(driver)
        if alert_msg != "All changes are saved.":
            raise AssertionError(f"Receive {alert_msg} instead of the expected message")

        close = find_element_by_xpath(driver, "//div[@class='sc-ur24yu-4 jgnDww']")
        click_element(close)
        
        after_table_header = get_table_headers(driver)
        print(f"Final validated table headers for {current_tab}:", after_table_header)
        
        for header in filter_header_list:
            if expected_symbol_visibility:
                print("Expected header is visible:", header)
                assert header in after_table_header, f"'{header}' was checked but is missing from the table!"
            else:
                print("Expected header is hidden:", header)
                assert header not in after_table_header, f"'{header}' was unchecked but still found in the table!"
        
        new_tab = "assets" if current_tab == "trade" else "trade"
        menu_button(driver, menu=new_tab)

        type_orderPanel(driver, tab_order_type, sub_tab, position)
        
        spinner_element(driver)

        after_table_header_new = get_table_headers(driver)
        print(f"Final validated table headers in {new_tab}:", after_table_header_new)

        for header in filter_header_list:
            if expected_symbol_visibility:
                print("Expected header is visible:", header)
                assert header in after_table_header_new, f"'{header}' was checked but is missing from {new_tab} table!"
            else:
                print("Expected header is hidden:", header)
                assert header not in after_table_header_new, f"'{header}' was unchecked but still found in {new_tab} table!"

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def toggle_order_panel_sort(driver, set_menu: bool = False, random_choice: bool = False, startDate: str = None, endDate: str = None, target_startMonth: str = None, target_endMonth: str = None):
    try:
        
        if set_menu:
            menu_button(driver, menu="assets")

        # Function to switch tabs and perform sorting
        type_orderPanel(driver, tab_order_type="open-positions")
        delay(2)
        perform_sorting(driver, random_choice)
        
        # type_orderPanel(driver, tab_order_type="pending-orders")
        # delay(2)
        # perform_sorting(driver)
        
        # tab_order_type = type_orderPanel(driver, tab_order_type="history")
        
        # if tab_order_type == "history":
        #     OH_closeDate(driver, startDate, endDate, target_startMonth, target_endMonth)
        #     delay(2)
        #     perform_sorting(driver)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)


def perform_sorting(driver, random_choice=False):
    try:
        # Wait for the spinner to disappear
        spinner_element(driver)

        # Check if the table has any data
        empty_message_elements = find_list_of_elements_by_xpath(driver, "//div[@class='sc-1xa1s3v-1 eNxvZp']")
        if empty_message_elements:
            empty_message = empty_message_elements[0].text.strip()
            assert False, f"Table is empty. Message: '{empty_message}'"

        # Locate and click the sort button
        sort_btn = visibility_of_element_by_xpath(driver, "(//div[@data-testid='asset-order-type']//div)[6]//div[3]")
        click_element(element=sort_btn)

        # Get the list of sort options
        sort_options = find_list_of_elements_by_xpath(driver, "//div[@class='sc-13tz5xz-2 cPmkEI']//div[@class='sc-19aa2c1-2 dTOaOe']")
        
        # Define the column types
        column_types = {
            "Open Date": "Open Date",
            "Symbol": "Symbol",
            "Profit": "Profit",
            "Close Date": "Close Date"
        }

        # If no sorting options are found, raise an exception
        if not sort_options:
            raise ValueError("No sorting options found.")

        # If random_choice is True, select one random option and verify sorting only once
        if random_choice:
            selected_sort = random.choice(sort_options)
            sort_text = selected_sort.text.strip()
            print("Randomly selected sorting is: ", sort_text)

            if sort_text in column_types:
                click_element_with_wait(driver, element=selected_sort)
                verify_sort_column(driver, column_type=column_types[sort_text])
            else:
                raise ValueError(f"Unknown sort option: {sort_text}")
            return  # Exit the function after verifying one option

        # If random_choice is False, iterate through all available sort options
        for sort in sort_options:
            sort_text = sort.text.strip()

            if sort_text in column_types:
                click_element_with_wait(driver, element=sort)
                verify_sort_column(driver, column_type=column_types[sort_text])
                click_element_with_wait(driver, element=sort)  # Sort again to check reverse order
                verify_sort_column(driver, column_type=column_types[sort_text])
            else:
                raise ValueError(f"Unknown sort option: {sort_text}")

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def verify_sort_column(driver, column_type):
    """
    Verifies if a column is sorted, either ascending or descending, based on the column type.
    
    :param driver: WebDriver instance
    :param column_type: The column to verify (openDate, symbol, profit)
    """
    # Define the XPaths based on the column type
    column_xpath_map = {
        "Open Date": "//th[contains(@data-testid, 'column-open-date')]",
        "Symbol": "//td[contains(@data-testid, 'column-symbol')]",
        "Profit": "//td[contains(@data-testid, 'column-profit')]",
        "Close Date": "//td[contains(@data-testid, 'column-close-date')]"
    }
    
    # Extract text from the column based on the column type
    column_elements = find_list_of_elements_by_xpath(driver, column_xpath_map[column_type])
    column_values = [element.text.strip() for element in column_elements]

    # Clean the values for sorting (keep signs and commas)
    def convert_value(value):
        """Converts the string to a float while keeping the + or - sign."""
        # Remove commas for proper conversion to float and keep + and - signs
        return float(value.replace(",", ""))

    # Handle "Profit" column specifically for numeric comparison
    if column_type == "Profit":
        column_values = [convert_value(value) for value in column_values]
    
    # Check if the column is sorted in ascending order
    ascending_sorted_values = sorted(column_values)
    
    # Check if the column is sorted in descending order
    descending_sorted_values = sorted(column_values, reverse=True)

    # Print the result for both orders
    # print(f"\nExpected '{column_type}' column values sorted: \nAscending: {ascending_sorted_values}\nDescending: {descending_sorted_values}")

    # Verify if the column is sorted in ascending order
    if column_values == ascending_sorted_values:
        combined_text = (f"Retrieve '{column_type}' column values:\n{column_values}\n\n"
                         f"Expected '{column_type}' column values:\n{ascending_sorted_values}\n\n")

        attach_text(combined_text, name=f"Column '{column_type}' is sorted in ascending order.")
        
    # Verify if the column is sorted in descending order
    elif column_values == descending_sorted_values:
        combined_text = (f"Retrieve '{column_type}' column values:\n{column_values}\n\n"
                         f"Expected '{column_type}' column values:\n{descending_sorted_values}\n\n")
        attach_text(combined_text, name=f"Column '{column_type}' is sorted in descending order.")
    else:
        assert False, f"\nColumn '{column_type}' is not sorted correctly."
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""