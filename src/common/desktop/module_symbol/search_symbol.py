import random

from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element_with_wait, find_element_by_xpath, populate_element, visibility_of_element_by_xpath, visibility_of_element_by_testid, wait_for_text_to_be_present_in_element_by_testid
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


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SYMBOL WATCHLIST
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
def symbol_watchlist(driver, tab_title: str):
    """
    The function is responsible for clicking on a tab in the symbol watchlist based on the title provided. 
    It handles any exceptions that may occur during the process, such as failing to find the tab or encountering issues with the click action.
   
    Arguments:
    - tab_title: The title of the tab to select in the symbol watchlist (e.g., 'All', 'Favourites', 'Top Picks', 'Top Gainer', 'Top Loser').

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
 """
    try:
        # Find the tab element using the provided tab title 
        watchlist = find_element_by_xpath(driver, f"//div[normalize-space()='{tab_title}']")
        # Click the tab and wait for the action to be completed
        click_element_with_wait(driver, element=watchlist)
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""