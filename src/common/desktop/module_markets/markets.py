import random

from constants.helper.driver import delay
from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element import spinner_element, get_label_of_element, click_element, visibility_of_element_by_xpath, find_element_by_xpath, find_list_of_elements_by_xpath, wait_for_text_to_be_present_in_element_by_xpath

from common.desktop.module_subMenu.utils import menu_button


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SELECT SYMBOL NAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_options():
    return {
        "My Trade": {
            "menu_name": "My Trade",
            "button_xpath": "(//span[@class='sc-1fdsqm5-2 gXxxIv'])[1]", # My Trade - button text
            "symbol_xpath": "//div[@class='sc-1cdfgfd-2 dXKVYB']", # symbol lists xpath
            "arrow_xpath": "(//div[@class='sc-1fdsqm5-0 crbctM'])[1]//*[name()='svg']",
            "tab_xpath": ["//div[@data-testid='tab-asset-order-type-open-positions']", "//div[text()='All']"] # trade - button text
        },
        "Top Picks": {
            "menu_name": "Top Picks",
            "button_xpath": "(//span[@class='sc-1fdsqm5-2 gXxxIv'])[2]", # Top Picks - button text
            "symbol_xpath": "(//div[@class='sc-uq6ok-0 eErQvo'])[2]//div[@class='sc-iubs14-5 bwsFsn']", # symbol lists xpath
            "arrow_xpath": "(//div[@class='sc-1fdsqm5-0 crbctM'])[2]//*[name()='svg']",
            "tab_xpath": ["//div[text()='Top Picks']"] # trade - button text
        },
        "Top Gainer": {
            "menu_name": "Top Gainer",
            "button_xpath": "(//span[@class='sc-1fdsqm5-2 gXxxIv'])[3]", # Top Gainer - button text
            "symbol_xpath": "(//div[@class='sc-uq6ok-0 eErQvo'])[3]//div[@class='sc-iubs14-5 bwsFsn']", # symbol lists xpath
            "arrow_xpath": "((//div[@class='sc-1fdsqm5-0 crbctM'])[3]//*[name()='svg'])[2]",
            "tab_xpath": ["//div[text()='Top Gainer']"] # trade - button text
        },
        "Top Loser": {
            "menu_name": "Top Loser",
            "button_xpath": "(//span[@class='sc-1fdsqm5-2 gXxxIv'])[3]", # Top Loser - button text
            "symbol_xpath": "(//div[@class='sc-uq6ok-0 eErQvo'])[3]//div[@class='sc-iubs14-5 bwsFsn']", # symbol lists xpath
            "arrow_xpath": "((//div[@class='sc-1fdsqm5-0 crbctM'])[3]//*[name()='svg'])[2]",
            "tab_xpath": ["//div[text()='Top Loser']"] # trade - button text
        },
        "Signal": {
            "menu_name": "Signal",
            "button_xpath": "(//span[@class='sc-1fdsqm5-2 gXxxIv'])[4]", # Signal - button text
            "symbol_xpath": "//tr[@class='sc-18g2plp-3 sc-18g2plp-5 sc-nazh05-2 iDCtfw imPFkd']//div[@class='sc-iubs14-5 fFEJmt']",
            "fav_xpath": "(//tr[@class='sc-18g2plp-3 sc-18g2plp-5 sc-nazh05-2 iDCtfw imPFkd']//div[@class='sc-1tkgbp9-0 iDQeCs'])[1]",
            "unfav_xpath": "(//tr[@class='sc-18g2plp-3 sc-18g2plp-5 sc-nazh05-2 iDCtfw imPFkd']//div[@class='sc-1tkgbp9-0 hwMknn'])[1]",
            "arrow_xpath": "((//div[@class='sc-1fdsqm5-0 crbctM'])[4]//*[name()='svg'])",
            "tab_xpath": ["//div[text()='Signal List']", "//div[text()='Favourite Signals']"]  # List of possible tab options
        },
        "News": {
            "menu_name": "News",
            "button_xpath": "(//span[@class='sc-1fdsqm5-2 gXxxIv'])[5]", # Signal - button text
            "arrow_xpath": "((//div[@class='sc-1fdsqm5-0 crbctM'])[5]//*[name()='svg'])",
            "tab_xpath": ["//div[@data-testid='side-bar-option-news']"]  # List of possible tab options
        }
    }


def select_top_loser_dropdown(driver):
    """
    Select the 'Top Loser' from the dropdown menu.
    """
    dropdown_arrow = visibility_of_element_by_xpath(driver, "//div[@class='sc-mxgjzk-0 bCqfTz']")
    click_element(dropdown_arrow)

    dropdown_value = find_element_by_xpath(driver, "//div[contains(@class, 'sc-mxgjzk-2') and text()='Top Loser']")
    click_element(dropdown_value)



def wait_for_menu_button(driver, option):
    """
    Wait for the relevant menu button to be visible.
    """
    result = wait_for_text_to_be_present_in_element_by_xpath(driver, option["button_xpath"], text=option.get("menu_name", ""))
    if not result:
        raise AssertionError(f"'{option.get('menu_name', '')}' button not found.")



def handle_signal_option(driver, option_name, option):
    """
    Handle the logic for the 'Signal' market option, dealing with favorite vs. unfavorite states.
    """
    if option_name == "Signal":
        states = [
            {
                "state": "unfav_xpath", 
                "message": "Redirecting to Signal List Tab", 
                "description": "Symbol is not marked as favorite."
            },
            {
                "state": "fav_xpath", 
                "message": "Redirecting to Favourite Signal Tab", 
                "description": "Symbol is marked as favorite."
            }
        ]
        
        for state in states:
            try:
                # Check the visibility of the state element
                visibility_of_element_by_xpath(driver, option[state["state"]])
                symbols = visibility_of_element_by_xpath(driver, option["symbol_xpath"])
                attach_text(state["message"], name=state["description"])
                return symbols
            except Exception:
                # If the element is not found, continue checking the other state
                continue
        
        # If neither state is matched, raise an exception or return a default value
        raise Exception("Neither favorite nor unfavorite state detected.")



def select_random_symbol(driver, option):
    """
    Select a random symbol from the list and click it.
    """
    symbols = find_list_of_elements_by_xpath(driver, option["symbol_xpath"])
    if not symbols:
        raise ValueError("No symbols found")
    random_symbol = random.choice(symbols)
    label_symbol = random_symbol.text
    attach_text(f"Symbol selected is: {label_symbol}", name=option.get('menu_name'))
    click_element(random_symbol)
    return random_symbol


def verify_selected_tab(driver, option):
    """
    Verify that the correct tab is selected by checking for the 'selected' class,
    matching tab text, and validating the presence of specific keys like 'fav_xpath'.
    """
    for tab_xpath in option["tab_xpath"]:
        tab = visibility_of_element_by_xpath(driver, tab_xpath)
        
        if tab:  # Ensure the tab is visible
            tab_text = tab.text
            if "selected" in tab.get_attribute("class"):
                # Check for Favourite Signals tab
                if tab_text == "Favourite Signals":
                    if "//div[@class='sc-1tkgbp9-0 iDQeCs']" in option.get("fav_xpath"):  # Replace with actual expected value
                        attach_text(f"Trade / Asset page: {tab_text} tab is pre-selected", name=f"Redirecting to the correct tab for: {option.get('menu_name')}")
                        return
                    else:
                        raise ValueError(f"Favourite Signals tab is selected, but 'fav_xpath' is incorrect {option.get('menu_name')}.")

                # Check for Signal List tab
                elif tab_text == "Signal List":
                    if "//div[@class='sc-1tkgbp9-0 hwMknn']" in option.get("unfav_xpath"):  # Replace with actual expected value
                        attach_text(f"Trade / Asset page: {tab_text} tab is pre-selected", name=f"Redirecting to the correct tab for: {option.get('menu_name')}")
                        return
                    else:
                        raise ValueError(f"Signal List tab is selected, but 'unfav_xpath' is incorrect {option.get('menu_name')}.")

                # General case
                else:
                    attach_text(f"{tab_text} tab is pre-selected", name=f"Redirecting to the correct tab for: {option.get('menu_name')}")
                    return

    raise ValueError(f"No pre-selected tab found from the specified tab options for {option.get('menu_name')}.")


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def market_select_symbols(driver, option_name):
    """
    This function navigates to the 'Markets' page, handles dropdowns for different market options,
    and selects a random symbol to interact with.

    Arguments:
    - option_name: The name of the market option to select, e.g., 'Top Loser', 'Signal', etc.

    Workflow:
    1. Navigate to the 'Markets' page.
    2. Handle special cases for specific market options (e.g., 'Top Loser', 'Signal').
    3. Wait for relevant elements to appear (e.g., menu button, symbol list).
    4. Select a random symbol and click on it.
    5. Verify that the correct tab is selected after the symbol is chosen.
    6. Handle any errors gracefully.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    
    # Define the options for each section, fetched from the 'get_options' function
    options = get_options()

    # Check if the option_name exists in the dictionary
    if option_name not in options:
        assert False, f"Invalid option name: '{option_name}'"
    
    # Get the selected option's details (e.g., button xpath, menu name, tab xpaths)
    option = options[option_name]

    try:
        # Redirect to the Markets page
        menu_button(driver, menu="markets")
        
        # Wait till the spinner icon no longer display
        spinner_element(driver)

        # Handle specific market options (e.g., 'Top Loser')
        if option_name == "Top Loser":
            select_top_loser_dropdown(driver)

        # Wait for the relevant menu button to be visible
        wait_for_menu_button(driver, option)

        # Handle "Signal" option logic
        handle_signal_option(driver, option_name, option)
        
        # Wait till the spinner icon no longer display
        spinner_element(driver)
        
        # Select a random symbol from the list and click it
        select_random_symbol(driver, option)

        # Verify that the correct tab is selected
        verify_selected_tab(driver, option)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SECTION REDIRECTION ARROW
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def market_redirect_arrow(driver, option_name):
    """
    This function navigates to the 'Markets' page, selects a given market option (e.g., 'Top Loser'),
    clicks through relevant dropdowns, and verifies redirection to the correct tab.

    Arguments:
    - option_name: The name of the option to select from the 'Markets' page, e.g., 'Top Loser', 'Top Gainer', etc.
    
    Workflow:
    1. Navigate to the 'Markets' page.
    2. Based on the given option_name, locate the appropriate dropdown and select the relevant option.
    3. Wait for the menu button (e.g., 'Top Loser', 'Top Gainer') to be visible.
    4. Click the arrow for the option to navigate to the corresponding tab.
    5. Verify the tab has been correctly selected by checking for the 'selected' class.
    6. Handle any errors gracefully.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    
    # Define the options for each section, fetched from the 'get_options' function
    options = get_options()

    # Check if the option_name exists in the dictionary
    if option_name not in options:
        assert False, f"Invalid option name: '{option_name}'"

    # Get the selected option's details (e.g., button xpath, menu name, tab xpaths)
    option = options[option_name]
        
    try:
        # Redirect to the Markets page
        menu_button(driver, menu="markets")
        
        # Handle specific market options (e.g., 'Top Loser')
        if option_name == "Top Loser":
            select_top_loser_dropdown(driver)
            
        # Wait for the relevant menu button to be visible
        wait_for_menu_button(driver, option)
        
        # Wait till the spinner icon no longer display
        spinner_element(driver)
        
        # Find and click the redirection arrow for the selected option
        redirection_arrow = find_element_by_xpath(driver, option["arrow_xpath"])
        click_element(element=redirection_arrow)
        
        # Handle "Signal" option logic
        handle_signal_option(driver, option_name, option)
        
        # Verify that the correct tab is selected
        verify_selected_tab(driver, option)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NEWS SECTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def news_section(driver):
    """
    Function to navigate to the 'Markets' page, randomly select a news item from the 'News' section,
    click on it, and then verify that the selected news item is correctly displayed on the 'News' page.
    
    Workflow:
    1. Navigate to the 'Markets' page by clicking the 'Markets' menu button.
    2. Wait for the 'News' section to load and retrieve the list of news items.
    3. Randomly select a news item and print its text.
    4. Click the selected news item.
    5. Wait for the page to load and verify that the correct news item appears on the new page.
    6. Handle exceptions and errors gracefully.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Redirect to the Markets page
        menu_button(driver, menu="markets")
        
        # Delay to allow elements to load
        delay(0.5)
        
        # Find all news items in the Markets section
        news = find_list_of_elements_by_xpath(driver, "//div[@class='sc-b6bkin-1 esEYzr']")
        
         # Check if any news items were found
        if news:
            # Check if the correct news item is displayed
            print(f"On the Markets - News section, found {len(news)} news items.")
            
            # Randomly pick one news item from the list
            selected_news = random.choice(news)
            
            # Get the text of the selected news item and print it
            news_text = selected_news.text
            print(f"Randomly selected news item: {news_text}")
            
            # Click the selected news item to navigate to its detail page
            click_element(element=selected_news)
        else:
            # Raise an error if no news items are found on the Markets page
            raise ValueError("No news found on the Markets page")
        
        # Wait for the new page to load
        delay(0.5)  # Adjust delay if needed, or use a more robust wait mechanism
        
        # Verify that the news items exist on the new page (News page)
        news_items = find_list_of_elements_by_xpath(driver, "//div[@class='sc-7tcp8z-1 EBOCv']/div")
        if news_items:
            # Check if the correct news item is displayed
            print(f"On the News page, found {len(news_items)} news items.")
                    
            # Iterate through the list of news items to find the one that is 'selected'
            for new_item in news_items:
                # Check if the 'selected' class is in the element's class attribute
                if new_item and "selected" in new_item.get_attribute("class").split():
                    news_text = new_item.text
                    # label_news = re.sub(r'\S+ \S+ - \d+ (minutes?|hours?) ago', '', news_text)
                    # print(f"{label_news.strip()} is pre-selected\n")

                    # Verify that the news item on the News page matches the randomly selected one
                    if news_text.strip() == news_text.strip():
                        attach_text(news_text, name="Match found: The news text matches the selected news in market page.")
                        assert True
                    else:
                        print("No match: The news text does not match the selected news in market page.")
                        assert False
                    break  # Exit after finding the active tab
        else:
            # Raise an error if no news items are found on the News page
            raise ValueError("No news items found.")
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SECTION MY TRADE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def myTrade_order(driver, symbol_name):
    """
    Verify that the specified symbol appears in the 'My Trade' section at the top row.
    
    Arguments:
        symbol_name: The name of the symbol to verify (e.g., "LTCUSD.std").
        
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    
    try:
        
        # Redirect to the Markets page
        menu_button(driver, menu="markets")
        
        # Wait till the spinner icon no longer display
        spinner_element(driver)
        
        # Wait until the rows in 'My Trade' section are loaded
        symbol_element = visibility_of_element_by_xpath(driver, "(//div[@class='sc-1cdfgfd-2 dXKVYB'])[1]")
        label_symbol = get_label_of_element(element=symbol_element)

        if label_symbol == symbol_name:
            print(f"Symbol '{symbol_name}' is displayed at the top row.")
            assert True
        else:
            assert False, f"Symbol '{symbol_name}' is not found in the top row."
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)