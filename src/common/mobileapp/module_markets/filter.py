import re
import random

from enums.main import Menu
from constants.element_ids import DataTestID

from constants.helper.driver import delay
from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element_android_app import find_element_by_testid, find_element_by_xpath_with_wait, find_presence_element_by_testid, get_label_of_element, scroll_horizontally_right_scrollview, spinner_element, is_element_present_by_xpath, find_element_by_xpath, find_list_of_elements_by_xpath, click_element, wait_for_text_to_be_present_in_element_by_testid, wait_for_text_to_be_present_in_element_by_xpath

from common.mobileapp.module_sub_menu.utils import menu_button



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                WATCHLIST - SYMBOL NAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def navigate_and_select_watchlist_symbol(driver):
    """
    Selects a category from the watchlist in Home page and clicks a randomly selected symbol from that category.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    
    try:
        # Randomly select a tab option        
        watchlist_tab_options = find_list_of_elements_by_xpath(driver, DataTestID.APP_WATCHLIST_TABS)
        if not watchlist_tab_options:
             assert False, "No categories found"
        
        # Randomly select a category from the watchlist
        random_category = random.choice(watchlist_tab_options)
        selected_option = get_label_of_element(random_category)
        print(f"Selected category: {selected_option}")
        click_element(element=random_category)
        
        # Handle case where the selected category is "Favourites" but contains no items
        if selected_option == "Favourites":
            if is_element_present_by_xpath(driver, DataTestID.APP_MSG_NO_ITEMS_AVAILABLE):
                # Exclude the "Favourites" category and select a new category randomly
                filtered_options = [category for category in watchlist_tab_options if category.text.strip() != "Favourites"]
                
                if filtered_options:  # Ensure there are available options
                    random_category = random.choice(filtered_options)
                    selected_option = get_label_of_element(random_category)
                    print(f"No items found in Favourites, selecting another category: {selected_option}")
                    click_element(element=random_category)
        
        # Wait for spinner/loading animation to disappear
        spinner_element(driver)
        
        # Retrieve all symbols available in the selected category
        symbols = find_list_of_elements_by_xpath(driver, DataTestID.APP_WATCHLIST_SYMBOL)
        if not symbols:
            assert False, f"No symbols found in the selected category: {selected_option}"
        
        # Randomly select a symbol and click on it
        random_symbol = random.choice(symbols)
        label_symbol = get_label_of_element(random_symbol)
        # label_symbol = random_symbol.text  # Get the symbol's name/text
        attach_text("Selected Symbol is: " + label_symbol, name="Market Watchlist Section")
        click_element(random_symbol)  # Click on the selected symbol

        # Verify if the correct symbol is displayed in the chart (ensuring the click was successful)
        chart_symbol_name = wait_for_text_to_be_present_in_element_by_testid(driver, data_testid=DataTestID.SYMBOL_OVERVIEW_ID, text=label_symbol)

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
                                                WATCHLIST - FILTER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def handle_alert_success(driver):
    """
    This function handles the expected login error scenario by checking for the error notification 
    and extracting the error message. It then attaches the error message for logging or reporting purposes.

    Returns:
    - success_message: The error message text extracted from the login failure notification.
    """
    spinner_element(driver)
    
    # Retrieve the error message notification
    message_notification = find_presence_element_by_testid(driver, data_testid=DataTestID.NOTIFICATION_BOX_DESCRIPTION)
    
    # Extract the text (label) of the error message from the notification element.
    label_message = get_label_of_element(element=message_notification)
    
    # Attach the extracted error message to the logs for reporting purposes.
    attach_text(label_message, name="Message:")
    
    btn_close = find_element_by_testid(driver, data_testid=DataTestID.NOTIFICATION_BOX_CLOSE)
    click_element(element=btn_close)
    
    return label_message
    
    
def select_category_from_watchlist(driver, selected_category_text, max_scroll_attempts=2):
    """
    Selects a category from the watchlist by scrolling horizontally if needed.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        selected_category_text (str): The category to select from the watchlist.
        max_scroll_attempts (int): The maximum number of scroll attempts (default is 2).

    Returns:
        bool: True if the category is found and selected, False otherwise.
    """
    for attempt in range(max_scroll_attempts):
        # Retrieve watchlist options
        watchlist_options = find_list_of_elements_by_xpath(driver, DataTestID.APP_WATCHLIST_TABS)
        print(f"Attempt {attempt + 1} - Number of options: {len(watchlist_options)}")

        # Search for the selected category
        for option in watchlist_options:
            label = get_label_of_element(element=option)
            print(f"Found option: {label}")

            if label == selected_category_text:
                click_element(element=option)
                print(f"Clicked '{selected_category_text}'")
                return True  # Exit function once found and clicked

        # Scroll if the option wasn't found and more attempts remain
        if attempt < max_scroll_attempts:
            print("Category not found, scrolling...")
            scroll_horizontally_right_scrollview(driver)

    print(f"Category '{selected_category_text}' not found after {max_scroll_attempts} scrolls.")
    return False



def market_watchlist_filter(driver):
    try:
        # Redirect to the Markets page
        menu_button(driver, menu=Menu.MARKET)
        
        delay(0.5)
        
        # Click on the filter icon
        filter = find_element_by_xpath_with_wait(driver, DataTestID.APP_SYMBOL_PREFERENCE)
        click_element(element=filter)
        
        # Wait for the "Show/Hide Symbol" modal to appear
        result = wait_for_text_to_be_present_in_element_by_xpath(driver, DataTestID.APP_SYMBOL_PREFERENCE_LABEL, text="Show/Hide Symbol")
        if not result:
            raise AssertionError("Show/Hide Symbol not found")
        
        delay(1)

        # Find the list of category tabs (Shares, Forex, Index, Commodities, Crypto, etc.)
        selected_option = find_list_of_elements_by_xpath(driver, DataTestID.APP_SYMBOL_PREFERENCE_TABS)

        # Check if any categories are found
        if not selected_option:
            raise Exception("No categories found")  # Raise a more specific exception if no elements are found

        # Exclude categories with an excessive number of symbols to reduce extraction time.
        exclude_categories = {'Shares', 'Forex', 'All'}

        # Filter the list to exclude specific categories
        filtered_options = [
            option for option in selected_option 
            if get_label_of_element(option) not in exclude_categories
        ]

        # Ensure there are remaining options after filtering
        if not filtered_options:
            raise Exception("No valid categories found after filtering Shares and Index")

        # Randomly choose one category from the filtered list
        random_category = random.choice(filtered_options)

        # Retrieve the label of the selected category
        selected_category_text = get_label_of_element(random_category)
        print(f"Selected category: {selected_category_text}")

        # Click the selected category to navigate
        click_element(random_category)
        
        # Check if the unchecked checkbox is found, and click it if available
        if is_element_present_by_xpath(driver, DataTestID.APP_SYMBOL_PREFERENCE_OPTION_SHOW_ALL_UNCHECKED):
            showall_unchecked_checkboxes = find_element_by_xpath(driver, DataTestID.APP_SYMBOL_PREFERENCE_OPTION_SHOW_ALL_UNCHECKED)
            click_element(showall_unchecked_checkboxes)
        else:   # If the unchecked checkbox is not found, check for the checked one and click it
            showall_checked_checkboxes = find_element_by_xpath(driver, DataTestID.APP_SYMBOL_PREFERENCE_OPTION_SHOW_ALL_CHECKED)
            click_element(element=showall_checked_checkboxes)
        
        # Locate all checkboxes (both checked and unchecked)
        unchecked_checkboxes = find_list_of_elements_by_xpath(driver, DataTestID.APP_SYMBOL_PREFERENCE_OPTION_UNCHECKED)
        checked_checkboxes = find_list_of_elements_by_xpath(driver, DataTestID.APP_SYMBOL_PREFERENCE_OPTION_CHECKED)
        # Combine both unchecked and checked checkboxes into a list
        all_checkboxes = unchecked_checkboxes + checked_checkboxes
        
        if not all_checkboxes:
            raise Exception("No checkboxes found!")
        
        # # Choose a random checkbox from the combined list
        random_checkbox = random.choice(all_checkboxes)

        # The code checks whether the randomly selected checkbox is part of the unchecked list:
        if random_checkbox in unchecked_checkboxes: # If the checkbox is originally unchecked
            # Check the checkbox
            click_element(element=random_checkbox)
            action = "checked"
            expected_symbol_visibility = True  # If checked, the symbol should be visible
        else: # If the checkbox is originally checked
            click_element(element=random_checkbox)
            action = "unchecked"
            expected_symbol_visibility = False  # If unchecked, the symbol should not be visible
        
        # Get the correct parent using XPath position
        symbol_name = find_element_by_xpath(driver, f"({DataTestID.APP_SYMBOL_PREFERENCE_OPTION_CHECKED} | {DataTestID.APP_SYMBOL_PREFERENCE_OPTION_UNCHECKED})[{all_checkboxes.index(random_checkbox) + 1}]/parent::*")
        label_symbol_name = get_label_of_element(element=symbol_name)  # Extract and clean up the text
        filter_symbol_name = re.search(r'\b[A-Z]+[A-Z0-9]*\.std\b', label_symbol_name).group()
        
        # Remain as current, no change to symbol
        filter_symbol_list = [filter_symbol_name]
        
        # Print the action taken and symbol name
        print(f"Checkbox for symbol '{filter_symbol_name}' {action}.")

        # Save changes
        save_button = find_element_by_xpath(driver, DataTestID.APP_SYMBOL_PREFERENCE_SAVE)
        click_element(element=save_button)

        alert_msg = handle_alert_success(driver)
        if alert_msg != "All changes are saved.":
            raise AssertionError(f"Receive {alert_msg} instead of the expected message")

        select_category_from_watchlist(driver, selected_category_text, max_scroll_attempts=2)
        
        delay(1)
        
        market_symbol_name = find_list_of_elements_by_xpath(driver, DataTestID.APP_MARKET_WATCHLIST_SYMBOL_NAME)
        
        data_loaded = set()  # To store unique data items
        
        for name in market_symbol_name:
            label_symbol_name = get_label_of_element(element=name)
            data_loaded.add(label_symbol_name)
            print(label_symbol_name)
            
        print("Market watchlist data:", data_loaded)  
        print("Filtered symbol list:", filter_symbol_list)

        # If checkbox was checked, expect the symbols to be displayed
        if expected_symbol_visibility:
            missing_symbols = set(filter_symbol_list) - set(data_loaded)
            if missing_symbols:
                assert False, f"Missing symbols from market watchlist (should be visible): {', '.join(missing_symbols)}"
            else:
                print(f"Symbols from filter_symbol_list {filter_symbol_list} are correctly displayed in the market watchlist.")
            
        # If checkbox was unchecked, expect the symbols to be hidden
        else:
            extra_symbols = set(filter_symbol_list) & set(data_loaded)
            if extra_symbols:
                assert False, f"Unexpected visible symbols in market watchlist (should be hidden): {', '.join(extra_symbols)}"
            else:
                print(f"No unexpected symbols {filter_symbol_list} visible, as expected.")
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""