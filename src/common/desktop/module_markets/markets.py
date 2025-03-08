import random

from selenium.webdriver.common.by import By

from constants.helper.driver import delay
from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element import javascript_click, get_label_of_element, spinner_element, click_element, visibility_of_element_by_testid, visibility_of_element_by_xpath, find_element_by_xpath, find_list_of_elements_by_testid, wait_for_text_to_be_present_in_element_by_xpath

from common.desktop.module_subMenu.utils import menu_button


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SECTION MY TRADE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def myTrade_order(driver, symbol_name, order_type):
    try:
        # Redirect to the Markets page
        menu_button(driver, menu="markets")
        
        # Wait till the spinner icon no longer displays
        spinner_element(driver)
        
        # Wait until the rows in 'My Trade' section are loaded
        top_row = visibility_of_element_by_xpath(driver, "//div[@class='sc-1g7mcs0-0 iiKKcu'][1]")
        
        # Validate symbol name in the top row
        displayed_symbol = top_row.find_element(By.XPATH, "//div[@data-testid='portfolio-row-symbol']").text.strip()
        
        if displayed_symbol != symbol_name:
            raise AssertionError(f"Symbol '{symbol_name}' is not found in the top row, instead found '{displayed_symbol}'")
        
        # Validate order type (BUY/SELL)
        displayed_order_type = top_row.find_element(By.XPATH, "//span[@data-testid='portfolio-row-order-type']").text.strip()
        
        if displayed_order_type.upper() != order_type.upper():
            raise AssertionError(f"Order type '{order_type}' does not match displayed type '{displayed_order_type}'")
        
        print(f"Order for symbol '{symbol_name}' with order type '{order_type}' is correctly displayed in the top row.")
        assert True
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)



def verify_no_orders_in_my_trades(driver):
    try:
        # Redirect to the Markets page
        menu_button(driver, menu="markets")
        
        # Wait till the spinner icon no longer displays
        spinner_element(driver)
        
        # Wait until the rows in 'My Trade' section are loaded
        match = wait_for_text_to_be_present_in_element_by_xpath(driver, "//div[contains(text(), 'You do not have any trades here')]", text="You do not have any trades here")
        if match:
            text = find_element_by_xpath(driver, "//div[contains(text(), 'You do not have any trades here')]")
            print(get_label_of_element(element=text))
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SELECT SYMBOL NAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_options():
    return {
        "My Trade": {
            "menu_name": "My Trade",
            "button_xpath": "(//span[@data-testid='market-section-title'])[1]", # My Trade - section text
            "symbol_xpath": "portfolio-row-symbol", # symbol lists xpath
            "arrow_xpath": "(//*[@data-testid='market-section-show-more'])[1]", # arrow xpath
            "tab_xpath": ["side-bar-option-assets", "tab-all"] # Assets / Trade (All) - button text
        },
        "Top Picks": {
            "menu_name": "Top Picks",
            "button_xpath": "(//span[@data-testid='market-section-title'])[2]", # Top Picks - section text
            "symbol_xpath": "top-picks-symbol", # symbol lists xpath            
            "arrow_xpath": "(//*[@data-testid='market-section-show-more'])[2]", # arrow xpath
            "tab_xpath": ["tab-popular"] # Trade (Top Picks) - button text
        },
        "Top Gainer": {
            "menu_name": "Top Gainer",
            "button_xpath": "(//span[@data-testid='market-section-title'])[3]", # Top Gainer - section text
            "symbol_xpath": "top-gainer-symbol", # symbol lists xpath
            "arrow_xpath": "(//*[@data-testid='market-section-show-more'])[3]", # arrow xpath
            "tab_xpath": ["tab-top-gainer"] # Trade (Top Gainer) - button text
        },
        "Top Loser": {
            "menu_name": "Top Loser",
            "button_xpath": "(//span[@data-testid='market-section-title'])[3]", # Top Loser - section text
            "symbol_xpath": "top-loser-symbol", # symbol lists xpath
            "arrow_xpath": "(//*[@data-testid='market-section-show-more'])[3]", # arrow xpath
            "tab_xpath": ["tab-top-loser"] # Trade (Top Loser) - button text
        },
        "Signal": {
            "menu_name": "Signal",
            "button_xpath": "(//span[@data-testid='market-section-title'])[4]", # Signal - section text
            "symbol_xpath": "signal-row-symbol",
            "fav_xpath": "(//div[@data-testid='signal-row-star-watch'])[1]", # Favourite Signals button
            "unfav_xpath": "(//div[@data-testid='signal-row-star-unwatch'])[1]", # Signal List button
            "arrow_xpath": "(//*[@data-testid='market-section-show-more'])[4]", # arrow xpath
            "tab_xpath": ["signal-filter-favourite", "signal-filter-all"]  # Favourite Signals / Signal List button text
        },
        "News": {
            "menu_name": "News",
            "button_xpath": "(//span[@data-testid='market-section-title'])[5]", # News - section text
            "arrow_xpath": "(//*[@data-testid='market-section-show-more'])[5]", # arrow xpath
            "tab_xpath": ["side-bar-option-news"]  # News - button text
        }
    }


def select_top_loser_dropdown(driver):
    """
    Select the 'Top Loser' from the dropdown menu.
    """
    # Click to select the element dropdown
    dropdown_arrow = visibility_of_element_by_testid(driver, data_testid="market-section-title-more")
    click_element(dropdown_arrow)

    # Click on the Top Loser button
    dropdown_value = find_element_by_xpath(driver, "//div[@data-testid='market-section-title-more-dropdown-item' and text()='Top Loser']")
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
    delay(1)
    
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
                symbols = visibility_of_element_by_testid(driver, data_testid=option["symbol_xpath"])
                attach_text(state["message"], name=state["description"])
                return symbols
            except Exception:
                # If the element is not found, continue checking the other state
                continue
        
        # If neither state is matched, raise an exception or return a default value
        raise Exception("Neither the xpath is wrong")


def select_random_symbol(driver, option):
    """
    Select a random symbol from the list and click it.
    """
    symbols = find_list_of_elements_by_testid(driver, data_testid=option["symbol_xpath"])
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
        # tab = visibility_of_element_by_xpath(driver, tab_xpath)
        tab = visibility_of_element_by_testid(driver, data_testid=tab_xpath)
        if tab:  # Ensure the tab is visible
            tab_text = tab.text
            if "selected" in tab.get_attribute("class"):
                # Check for Favourite Signals tab
                if tab_text == "Favourite Signals":
                    if "//div[@data-testid='signal-row-star-watch']" in option.get("fav_xpath"):
                        attach_text(f"Trade / Asset page: {tab_text} tab is pre-selected", name=f"Redirecting to the correct tab for: {option.get('menu_name')}")
                        return
                    else:
                        raise ValueError(f"Favourite Signals tab is selected, but 'fav_xpath' is incorrect {option.get('menu_name')}.")

                # Check for Signal List tab
                elif tab_text == "Signal List":
                    if "//div[@data-testid='signal-row-star-unwatch']" in option.get("unfav_xpath"):
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
        
        spinner_element(driver)
        
        # Delay to allow elements to load
        delay(2)

        # Find all news items in the Markets section
        news = find_list_of_elements_by_testid(driver, data_testid="market-news-content-text")
        
         # Check if any news items were found
        if news:
            # Check if the correct news item is displayed
            print(f"On the Markets - News section, found {len(news)} news items.")
            
            # Randomly pick one news item from the list
            selected_news = random.choice(news)
            
            # Get the text of the selected news item and print it
            market_news_text = selected_news.text
            attach_text(market_news_text, name="Randomly selected news item: ")

            # Click the selected news item to navigate to its detail page
            javascript_click(driver, element=selected_news)
        
        # Wait for the new page to load
        delay(0.5)  # Adjust delay if needed, or use a more robust wait mechanism
        
        # Verify that the news items exist on the new page (News page)
        news_items = find_list_of_elements_by_testid(driver, "news-option")
        if news_items:
            # Iterate through the list of news items to find the one that is 'selected'
            for new_item in news_items:
                # Check if the 'selected' class is in the element's class attribute
                if new_item and "selected" in new_item.get_attribute("class").split():
                    signal_news_text = new_item.text
                    # label_news = re.sub(r'\S+ \S+ - \d+ (minutes?|hours?) ago', '', news_text)
                    # print(f"{label_news.strip()} is pre-selected\n")
                    # Verify that the news item on the News page matches the randomly selected one
                    if signal_news_text.strip() == market_news_text.strip():
                        attach_text(signal_news_text, name="Match found: The news text pre-selected on the new page aligns with the selected news on the market page.")
                        assert True
                    else:
                        assert False, "No match: The news text does not match the selected news in market page."
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