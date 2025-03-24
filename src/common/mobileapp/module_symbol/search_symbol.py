import random
from selenium.webdriver.common.by import By

from enums.main import Server, SymbolsList
from constants.element_ids import DataTestID

from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception
from constants.helper.element_android_app import clear_input_field, click_element, click_element_with_wait, find_element_by_testid, find_element_by_testid_with_wait, find_element_by_xpath, find_element_by_xpath_with_wait, find_list_of_elements_by_xpath, is_element_present_by_testid, is_element_present_by_xpath, populate_element, find_list_of_elements_by_testid, spinner_element, find_visible_element_by_xpath, find_visible_element_by_testid, wait_for_text_to_be_present_in_element_by_testid, get_label_of_element

from data_config.file_handler import read_symbol_file
from common.desktop.module_chart.chart import get_chart_symbol_name


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                INPUT SYMBOL
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def input_symbol(driver, server: Server, symbol_type: SymbolsList = SymbolsList.SYMBOLS, desired_symbol_name: str = None):
    """
    The function interacts with the server's symbol search input field, selects the desired symbol 
    from a dropdown, and verifies that the correct symbol is shown in the chart.
    
    Arguments:
    - Server: The server from which to load symbols (e.g., 'MT4', 'MT5').
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
        
        # Load available symbols for the given server and symbol type
        symbols = read_symbol_file(server, symbol_type)
        
        # If no specific symbol is given, randomly select one
        if desired_symbol_name is None:
            desired_symbol_name = random.choice(symbols)
        else:
            # Check if the desired symbol is in the available symbols list
            if desired_symbol_name not in symbols:
                raise ValueError(f"The desired symbol '{desired_symbol_name}' is not in the list of available symbols.")
        
        # Find the search input field for symbols
        btn_search = find_element_by_testid_with_wait(driver, data_testid=DataTestID.SYMBOL_SEARCH_SELECTOR)
        click_element(element=btn_search)
        
        # Search for symbol
        input_search = find_element_by_testid_with_wait(driver, data_testid=DataTestID.SYMBOL_INPUT_SEARCH)
        click_element(element=input_search)

        # Enter the selected symbol into the search input
        populate_element(element=input_search, text=desired_symbol_name)
        
        # Wait for spinner to be invisible
        spinner_element(driver)
        
        # Find and click the dropdown option that matches the desired symbol            
        dropdown_options = find_list_of_elements_by_xpath(driver, DataTestID.APP_SYMBOL_NAME_DROPDOWN_RESULT)
        for option in dropdown_options:
            if (get_label_of_element(option)) == desired_symbol_name:
                click_element(option)
                break

        # Verify that the correct symbol has been selected by checking the chart symbol
        if wait_for_text_to_be_present_in_element_by_testid(driver, data_testid=DataTestID.SYMBOL_OVERVIEW_ID, text=desired_symbol_name):
            # If the symbol is correctly shown, return success
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

def search_symbol_variations(driver, server: Server, symbol_type: SymbolsList = SymbolsList.SYMBOLS, desired_symbol_name: str = None):
    try:
        # Load available symbols for the given server and symbol type
        symbols = read_symbol_file(server, symbol_type)
        
        # If no specific symbol is given, randomly select one
        if desired_symbol_name is None:
            desired_symbol_name = random.choice(symbols)
        else:
            # Check if the desired symbol is in the available symbols list
            if desired_symbol_name not in symbols:
                raise ValueError(f"The desired symbol '{desired_symbol_name}' is not in the list of available symbols.")
        
        for index, input_search in enumerate([desired_symbol_name, desired_symbol_name[:2]]):
            if index == 0:
                # Find the search input field for symbols only on the first search
                btn_search = find_element_by_testid_with_wait(driver, data_testid=DataTestID.SYMBOL_SEARCH_SELECTOR)
                click_element(element=btn_search)
            
            # Search for symbol
            input_search_field = find_element_by_testid_with_wait(driver, data_testid=DataTestID.SYMBOL_INPUT_SEARCH)
            click_element(element=input_search_field)
            clear_input_field(element=input_search_field)
            
            # Enter search term
            populate_element(element=input_search_field, text=input_search)
            spinner_element(driver)
            
            # Wait for search results
            if is_element_present_by_xpath(driver, DataTestID.APP_WATCHLIST_LIST_ITEM):
                search_results = find_list_of_elements_by_xpath(driver, DataTestID.APP_WATCHLIST_LIST_ITEM)
                print("Total row found", len(search_results))
                matched_rows = [get_label_of_element(result) for result in search_results if input_search in get_label_of_element(result)]
                
                if matched_rows:
                    print(f"✅ Matching rows found for '{input_search}':\n" + "\n".join(matched_rows))
                else:
                    raise AssertionError(f"No matching row found for symbol: {input_search}")
            else:
                no_items_message = find_visible_element_by_xpath(driver, "//*[contains(text(), 'Type something to search')]")
                msg = get_label_of_element(no_items_message)
                raise AssertionError(f"No matching row found for symbol: {input_search} with message: {msg}")
    
    except Exception as e:
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
    try:
        
        # Click on the search inspector
        btn_search = find_element_by_testid_with_wait(driver, data_testid=DataTestID.SYMBOL_SEARCH_SELECTOR)
        click_element(element=btn_search)
        
        btn_delete = find_element_by_xpath_with_wait(driver, DataTestID.APP_SYMBOL_INPUT_SEARCH_HISTORY_DELETE)
        click_element(element=btn_delete)
        
        # Verify search history is cleared
        if not is_element_present_by_xpath(driver, DataTestID.APP_SEARCH_HISTORY_LABEL):
            raise AssertionError("Expected Search History to be hidden")
        
        print("Element not present")

    except Exception as e:
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""