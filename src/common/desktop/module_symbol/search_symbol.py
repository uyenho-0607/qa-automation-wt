import random

from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element_with_wait, find_element_by_xpath, populate_element_with_wait, visibility_of_element_by_xpath, visibility_of_element_by_testid, wait_for_text_to_be_present_in_element_by_testid
from data_config.fileHandler import read_symbol_file
from common.desktop.module_chart.chart import get_chart_symbol_name



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                INPUT SYMBOL
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def input_symbol(driver, platform, client_name, symbol_type="Symbols", desired_symbol_name=None):

    try:
        
        # Load symbols for the specified platform, client, and symbol type
        symbols = read_symbol_file(platform, client_name, symbol_type)
        
        # If a specific symbol is provided, use it; otherwise, select a random one
        if desired_symbol_name is None:
            desired_symbol_name = random.choice(symbols)
        else:
            # Check if the desired symbol is in the list of symbols
            if desired_symbol_name not in symbols:
                raise ValueError(f"The desired symbol '{desired_symbol_name}' is not in the list of available symbols.")
            
        # Find the search input element
        search_input = visibility_of_element_by_testid(driver, data_testid="symbol-input-search")
        
        # Enter the random symbol into the search input
        populate_element_with_wait(driver, element=search_input, text=desired_symbol_name)

        # Find the dropdown option corresponding to the symbol
        dropdown = visibility_of_element_by_xpath(driver, f"//div[contains(@data-testid, 'symbol-input-search-items')]//div[normalize-space(text())='{desired_symbol_name}']")
        click_element_with_wait(driver, element=dropdown)

        # Verify the symbol has been selected correctly
        chart_symbol_name = wait_for_text_to_be_present_in_element_by_testid(driver, data_testid="symbol-overview-id", text=desired_symbol_name)
        
        # If the correct symbol is shown, return successfully
        if chart_symbol_name:
            assert True
            return
        else:
            chart_symbolName = get_chart_symbol_name(driver)
            assert False, f"Invalid Symbol Name: {chart_symbolName}"
    
    except Exception as e:
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
def symbol_watchlist(driver, tab_title):
    try:
        watchlist = find_element_by_xpath(driver, f"//div[normalize-space()='{tab_title}']")
        click_element_with_wait(driver, element=watchlist)
    except Exception as e:
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""