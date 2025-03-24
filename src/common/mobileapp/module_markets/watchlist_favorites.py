import random
from selenium.webdriver.common.by import By

from constants.helper.error_handler import handle_exception
from constants.helper.element import spinner_element, find_list_of_elements_by_xpath, find_list_of_elements_by_testid, click_element



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TOGGLE SYMBOL TO FAV / UNFAVOURITE STAR
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def toggle_symbol_favorite_status(driver):
    try:
        def get_watchlist_options(exclude="Favourites"):
            """Retrieve watchlist options, excluding a specific category."""
            options = find_list_of_elements_by_xpath(driver, "//div[@data-testid='watchlist-tabs']/div")
            
            if not options:
                assert False, "No categories found"
            return [option for option in options if option.text != exclude], next((option for option in options if option.text == exclude), None)

        def verify_symbol_in_favourites(symbol_name, should_exist):
            """Verify if a symbol is present or absent in the Favourites tab."""
            print("Switching to 'Favourites' tab.")
            click_element(element=favourites_tab)
            spinner_element(driver)
            favourites_symbols = find_list_of_elements_by_testid(driver, "watchlist-symbol")
            favourite_symbol_names = [element.text.strip() for element in favourites_symbols]
            if should_exist:
                print(f"Symbol '{symbol_name}' is found in Favourites tab")
                assert symbol_name in favourite_symbol_names, f"Symbol '{symbol_name}' not found in Favourites."
            else:
                print(f"Symbol '{symbol_name}' no longer found in Favourites tab")
                assert symbol_name not in favourite_symbol_names, f"Symbol '{symbol_name}' is still in Favourites."
        
        def toggle_star_icon(star_icon):
            """Toggle a star icon (favorite/unfavorite) and return the symbol name."""
            # To find the parent div class for the "star_icon"
            symbol_container = star_icon.find_element(By.XPATH, ".//ancestor::div[@data-testid='watchlist-list-item']")
            # To find the symbol name that is being fav/unfavourite
            symbol_name_element = symbol_container.find_element(By.XPATH, ".//div[@data-testid='watchlist-symbol']")
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
        unfavourite_star_icons = find_list_of_elements_by_testid(driver, data_testid="watchlist-star-unwatch")
        if not unfavourite_star_icons:
            assert False, f"No unfavorited symbols found in the selected category: '{selected_category}'."
            
        symbol_name_to_favorite = toggle_star_icon(random.choice(unfavourite_star_icons))
        print(f"Star for symbol '{symbol_name_to_favorite}' is favourite.")
        verify_symbol_in_favourites(symbol_name_to_favorite, should_exist=True)

        # Step 3: Remove a symbol from Favourites
        print("\nPart 2: Removing a symbol from 'Favourites'")
        favourite_star_icons = find_list_of_elements_by_testid(driver, data_testid="watchlist-star-watch")
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