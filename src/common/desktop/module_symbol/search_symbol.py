import random

from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element_with_wait, find_list_of_elements_by_xpath, populate_element, find_list_of_elements_by_testid, visibility_of_element_by_xpath, visibility_of_element_by_testid, wait_for_text_to_be_present_in_element_by_testid
from data_config.fileHandler import read_symbol_file
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
        
        
def clear_search_history(driver):
    try:
        
        # Find the search input field for symbols
        search_input = visibility_of_element_by_testid(driver, data_testid="symbol-input-search")
        click_element_with_wait(driver, element=search_input)
        
        # Locate the search history items and iterate through them
        search_history_items = find_list_of_elements_by_xpath(driver, "//div[@data-testid='symbol-input-search-items']//div[@class='sc-1jx9xug-5 gVqGuT']")
        
        # Locate all clear buttons (bin or x)
        clear_btns = find_list_of_elements_by_xpath(driver, "//div[@class='sc-1jx9xug-8 kXyyDI']")
        
        if clear_btns:
            # If there's more than one button (Delete All / Delete One)
            # Assuming the first button is always the "bin" (delete all) and subsequent ones are "x"
            for idx, clear_btn in enumerate(clear_btns):
                # If it's the first clear button, consider it as the bin (delete all)
                # if idx == 0:
                #     clear_btn.click()
                #     print("Cleared all search history.")
                #     break  # Exit after clicking the "bin" icon (delete all)
                # else:
                if idx >= 1:
                    # Click the "x" icon (delete specific item)
                    clear_btn.click()
                    symbol_name = search_history_items[idx].text  # Get the name of the symbol being deleted
                    print(f"Deleted search item: {symbol_name}")
        
        else:
            print("No clear buttons found in search history.")
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)


