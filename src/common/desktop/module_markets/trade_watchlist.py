import random
from selenium.webdriver.common.by import By


from constants.helper.driver import delay
from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element import spinner_element, get_label_of_element, visibility_of_element_by_xpath, find_element_by_xpath, find_list_of_elements_by_xpath, click_element, wait_for_text_to_be_present_in_element_by_testid



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SYMBOL WATCHLIST
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
   
def select_trade_symbol_from_watchlist(driver, excluded_tabs=None):
    """
    The function is responsible for clicking on a tab in the symbol watchlist based on the title provided. 
    It handles any exceptions that may occur during the process, such as failing to find the tab or encountering issues with the click action.

    Args:
    - driver: Selenium WebDriver instance.
    - excluded_tabs: A set of tab names to exclude from selection during recursive calls.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Initialize excluded_tabs if not provided
        if excluded_tabs is None:
            excluded_tabs = set()

        # Find the tab elements using the provided XPath
        watchlist_options = find_list_of_elements_by_xpath(driver, "(//div[@class='sc-jekbnu-2 dKFAqJ'])[1]/div")
        available_tabs = [tab for tab in watchlist_options if tab.text not in excluded_tabs]

        if available_tabs:
            # Randomly select a category from available tabs
            random_category = random.choice(available_tabs)
            selected_category_text = random_category.text
            print(f"Selected category: {selected_category_text}")
            click_element(element=random_category)
        else:
            assert False, "No categories available for selection"
        
        # Add the selected category to the exclusion set
        excluded_tabs.add(selected_category_text)

        # Wait briefly to ensure the tab content loads
        delay(1)
        
        # Locate all symbols in the selected category
        symbols = find_list_of_elements_by_xpath(driver, "//div[@class='sc-iubs14-5 fFEJmt']")
        if symbols:
            random_symbol = random.choice(symbols)  # Randomly choose one symbol from the list
            label_symbol = random_symbol.text  # Get the symbol's name/text
            attach_text("Selected Symbol is: " + label_symbol, name="Trade Watchlist Section")
            click_element(random_symbol)  # Click on the selected symbol
        else:
            # Check for "No items found" message
            no_items_message = visibility_of_element_by_xpath(driver, "//div[@class='sc-gl6kw9-0 kqmkWT']")
            msg = get_label_of_element(no_items_message)
            print(f"Message displayed: {msg}")
            
            if selected_category_text.lower() == "favourites":
                print("No symbols found in 'Favourites'. Selecting a different tab...")
                return select_trade_symbol_from_watchlist(driver, excluded_tabs)  # Recursive call to try another tab
            
            # Raise an error if no symbols were found for non-Favourites categories
            raise AssertionError(f"The message '{msg}' was displayed after selecting '{selected_category_text}' tab")

        # Verify if the correct symbol is displayed in the chart (ensuring the click was successful)
        chart_symbol_name = wait_for_text_to_be_present_in_element_by_testid(driver, data_testid="symbol-overview-id", text=label_symbol)
        
        # Assert that the symbol in the chart matches the selected symbol
        assert chart_symbol_name, f"Chart symbol mismatch: expected '{label_symbol}', found '{chart_symbol_name}'"
    
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

     
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TOGGLE SYMBOL TO FAV / UNFAVOURITE STAR
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def toggle_symbol_favorite_status(driver):
    try:
        def get_watchlist_options(exclude="Favourites"):
            """Retrieve watchlist options, excluding a specific category."""
            options = find_list_of_elements_by_xpath(driver, "(//div[@class='sc-jekbnu-2 dKFAqJ'])[1]/div")
            if not options:
                assert False, "No categories found"
            return [option for option in options if option.text != exclude], next((option for option in options if option.text == exclude), None)

        def verify_symbol_in_favourites(symbol_name, should_exist):
            """Verify if a symbol is present or absent in the Favourites tab."""
            print("Switching to 'Favourites' tab.")
            click_element(element=favourites_tab)
            spinner_element(driver)
            favourites_symbols = find_list_of_elements_by_xpath(driver, "//div[contains(@class, 'fFEJmt')]")
            favourite_symbol_names = [element.text.strip() for element in favourites_symbols]
            if should_exist:
                print(f"Symbol '{symbol_name}' is found in Favourites tab")
                assert symbol_name in favourite_symbol_names, f"Symbol '{symbol_name}' not found in Favourites."
            else:
                print(f"Symbol '{symbol_name}' no longer found in Favourites tab")
                assert symbol_name not in favourite_symbol_names, f"Symbol '{symbol_name}' is still in Favourites."

        def toggle_star_icon(star_icon):
            """Toggle a star icon (favorite/unfavorite) and return the symbol name."""
            symbol_container = star_icon.find_element(By.XPATH, "./ancestor::div[contains(@class, 'sc-iubs14')]")
            symbol_name_element = symbol_container.find_element(By.XPATH, ".//div[contains(@class, 'fFEJmt')]")
            symbol_name = symbol_name_element.text.strip()
            click_element(element=star_icon)
            return symbol_name

        def select_random_category(categories):
            """Randomly select and click on a category tab, then return its name."""
            random_category = random.choice(categories)
            category_name = random_category.text.strip()
            print(f"Switching to category: '{category_name}'.")
            click_element(element=random_category)
            spinner_element(driver)
            return category_name

        # Step 1: Get watchlist options and the Favourites tab
        filtered_options, favourites_tab = get_watchlist_options()
        if not filtered_options:
            assert False, "No categories available after filtering out 'Favourites'."
        if not favourites_tab:
            assert False, "'Favourites' tab not found."

        # Step 2: Add a symbol to Favourites
        print("Part 1: Adding a symbol to 'Favourites'")
        selected_category = select_random_category(filtered_options)

        unfavourite_star_icons = find_list_of_elements_by_xpath(driver, "//div[@class='sc-1tkgbp9-0 hwMknn']")
        if not unfavourite_star_icons:
            assert False, f"No unfavorited symbols found in the selected category: '{selected_category}'."
            
        symbol_name_to_favorite = toggle_star_icon(random.choice(unfavourite_star_icons))
        print(f"Star for symbol '{symbol_name_to_favorite}' is favourite.")
        verify_symbol_in_favourites(symbol_name_to_favorite, should_exist=True)

        # Step 3: Remove a symbol from Favourites
        print("\nPart 2: Removing a symbol from 'Favourites'")
        favourite_star_icons = find_list_of_elements_by_xpath(driver, "//div[@class='sc-1tkgbp9-0 kLQFAh']")
        if not favourite_star_icons:
            assert False, "No favorite symbols available to unfavourite."
        symbol_name_to_unfavorite = toggle_star_icon(random.choice(favourite_star_icons))
        print(f"Star for symbol '{symbol_name_to_unfavorite}' is unfavourite.")

        # Step 4: Verify symbol is removed from Favourites
        selected_category = select_random_category(filtered_options)
        verify_symbol_in_favourites(symbol_name_to_unfavorite, should_exist=False)

    except Exception as e:
        handle_exception(driver, e)
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                VERIFY THE PRE-SELECTED TAB IS CORRECT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_pre_selected_tab(driver):
    try:
        # Determine which tab is currently selected
        watchlist_options = find_list_of_elements_by_xpath(driver, "(//div[@class='sc-jekbnu-2 dKFAqJ'])[1]/div")
        selected_tab_text = None

        if watchlist_options:  # Ensure the list is not empty
            for option in watchlist_options:
                if "selected" in option.get_attribute("class"):
                    selected_tab_text = option.text.strip()  # Get the text of the selected option
                    print(f"Selected option text: {selected_tab_text}")
                    break

        if not selected_tab_text:
            assert False, "No pre-selected tab found."

        if selected_tab_text == "Favourites":
            # Check if there are symbols in the Favourites tab
            symbols = find_list_of_elements_by_xpath(driver, "//div[contains(@class, 'fFEJmt')]")
            if symbols:
                print("Favourites tab has symbols.")
            else:
                assert False, "Favourites tab is pre-selected but has no symbols."

        elif selected_tab_text == "Top Gainer":
            print("Top Gainers tab is pre-selected.")
            # Switch to the Favourites tab to verify it does not have symbols
            favourites_tab = find_element_by_xpath(driver, "//div[text()='Favourites']")
            if favourites_tab:
                favourites_tab.click()
                symbols_in_favourites = find_list_of_elements_by_xpath(driver, "//div[contains(@class, 'fFEJmt')]")
                if symbols_in_favourites:
                    assert False, "Top Gainer is pre-selected but Favourites tab has symbols."
                else:           
                    # Verify and capture the message displayed in the Favourites tab
                    no_items_message = visibility_of_element_by_xpath(driver, "//div[@class='sc-gl6kw9-0 kqmkWT']")
                    msg = get_label_of_element(no_items_message)
                    print(f"Verified that the Favourites tab contains no symbols. Message displayed: {msg}")
        else:
            assert False, f"Unexpected pre-selected tab: {selected_tab_text}"

    except Exception as e:
        handle_exception(driver, e)
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""