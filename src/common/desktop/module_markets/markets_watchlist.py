import random
from selenium.webdriver.common.by import By

from constants.element_ids import DataTestID
from constants.helper.driver import delay
from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element import get_label_of_element, javascript_click, spinner_element, find_visible_element_by_testid, find_visible_element_by_xpath, is_element_present_by_xpath, is_element_present_by_testid, find_element_by_testid, find_element_by_xpath, find_list_of_elements_by_testid, find_list_of_elements_by_xpath, click_element, wait_for_text_to_be_present_in_element_by_testid

from common.desktop.module_subMenu.utils import menu_button


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                WATCHLIST - SYMBOL NAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def market_watchlist(driver):
    """
    This function navigates to the 'Markets' page, selects a category from the watchlist,
    and clicks a randomly selected symbol from that category.
    
    Workflow:
    1. Navigate to the 'Markets' page.
    2. Select the desired watchlist category (or a random one if not provided).
    3. Wait for symbols to load, then select a random symbol.
    4. Click on the symbol and verify that the chart is updated with the correct symbol.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    
    try:
        # Redirect to the Markets page
        menu_button(driver, menu="markets")
        
        # Ensure the tabs are visible
        # visibility_of_element_by_xpath(driver, "//div[@data-testid='watchlist-tabs']/div")
        
        delay(1)

        # Randomly select a tab
        # selected_option = find_list_of_elements_by_xpath(driver, "//div[@data-testid='watchlist-tabs']/div")
        selected_option = find_list_of_elements_by_xpath(driver, f"//*[@data-testid='{DataTestID.WATCHLIST_TABS.value}']/div")
        if selected_option:
            random_category = random.choice(selected_option)
            selected_category_text = random_category.text
            print(f"Selected category: {selected_category_text}")
            click_element(element=random_category)
            if selected_category_text.strip() == "Favourites":
                delay(0.5)
                # msg_validate = is_element_present_by_xpath(driver, "//div[@data-testid='watchlist-list']//div[@data-testid='empty-message']")
                if is_element_present_by_xpath(driver, f"//*[@data-testid='{DataTestID.WATCHLIST_LIST.value}']//*[@data-testid='empty-message']"):
                    no_items_message = find_visible_element_by_xpath(driver, f"//*[@data-testid='{DataTestID.WATCHLIST_LIST.value}']//*[@data-testid='empty-message']")
                    msg = get_label_of_element(element=no_items_message)
                    # Exclude the "Favourites" category and select a new category randomly
                    selected_option = [category for category in selected_option if category.text.strip() != "Favourites"]
                    if selected_option:  # Ensure there are other options to select from
                        random_category = random.choice(selected_option)
                        selected_category_text = random_category.text.strip()
                        print(f"No items found in Favourites, selecting another category: {selected_category_text}")
                        click_element(element=random_category)
        else:
            assert False, "No categories found"
        
        # # Wait till the spinner icon no longer display
        spinner_element(driver)
        
        # Locate all symbols in the selected category
        # symbols = find_list_of_elements_by_testid(driver, data_testid="watchlist-symbol")
        symbols = find_list_of_elements_by_testid(driver, data_testid=DataTestID.WATCHLIST_SYMBOL.value)
        if symbols:
            random_symbol = random.choice(symbols) # Randomly choose one symbol from the list
            label_symbol = random_symbol.text  # Get the symbol's name/text
            attach_text("Selected Symbol is: " + label_symbol, name="Market Watchlist Section")
            click_element(random_symbol)  # Click on the selected symbol
        else:
            # no_items_message = visibility_of_element_by_testid(driver, data_testid="empty-message")
            # no_items_message = visibility_of_element_by_xpath(driver, "//div[@data-testid='watchlist-list']//div[@data-testid='empty-message']")
            no_items_message = find_visible_element_by_xpath(driver, f"//*[@data-testid='{DataTestID.WATCHLIST_LIST.value}']//*[@data-testid='empty-message']")
            msg = get_label_of_element(element=no_items_message)
            # Raise an error if no symbols were found
            raise AssertionError(f"The message '{msg}' was displayed after selecting '{selected_category_text}' tab")

        # Verify if the correct symbol is displayed in the chart (ensuring the click was successful)
        # chart_symbol_name = wait_for_text_to_be_present_in_element_by_testid(driver, data_testid="symbol-overview-id", text=label_symbol)
        chart_symbol_name = wait_for_text_to_be_present_in_element_by_testid(driver, data_testid=DataTestID.SYMBOL_OVERVIEW_ID.value, text=label_symbol)
        
        # Assert that the symbol in the chart matches the selected symbol
        assert chart_symbol_name, f"Chart symbol mismatch: expected '{label_symbol}', found '{chart_symbol_name}'"
    
        # tab = visibility_of_element_by_testid(driver, data_testid="tab-all")
        tab = find_visible_element_by_testid(driver, data_testid=DataTestID.TAB_ALL.value)
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

def handle_alert_success(driver):
    """
    This function handles the expected login error scenario by checking for the error notification 
    and extracting the error message. It then attaches the error message for logging or reporting purposes.

    Returns:
    - success_message: The error message text extracted from the login failure notification.
    """
    # Locate the error message notification element by its test ID.
    if is_element_present_by_testid(driver, data_testid=DataTestID.ALERT_SUCCESS.value):
        success_message_notification = find_visible_element_by_testid(driver, data_testid=DataTestID.ALERT_SUCCESS.value)
        # Extract the text (label) of the error message from the notification element.
        success_message = get_label_of_element(success_message_notification)
        # Attach the extracted error message to the logs for reporting purposes.
        attach_text(success_message, name="Success message found:")
        return success_message
    else:
        error_message_notification = find_visible_element_by_testid(driver, data_testid=DataTestID.ALERT_ERROR.value)
        # Extract the text (label) of the error message from the notification element.
        error_message = get_label_of_element(error_message_notification)
        # Attach the extracted error message to the logs for reporting purposes.
        attach_text(error_message, name="Error message found:")
        assert False, f"Error message prompted, {error_message}"



def scroll_and_retrieve_data(driver):
    # Locate the scrollable div
    find_visible_element_by_testid(driver ,data_testid=DataTestID.WATCHLIST_LIST_ITEM.value)
    scrollable_div = find_element_by_xpath(driver, f"(//*[@data-testid='{DataTestID.WATCHLIST_LIST.value}']//div)[2]")
    
    # Store the current scroll height to detect when scrolling stops
    last_scroll_height = 0
    data_loaded = set()  # To store unique data items

    while True:
        # Scroll down by a small amount
        driver.execute_script("arguments[0].scrollBy(0, 200);", scrollable_div)
        
        delay(0.5)

        # Collect visible data (modify as needed for the content inside the div)
        rows = scrollable_div.find_elements(By.XPATH, f"//*[@data-testid='{DataTestID.WATCHLIST_SYMBOL.value}']")  # Adjust for your row or item selector
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
        menu_button(driver, menu="markets")
        
        # Locate all symbols in the selected category
        filter = find_visible_element_by_testid(driver, data_testid=DataTestID.SYMBOL_PREFERENCE.value)
        click_element(element=filter)  # Click on the selected symbol
        
        # Wait for the "Show/Hide Symbol" modal to appear
        result = wait_for_text_to_be_present_in_element_by_testid(driver, data_testid=DataTestID.SYMBOL_PREFERENCE_LABEL.value, text="Show/Hide Symbol")
        if not result:
            raise AssertionError("Show/Hide Symbol not found")
        
        delay(1)
        
        # Randomly select any of the tabs (e.g Shares / Forex / Index / Commodities / Crypto)
        selected_option = find_list_of_elements_by_xpath(driver, f"//*[@data-testid='{DataTestID.SYMBOL_PREFERENCE_TABS.value}']/*")
        if selected_option:
            random_category = random.choice(selected_option)
            # selected_category_text = random_category.text
            selected_category_text = random_category.text.lower()
            print(f"Selected category: {selected_category_text}")
            javascript_click(driver, element=random_category)
        else:
            assert False, "No categories found"
        
        # Locate all checkboxes (both checked and unchecked)
        unchecked_checkboxes = find_list_of_elements_by_xpath(driver, f"//*[@data-testid='{DataTestID.SYMBOL_PREFERENCE_OPTION_UNCHECKED.value}']/*")
        checked_checkboxes = find_list_of_elements_by_xpath(driver, f"//*[@data-testid='{DataTestID.SYMBOL_PREFERENCE_OPTION_CHECKED.value}']/*")
        # Combine both unchecked and checked checkboxes into a list
        all_checkboxes = unchecked_checkboxes + checked_checkboxes

        # Choose a random checkbox from the combined list
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

        # Navigate to the parent container to locate the associated text
        symbol_name = random_checkbox.find_element(By.XPATH, f".//ancestor::*[@data-testid='{DataTestID.SYMBOL_PREFERENCE_OPTION_CHECKED.value}' or @data-testid='{DataTestID.SYMBOL_PREFERENCE_OPTION_UNCHECKED.value}']")
        filter_symbol_name = symbol_name.text.strip()  # Extract and clean up the text

        # Print the action taken and symbol name
        print(f"Checkbox for symbol '{filter_symbol_name}' {action}.")

        # If the filter symbol is 'Show all', get the full list of symbols
        if filter_symbol_name == 'Show all':
            filter_symbols = find_list_of_elements_by_xpath(driver, "//div[contains(@data-testid, 'symbol-preference-option-')]")
            print(len(filter_symbols))
            filter_symbol_list = [symbol.text.strip() for symbol in filter_symbols]
            print(f"Full list of symbols: {filter_symbol_list} {action}")
        else:
            # Remain as current, no change to symbol
            filter_symbol_list = [filter_symbol_name]

        # Save changes
        save_button = find_element_by_testid(driver, data_testid=DataTestID.SYMBOL_PREFERENCE_SAVE.value)
        click_element(element=save_button)

        alert_msg = handle_alert_success(driver)
        if alert_msg != "All changes are saved.":
            raise AssertionError(f"Receive {alert_msg} instead of the expected message")

        # Locate 'X' button
        close = find_element_by_testid(driver, data_testid=DataTestID.SYMBOL_PREFERENCE_CLOSE.value)
        click_element(close)
        
        # Navigate to the selected category
        watchlist_option = find_visible_element_by_testid(driver, data_testid=f"tab-{selected_category_text}")
        click_element(element=watchlist_option)
        
        delay(0.5)
        
        if filter_symbol_name == "Show all":
            if random_checkbox in unchecked_checkboxes:
                market_watchlist_symbol = scroll_and_retrieve_data(driver)

                # Compare data_loaded and full_symbol_list
                if set(market_watchlist_symbol) == set(filter_symbol_list):
                    print("All symbols from full_symbol_list are present in data_loaded.")
                else:
                    missing_symbols = set(filter_symbol_list) - set(market_watchlist_symbol)
                    extra_symbols = set(market_watchlist_symbol) - set(filter_symbol_list)
                    
                    if missing_symbols:
                        assert False, f"Missing symbols from market watchlist: {', '.join(missing_symbols)}"
                    if extra_symbols:
                        assert False, f"Extra symbols in market watchlist not in filter_symbol_list: {', '.join(extra_symbols)}"

            else:
                no_items_message = find_visible_element_by_testid(driver, data_testid="empty-message")
                msg = get_label_of_element(no_items_message)
                if msg == "No items available.":
                    print(f"{msg} is displayed")
                    assert True
                else:
                    raise AssertionError("The message 'No items available' was not displayed after selecting 'Show all'.")
                
        else:
            market_watchlist_symbol = scroll_and_retrieve_data(driver)
            # If checkbox was checked, expect the symbols to be displayed
            if expected_symbol_visibility:  # Checkbox was checked, so expect the symbols to be visible
                missing_symbols = set(filter_symbol_list) - set(market_watchlist_symbol)
                if missing_symbols:
                    assert False, f"Missing symbols from market watchlist (should be visible): {', '.join(missing_symbols)}"
                else:
                    print(f"Symbols from filter_symbol_list {filter_symbol_list} are correctly displayed in the market watchlist.")
                
            # If checkbox was unchecked, expect the symbols to be hidden
            else:  # Checkbox was unchecked, so expect the symbols to be hidden
                extra_symbols = set(filter_symbol_list) & set(market_watchlist_symbol)
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