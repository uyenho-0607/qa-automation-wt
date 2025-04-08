import re

from constants.element_ids import DataTestID

from constants.helper.element_android_app import click_element, find_element_by_testid, find_element_by_testid_with_wait, find_presence_element_by_testid, find_visible_element_by_testid, get_label_of_element
from constants.helper.error_handler import handle_exception
from enums.main import ButtonModuleType, TradeDirectionOption, OrderExecutionType


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE MODULE - ONE POINTS EQUALS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_label_one_point_equal(driver, trade_type: ButtonModuleType):
    try:
            
        # Define both possible 'data-testid' values for the radio button states
        one_point_equal = {
            ButtonModuleType.TRADE: DataTestID.TRADE_ONE_POINT_EQUAL_LABEL,
            ButtonModuleType.EDIT: DataTestID.EDIT_ONE_POINT_EQUAL_LABEL
        }
        
        button_testid = one_point_equal.get(trade_type)
        if not button_testid:
            raise ValueError(f"Invalid button type: {trade_type}")
        
        # Locate the One Ppoint Equal label element
        one_points_equal_element = find_presence_element_by_testid(driver, data_testid=button_testid)
        label_one_points_equal = get_label_of_element(one_points_equal_element)

        # Regular expression to find the number after "equals:"
        one_points_equal_value = re.search(r"[\d.]+", label_one_points_equal).group()
        
        return float(one_points_equal_value)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def trade_placingModal(driver):
    return find_visible_element_by_testid(driver, data_testid=DataTestID.TRADE_BOTTOM_SHEET) 

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - PRE-TRADE DETAILS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_pre_trade(driver):
    try:
        
        button_trade = find_visible_element_by_testid(driver, data_testid=DataTestID.TRADE_BUTTON_PRE_TRADE_DETAILS)
        click_element(element=button_trade)

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

def oct_buy_sell_type(driver, option: TradeDirectionOption):
    try:
        
        # Define both possible 'data-testid' values for the radio button states
        pre_trade = {
            TradeDirectionOption.BUY: DataTestID.TRADE_BUTTON_OCT_ORDER_BUY,
            TradeDirectionOption.SELL: DataTestID.TRADE_BUTTON_OCT_ORDER_SELL
        }
        
        button_testid = pre_trade.get(option)
        if not button_testid:
            raise ValueError(f"Invalid button type: {option}")
        
        order_execution = find_element_by_testid(driver, data_testid=button_testid)
        click_element(element=order_execution)

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

def dropdown_order_type(driver, partial_text: OrderExecutionType = None):
    try:
        
        type_dropdown = find_visible_element_by_testid(driver, data_testid=DataTestID.TRADE_DROPDOWN_ORDER_TYPE)
        click_element(element=type_dropdown)
        
        # Define both possible 'data-testid' values for the radio button states
        trade_option_type = {
            OrderExecutionType.MARKET: DataTestID.TRADE_DROPDOWN_ORDER_TYPE_MARKET,
            OrderExecutionType.LIMIT: DataTestID.TRADE_DROPDOWN_ORDER_TYPE_LIMIT,
            OrderExecutionType.STOP: DataTestID.TRADE_DROPDOWN_ORDER_TYPE_STOP,
            OrderExecutionType.STOP_LIMIT: DataTestID.TRADE_DROPDOWN_ORDER_TYPE_STOP_LIMIT
        }
        
        button_testid = trade_option_type.get(partial_text)
        if not button_testid:
            raise ValueError(f"Invalid button type: {partial_text}")
        
        # Click on the Order Type
        orderType_options = find_element_by_testid_with_wait(driver, data_testid=button_testid)
        click_element(element=orderType_options)
        
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

def button_trade_action(driver, trade_type: ButtonModuleType):
    try:
        
        # Define both possible 'data-testid' values for the radio button states
        trade_action_button = {
            ButtonModuleType.TRADE: DataTestID.TRADE_BUTTON_ORDER,
            ButtonModuleType.EDIT: DataTestID.EDIT_BUTTON_ORDER
        }
        
        button_testid = trade_action_button.get(trade_type)
        if not button_testid:
            raise ValueError(f"Invalid button type: {trade_type}")
        
        # Locate the trade action button using the provided trade_type
        trade_action = find_element_by_testid_with_wait(driver, data_testid=button_testid)
        # Click the button and wait for the action to complete
        click_element(trade_action)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""