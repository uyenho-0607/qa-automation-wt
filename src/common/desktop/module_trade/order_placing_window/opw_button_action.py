import re

from constants.helper.driver import delay
from constants.helper.element import click_element, javascript_click, click_element_with_wait, find_element_by_testid, visibility_of_element_by_testid, get_label_of_element
from constants.helper.error_handler import handle_exception



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE MODULE - ONE POINTS EQUALS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def label_onePointEqual(driver, trade_type):
    """
    Retrieves the value of "one point equal" for a given trade type from the web page.
    The value is extracted from a label element that displays the value in the format "equals: <value>".
    
    Arguments:
    - trade_type: The type of trade (e.g., "trade", "edit") to help locate the specific elements.
    
    Returns:
    - float: The value extracted from the label, representing "one point equal" for the given trade type.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Locate the element that contains the "one point equal" value
        onePointsEqual = visibility_of_element_by_testid(driver, data_testid=f"{trade_type}-one-point-equal-label")
        
        # Get the label text from the located element
        label_onePointsEqual = get_label_of_element(onePointsEqual)

        # Regular expression to find the number after "equals:"
        onePointsEqual_value = re.search(r"[\d.]+", label_onePointsEqual).group()
        
        # Ensure that a value was found, otherwise raise an exception
        if onePointsEqual_value:
            # Return the numeric value as a float
            return float(onePointsEqual_value)
        else:
            raise ValueError(f"Could not find a valid value in the label: {label_onePointsEqual}")
        
        # return float(onePointsEqual_value)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE MODULE - OCT / TRADE / SPECIFICATION SELECTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_tradeModule(driver, module_Type: str):
    """
    Interacts with the trade module based on the provided module type.
    It locates the corresponding tab for the module type and clicks it.

    Arguments:
    - module_Type: The type of trade module to click, such as "oct", "trade", "specification", etc.

    Returns:
    - None: The function doesn't return any value. It performs actions on the page.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Introducing a slight delay to handle any page load or rendering delays
        delay(0.5)

        # Locate the module tab based on the provided module type
        moduleOption = visibility_of_element_by_testid(driver, data_testid=f"tab-{module_Type}")

        # Click the module tab with wait to ensure it's properly loaded before proceeding
        click_element_with_wait(driver, element=moduleOption)
                
        # if module_Type == "specification":
        #     onePointsEqual = find_element_by_xpath_with_wait(driver, "//div[@data-testid='specification-point-step']/div[2]")
        #     label_onePointsEqual = float(get_label_of_element(onePointsEqual))
        #     return label_onePointsEqual

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - BUY / SELL BUTTON INDICATOR
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_buy_sell_type(driver, indicator_type):
    """
    Clicks on the trade button (Buy/Sell) based on the given indicator type.
    The button is identified by its `data-testid` attribute, which is dynamically constructed using the `indicator_type`.

    Arguments:
    - indicator_type: A string representing the type of trade action, such as "buy" or "sell".
    
    Returns:
    - None: The function performs the action of clicking the button but does not return any value.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Locate the order execution button based on the provided indicator_type (buy/sell)
        order_execution = visibility_of_element_by_testid(driver, data_testid=f"trade-button-order-{indicator_type}")

        # Click the button with a wait to ensure the element is interactable before clicking
        click_element_with_wait(driver, element=order_execution)
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE OCT - BUY / SELL BUTTON INDICATOR
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_OCT_buy_sell_type(driver, option):
    """
    Clicks on the OCT (Order Confirmation Tab) buy or sell button based on the given option.
    The button is identified by its `data-testid` attribute, dynamically constructed using the `option`.

    Arguments:
    - option: A string representing the trade action, such as "buy" or "sell".
    
    Returns:
    - None: The function performs the action of clicking the button but does not return any value.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Locate the order execution button for the OCT buy/sell option
        order_execution = find_element_by_testid(driver, data_testid=f"trade-button-oct-order-{option}")
        
        # Click the button using JavaScript to ensure the click is performed even if the element is hidden or overlayed
        javascript_click(driver, element=order_execution)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - ORDER TYPE DROPDOWN SELECTION (MARKET / LIMIT / STOP / STOP LIMIT)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def dropdown_orderType(driver, partial_text=None):
    """
    Selects an order type from the dropdown based on the provided partial_text.
    The dropdown options are dynamically located by the `data-testid` attributes.

    Arguments:
    - partial_text: A string (or partial string) to match against the order type options in the dropdown. (e.g. 'market', 'limit', 'stop', 'stop-limit')
      If `None`, the function will not filter by text but will select the first available option.

    Returns:
    - partial_text: The text of the order type selected from the dropdown. 
      If `partial_text` is provided, it will return the selected option text.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        
        # Locate the dropdown element for the order type
        type_dropdown = find_element_by_testid(driver, data_testid="trade-dropdown-order-type")
        # Click on the dropdown to reveal the options
        javascript_click(driver, element=type_dropdown)
        
        # Locate the option with a test ID based on the partial_text value
        orderType_options = visibility_of_element_by_testid(driver, data_testid=f"trade-dropdown-order-type-{partial_text}")
        # Click on the dropdown to reveal the options
        javascript_click(driver, element=orderType_options)

        # Return the text of the selected order type
        return partial_text
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - PLACE / UPDATE BUTTON
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_trade_action(driver, trade_type):
    """
    This function locates and clicks on the trade action button for a given trade type.
    The button is identified dynamically using the `trade_type` to form a test ID.

    Arguments:
    - trade_type: The type of trade (e.g., "trade", "edit") to help locate the specific elements.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Locate the trade action button using the provided trade_type
        trade_action = find_element_by_testid(driver, data_testid=f"{trade_type}-button-order")
        javascript_click(driver, element=trade_action)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""