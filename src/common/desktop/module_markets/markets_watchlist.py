import random

from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element import spinner_element, visibility_of_element_by_xpath, find_list_of_elements_by_xpath, click_element, wait_for_text_to_be_present_in_element_by_testid

from common.desktop.module_subMenu.utils import menu_button


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                WATCHLIST - SYMBOL NAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def market_watchlist(driver, options: str = None):
    """
    This function navigates to the 'Markets' page, selects a category from the watchlist,
    and clicks a randomly selected symbol from that category.

    Arguments:
    - options: The category to select from the watchlist (e.g., "Favourites", "Shares", etc.)
    
    Workflow:
    1. Navigate to the 'Markets' page.
    2. Select the desired watchlist category (or a random one if not provided).
    3. Wait for symbols to load, then select a random symbol.
    4. Click on the symbol and verify that the chart is updated with the correct symbol.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    
    # Define the options for each section in the watchlist
    available_options = ["Favourites", "Shares", "Forex", "Index", "Commodities", "Crypto", "All"]
    
    try:
        # Redirect to the Markets page
        menu_button(driver, menu="markets")
        
        # Wait till the spinner icon no longer display
        spinner_element(driver)
        
        # If no specific option is given, randomly select one from available options
        if options is None:
            selected_option = random.choice(available_options) # Randomly select an option
        elif options in available_options:
            selected_option = options # If the option is valid, use it
        else:
            # Raise an error if the selected option is invalid
            raise ValueError(f"Invalid option selected. Please choose a valid option from {available_options}")

        # Find and click the selected watchlist category option
        watchlist_option =  visibility_of_element_by_xpath(driver, f"//div[@class='sc-jekbnu-2 dKFAqJ']//div[text()='{selected_option}']")
        click_element(element=watchlist_option)
        
        # Wait till the spinner icon no longer display
        spinner_element(driver)
        
        # Locate all symbols in the selected category
        symbols = find_list_of_elements_by_xpath(driver, "//div[@class='sc-1cyjrzn-1 dIPaVz']//div[@class='sc-iubs14-5 fFEJmt']")
        if symbols:
            random_symbol = random.choice(symbols) # Randomly choose one symbol from the list
            label_symbol = random_symbol.text  # Get the symbol's name/text
            attach_text("Symbol selected is: " + label_symbol, name="Market Watchlist Section")
            click_element(random_symbol)  # Click on the selected symbol
        else:
            # Raise an error if no symbols were found
            raise ValueError("No symbols found")

        # Verify if the correct symbol is displayed in the chart (ensuring the click was successful)
        chart_symbol_name = wait_for_text_to_be_present_in_element_by_testid(driver, data_testid="symbol-overview-id", text=label_symbol)
        
        # Assert that the symbol in the chart matches the selected symbol
        assert chart_symbol_name, f"Chart symbol mismatch: expected '{label_symbol}', found '{chart_symbol_name}'"
    
        tab = visibility_of_element_by_xpath(driver, "//div[text()='All']")
            
        if tab:  # Ensure the tab is visible
            tab_text = tab.text
            if "selected" in tab.get_attribute("class"):
                attach_text(f"{tab_text} tab is pre-selected", name=f"Redirecting to the correct tab:")
                return
        else:
            raise ValueError(f"No pre-selected tab found from the specified tab options for ALL")

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                WATCHLIST - FILTER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def market_watchlist_filter(driver):
   
    try:
        # Redirect to the Markets page
        menu_button(driver, menu="markets")

        # Locate all symbols in the selected category
        filter = visibility_of_element_by_xpath(driver, "//div[@class='sc-jekbnu-3 QuCNL']")
        click_element(filter)  # Click on the selected symbol
        
        # Locate the symbol name
        symbol_name = find_list_of_elements_by_xpath(driver, "//div[@class='sc-1y7v0bd-0 fQRgGF']")
        click_element(symbol_name)  # Click on the selected symbol

        # Locate 'Save Changes' button
        close = visibility_of_element_by_xpath(driver, "//button[contains(normalize-space(text()), 'Save Changes')]")
        click_element(close)  # Click on the selected symbol

        # Locate 'X' button
        close = visibility_of_element_by_xpath(driver, "//div[@class='sc-ur24yu-4 jgnDww']")
        click_element(close)  # Click on the selected symbol

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
