import random
from selenium.webdriver.common.by import By

from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception
from constants.helper.element import clear_input_field, click_element, click_element_with_wait, find_element_by_testid, is_element_present_by_testid, populate_element, find_list_of_elements_by_testid, spinner_element, visibility_of_element_by_xpath, visibility_of_element_by_testid, wait_for_text_to_be_present_in_element_by_testid, get_label_of_element

from data_config.file_handler import read_symbol_file
from common.desktop.module_chart.chart import get_chart_symbol_name



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                INPUT SYMBOL
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def input_symbol(driver, server: str, client_name: str, symbol_type: str = "Symbols", desired_symbol_name: str = None):
    """
    The function interacts with the platform's symbol search input field, selects the desired symbol 
    from a dropdown, and verifies that the correct symbol is shown in the chart.
    
    Arguments:
    - platform: The platform from which to load symbols (e.g., 'MT4', 'MT5').
    - client_name: The client name to load the corresponding symbols. (e.g. 'Lirunex', 'Transactcloudmt5')
    - symbol_type: The type of symbol to search for, default is "Symbols".
    - desired_symbol_name: A specific symbol name to search for. 
      If None, a random symbol will be chosen from the available list.

    Returns:
    - None: If the symbol is selected successfully or an error is raised.

    Raises:
    - ValueError: If the specified symbol is not found in the list of available symbols.
    - AssertionError: If the selected symbol does not match the desired symbol.
    """
    try:
        
        # Load available symbols for the given platform, client, and symbol type
        symbols = read_symbol_file(server, client_name, symbol_type)
        
        # If no specific symbol is given, randomly select one
        if desired_symbol_name is None:
            desired_symbol_name = random.choice(symbols)
        else:
            # Check if the desired symbol is in the available symbols list
            if desired_symbol_name not in symbols:
                raise ValueError(f"The desired symbol '{desired_symbol_name}' is not in the list of available symbols.")
            
        # Find the search input field for symbols
        search_input = visibility_of_element_by_testid(driver, data_testid="symbol-input-search")
        
        # Enter the selected symbol into the search input
        populate_element(element=search_input, text=desired_symbol_name)

        # Find and click the dropdown option that matches the desired symbol
        dropdown = visibility_of_element_by_xpath(driver, f"//div[contains(@data-testid, 'symbol-input-search-items')]//div[normalize-space(text())='{desired_symbol_name}']")
        click_element_with_wait(driver, element=dropdown)

        # Verify that the correct symbol has been selected by checking the chart symbol
        chart_symbol_name = wait_for_text_to_be_present_in_element_by_testid(driver, data_testid="symbol-overview-id", text=desired_symbol_name)
        
        # If the symbol is correctly shown, return success
        if chart_symbol_name:
            # assert True
            return desired_symbol_name
        else:
            # If the symbol name does not match, log an error
            chart_symbolName = get_chart_symbol_name(driver)
            assert False, f"Invalid Symbol Name: {chart_symbolName}"
            
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
        


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SEARCH FUNCTION (EXACT / WILDCARD SEARCH)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def perform_search(driver, input_search):
        # Find the search input field for symbols
        search_input = visibility_of_element_by_testid(driver, data_testid="symbol-input-search")
        click_element(element=search_input)
        
        if is_element_present_by_testid(driver, data_testid="symbol-input-search-history-delete"):
            btn_bin = visibility_of_element_by_testid(driver, "symbol-input-search-history-delete")
            click_element_with_wait(driver, element=btn_bin)

        clear_input_field(element=search_input)

        # Enter the first few characters of the selected symbol into the search input
        populate_element(element=search_input, text=input_search)
        
        spinner_element(driver)

        delay(2.5)
        
        # Wait for search results
        if is_element_present_by_testid(driver, data_testid="symbol-input-search-items"):
            search_results = find_list_of_elements_by_testid(driver, data_testid="symbol-input-search-items")
            print("Total row found", len(search_results))
            matched_rows = []
            for result in search_results:
                text = result.text  # Remove parentheses
                if input_search in text:
                    matched_rows.append(text)

            # Print results or raise an error if no match is found
            if matched_rows:
                # print(f"✅ Matching rows found for '{input_search}': {matched_rows}")
                print(f"✅ Matching rows found for '{input_search}':\n" + "\n".join(matched_rows))
            else:
                raise AssertionError(f"No matching row found for symbol: {input_search}")
        else:
            no_items_message = visibility_of_element_by_xpath(driver, "//*[contains(text(), 'Type something to search')]")
            msg = get_label_of_element(no_items_message)
            raise AssertionError(f"No matching row found for symbol: {input_search} with message: {msg}")


def symbol_search_feature(driver, server: str, client_name: str, symbol_type: str = "Symbols", desired_symbol_name: str = None):
    try:
        # Load available symbols for the given platform, client, and symbol type
        symbols = read_symbol_file(server, client_name, symbol_type)

        # If no specific symbol is given, randomly select one
        if desired_symbol_name is None:
            desired_symbol_name = random.choice(symbols)
        else:
            # Check if the desired symbol is in the available symbols list
            if desired_symbol_name not in symbols:
                raise ValueError(f"The desired symbol '{desired_symbol_name}' is not in the list of available symbols.")
        
        # Perform an exact match search (full symbol)
        perform_search(driver, input_search=desired_symbol_name)
        
        # Perform a wildcard match search (first two letters)
        perform_search(driver, input_search=desired_symbol_name[:2])

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CLEAR SEARCH HISTORY
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def clear_search_history(driver):

    def get_delete_buttons():
        return find_list_of_elements_by_testid(driver, "symbol-input-search-items-delete")

    def get_symbol_name(delete_button):
        container = delete_button.find_element(By.XPATH, ".//ancestor::div[@data-testid='symbol-input-search-items']")
        symbol_element = container.find_element(By.XPATH, ".//span[@data-testid='symbol-input-search-items-symbol']")
        return get_label_of_element(element=symbol_element).strip()

    def log_symbols(message, buttons):
        print(message)
        symbols = [get_symbol_name(btn) for btn in buttons]
        for idx, name in enumerate(symbols):
            print(f"Index {idx}: {name}")

    def delete_random_item(initial_count):
        delete_buttons = get_delete_buttons()
        selected_index = random.randint(0, len(delete_buttons) - 1)
        selected_symbol = get_symbol_name(delete_buttons[selected_index])
        print(f"Deleting symbol: (Index {selected_index}): {selected_symbol}")
        click_element_with_wait(driver, element=delete_buttons[selected_index])
        delay(1)

        updated_count = len(get_delete_buttons())
        if updated_count != initial_count - 1:
            raise AssertionError(f"Items remaining: {updated_count} (Expected {initial_count - 1})")
    try:
        spinner_element(driver)
        
        search_input = visibility_of_element_by_testid(driver, "symbol-input-search")
        click_element_with_wait(driver, element=search_input)

        # Initial state check
        initial_buttons = get_delete_buttons()
        initial_count = len(initial_buttons)
        if initial_count == 0:
            raise AssertionError("No search history items found")

        # Delete single random item
        print(f"\nInitial count: {initial_count}")
        log_symbols("Available symbols before deletion:", initial_buttons)
        delete_random_item(initial_count)

        # Clear remaining history
        remaining_buttons = get_delete_buttons()
        log_symbols("\nRemaining symbols before full clear:", remaining_buttons)
        btn_bin = find_element_by_testid(driver, "symbol-input-search-history-delete")
        click_element_with_wait(driver, element=btn_bin)
        delay(1)

        # Final verification
        final_count = len(get_delete_buttons())
        if final_count != 0:
            raise AssertionError(f"Clear all failed - Remaining items: {final_count}")

    except Exception as e:
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""