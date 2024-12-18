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
    try:
        
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


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE MODULE - OCT / TRADE / SPECIFICATION SELECTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_tradeModule(driver, module_Type):
    try:
        
        delay(0.5)

        moduleOption = visibility_of_element_by_testid(driver, data_testid=f"tab-{module_Type}")
        # javascript_click(driver, element=moduleOption)
        click_element_with_wait(driver, element=moduleOption)
                
        # if module_Type == "specification":
        #     onePointsEqual = find_element_by_xpath_with_wait(driver, "//div[@data-testid='specification-point-step']/div[2]")
        #     label_onePointsEqual = float(get_label_of_element(onePointsEqual))
        #     return label_onePointsEqual

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
        click_element_with_wait(driver, element=order_execution)
        
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
        
        type_dropdown = find_element_by_testid(driver, data_testid="trade-dropdown-order-type")
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
        javascript_click(driver, element=trade_action)

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""