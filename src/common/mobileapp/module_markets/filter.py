import random
from appium.webdriver.common.appiumby import AppiumBy

from constants.element_ids import DataTestID
from constants.helper.driver import delay
from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element_android_app import find_element_by_testid, find_element_by_xpath_with_wait, find_presence_element_by_testid, find_visible_element_by_xpath, get_label_of_element, spinner_element, find_visible_element_by_testid, is_element_present_by_xpath, is_element_present_by_testid, find_element_by_xpath, find_list_of_elements_by_xpath, click_element, wait_for_text_to_be_present_in_element_by_testid, wait_for_text_to_be_present_in_element_by_xpath

from common.mobileapp.module_sub_menu.utils import menu_button
from enums.main import Menu


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
    
    
    
    
    

def scroll_and_retrieve_data(driver):
    # Locate the scrollable div
    find_visible_element_by_testid(driver ,data_testid=DataTestID.WATCHLIST_LIST_ITEM)
    scrollable_div = find_element_by_xpath(driver, f"(//*[@data-testid='{DataTestID.WATCHLIST_LIST}']//div)[2]")
    
    # Store the current scroll height to detect when scrolling stops
    last_scroll_height = 0
    data_loaded = set()  # To store unique data items

    while True:
        # Scroll down by a small amount
        driver.execute_script("arguments[0].scrollBy(0, 200);", scrollable_div)
        
        delay(0.5)

        # Collect visible data (modify as needed for the content inside the div)
        rows = scrollable_div.find_elements(AppiumBy.XPATH, f"//*[@data-testid='{DataTestID.WATCHLIST_SYMBOL}']")  # Adjust for your row or item selector
        for row in rows:
            data_loaded.add(row.text.strip())  # Save row content or other unique data
        
        # Get the current scroll height
        current_scroll_height = driver.execute_script("return arguments[0].scrollTop;", scrollable_div)
        
        # Stop if the scroll height doesn't change
        if current_scroll_height == last_scroll_height:
            break
        
        last_scroll_height = current_scroll_height
        
    return list(data_loaded)



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
        
        # Randomly select any of the tabs (e.g Shares / Forex / Index / Commodities / Crypto)
        selected_option = find_list_of_elements_by_xpath(driver, DataTestID.APP_SYMBOL_PREFERENCE_TABS)
        if not selected_option:
            assert False, "No categories found"

        random_category = random.choice(selected_option)
        selected_category_text = get_label_of_element(element=random_category)
        print(f"Selected category: {selected_category_text}")
        click_element(element=random_category)
        
        delay(3)
        
        # Locate all checkboxes (both checked and unchecked)
        unchecked_checkboxes = find_list_of_elements_by_xpath(driver, DataTestID.APP_SYMBOL_PREFERENCE_OPTION_UNCHECKED)
        checked_checkboxes = find_list_of_elements_by_xpath(driver, DataTestID.APP_SYMBOL_PREFERENCE_OPTION_CHECKED)
        # Combine both unchecked and checked checkboxes into a list
        all_checkboxes = unchecked_checkboxes + checked_checkboxes

        if not all_checkboxes:
            raise Exception("No checkboxes found!")
        
        # # Choose a random checkbox from the combined list
        random_checkbox = random.choice(all_checkboxes)
        
        # Get the correct parent using XPath position
        symbol_name = find_element_by_xpath(driver, f"({DataTestID.APP_SYMBOL_PREFERENCE_OPTION_CHECKED} | {DataTestID.APP_SYMBOL_PREFERENCE_OPTION_UNCHECKED})[{all_checkboxes.index(random_checkbox) + 1}]/..")
        filter_symbol_name = get_label_of_element(element=symbol_name)  # Extract and clean up the text
        
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

        # Print the action taken and symbol name
        print(f"Checkbox for symbol '{filter_symbol_name}' {action}.")

        # Save changes
        save_button = find_element_by_xpath(driver, DataTestID.APP_SYMBOL_PREFERENCE_SAVE)
        click_element(element=save_button)

        alert_msg = handle_alert_success(driver)
        if alert_msg != "All changes are saved.":
            raise AssertionError(f"Receive {alert_msg} instead of the expected message")
        

        
        # Navigate to the selected category
        watchlist_option = find_list_of_elements_by_xpath(driver, DataTestID.APP_WATCHLIST_TABS)
        for option in watchlist_option:
            label_watchlist = get_label_of_element(element=option)
            print(label_watchlist)
            if label_watchlist == selected_category_text:
                click_element(element=watchlist_option)
                break
        
        # if filter_symbol_name == "Show all":
        #     if random_checkbox in unchecked_checkboxes:
        #         market_watchlist_symbol = scroll_and_retrieve_data(driver)

        #         # Compare data_loaded and full_symbol_list
        #         if set(market_watchlist_symbol) == set(filter_symbol_list):
        #             print("All symbols from full_symbol_list are present in data_loaded.")
        #         else:
        #             missing_symbols = set(filter_symbol_list) - set(market_watchlist_symbol)
        #             extra_symbols = set(market_watchlist_symbol) - set(filter_symbol_list)
                    
        #             if missing_symbols:
        #                 assert False, f"Missing symbols from market watchlist: {', '.join(missing_symbols)}"
        #             if extra_symbols:
        #                 assert False, f"Extra symbols in market watchlist not in filter_symbol_list: {', '.join(extra_symbols)}"

        #     else:
        #         no_items_message = find_visible_element_by_testid(driver, data_testid="empty-message")
        #         msg = get_label_of_element(no_items_message)
        #         if msg == "No items available.":
        #             print(f"{msg} is displayed")
        #             assert True
        #         else:
        #             raise AssertionError("The message 'No items available' was not displayed after selecting 'Show all'.")
                
        # else:
        #     market_watchlist_symbol = scroll_and_retrieve_data(driver)
        #     # If checkbox was checked, expect the symbols to be displayed
        #     if expected_symbol_visibility:  # Checkbox was checked, so expect the symbols to be visible
        #         missing_symbols = set(filter_symbol_list) - set(market_watchlist_symbol)
        #         if missing_symbols:
        #             assert False, f"Missing symbols from market watchlist (should be visible): {', '.join(missing_symbols)}"
        #         else:
        #             print(f"Symbols from filter_symbol_list {filter_symbol_list} are correctly displayed in the market watchlist.")
                
        #     # If checkbox was unchecked, expect the symbols to be hidden
        #     else:  # Checkbox was unchecked, so expect the symbols to be hidden
        #         extra_symbols = set(filter_symbol_list) & set(market_watchlist_symbol)
        #         if extra_symbols:
        #             assert False, f"Unexpected visible symbols in market watchlist (should be hidden): {', '.join(extra_symbols)}"
        #         else:
        #             print(f"No unexpected symbols {filter_symbol_list} visible, as expected.")

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""