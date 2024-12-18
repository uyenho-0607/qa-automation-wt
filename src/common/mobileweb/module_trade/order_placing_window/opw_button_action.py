import re

from constants.helper.driver import delay
from constants.helper.element import click_element, find_element_by_testid, visibility_of_element_by_testid, get_label_of_element, javascript_click
from constants.helper.error_handler import handle_exception


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE MODULE - ONE POINTS EQUALS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def label_onePointEqual(driver, trade_type):
    try:
        
        # Locate the One Ppoint Equal label element
        onePointsEqual = visibility_of_element_by_testid(driver, data_testid=f"{trade_type}-one-point-equal-label")
        label_onePointsEqual = get_label_of_element(onePointsEqual)

        # Regular expression to find the number after "equals:"
        onePointsEqual_value = re.search(r"[\d.]+", label_onePointsEqual).group()
        
        return float(onePointsEqual_value)

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def trade_placingModal(driver):        
    return visibility_of_element_by_testid(driver, data_testid="trade-bottom-sheet") 

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - PRE-TRADE DETAILS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_preTrade(driver):
    try:
        
        button_trade = visibility_of_element_by_testid(driver, data_testid="trade-button-pre-trade-details")
        click_element(element=button_trade)

    except Exception as e:
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
    try:
        
        order_execution = visibility_of_element_by_testid(driver, data_testid=f"trade-button-order-{indicator_type}")
        javascript_click(driver, element=order_execution)

    except Exception as e:
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
    try:
        
        order_execution = find_element_by_testid(driver, data_testid=f"trade-button-oct-order-{option}")
        javascript_click(driver, element=order_execution)

    except Exception as e:
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
    try:
        
        type_dropdown = visibility_of_element_by_testid(driver, data_testid="trade-dropdown-order-type")
        javascript_click(driver, element=type_dropdown)

        orderType_options = visibility_of_element_by_testid(driver, data_testid=f"trade-dropdown-order-type-{partial_text}")
        javascript_click(driver, element=orderType_options)
            
        return partial_text
        
    except Exception as e:
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
    try:

        # Locate the trade action button using the provided trade_type
        trade_action = find_element_by_testid(driver, data_testid=f"{trade_type}-button-order")
        # Click the button and wait for the action to complete
        click_element(trade_action)

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""