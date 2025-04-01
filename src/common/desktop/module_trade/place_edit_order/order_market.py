from constants.helper.error_handler import handle_exception
from constants.helper.element import spinner_element, populate_element

from common.desktop.module_chart.chart import chart_minMax
from common.desktop.module_trade.order_panel.order_panel_info import button_orderPanel_action
from common.desktop.module_trade.place_edit_order.price_related import get_current_price, get_edit_order_label, get_sl_point_distance, get_tp_point_distance, pointsDistance
from common.desktop.module_trade.order_placing_window.utils import verify_volume_minMax_buttons, button_buy_sell_type, button_tradeModule, label_onePointEqual, input_size_volume, fillPolicy_type, handle_stop_loss, handle_takeProfit, button_trade_action, handle_stop_loss, handle_takeProfit, close_partialSize
from common.desktop.module_trade.order_placing_window.module_size_volume import verify_button_behavior_at_min_max, verify_invalid_size_volume_input
from enums.main import ModuleType



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE MARKET STOP LOSS VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def calculate_stop_loss(driver, trade_type, sl_type, option, label_onePointsEqual, current_price, stopLoss_flag: bool = True):
    
    min_point_distance = pointsDistance(trade_type)
    
    stopLoss_point = get_sl_point_distance(option, trade_type)

    stopLoss_input = handle_stop_loss(driver, trade_type, sl_type)

    if stopLoss_flag: # For Positive scenario
        if sl_type == "price":
            if option in ["buy", "BUY"]:
                # stopLoss_value = Sell price - (One point equals * Minimum Point Distance)
                stopLoss_value = current_price - (label_onePointsEqual * min_point_distance)
            if option in ["sell", "SELL"]:
                # stopLoss_value = Buy price + (One point equals * Minimum Point Distance)
                stopLoss_value = current_price + (label_onePointsEqual * min_point_distance)
        elif sl_type == "points":
            if option in ["buy", "BUY", "sell", "SELL"]:
                stopLoss_value = stopLoss_point
    else: # For Negative scenario
        if option in ["buy", "BUY"]:
            stopLoss_value = current_price + (label_onePointsEqual * min_point_distance)

        if option in ["sell", "SELL"]:
            stopLoss_value = current_price - (label_onePointsEqual * min_point_distance)

    print("Stop Loss Value", stopLoss_value)
    populate_element(element=stopLoss_input, text=stopLoss_value)

    return stopLoss_value

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE MARKET TAKE PROFIT VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def calculate_take_profit(driver, trade_type, tp_type, option, label_onePointsEqual, current_price, takeProfit_flag: bool = True):
    
    min_point_distance = pointsDistance(trade_type)

    takeProfit_point = get_tp_point_distance(option, trade_type)

    takeProfit_input = handle_takeProfit(driver, trade_type, tp_type)
    
    if takeProfit_flag: # For Positive scenario
        if tp_type == "price":
            if option in ["buy", "BUY"]:
                # takeProfit_value = Sell price + (One point equals * Minimum Point Distance)
                takeProfit_value = current_price + (label_onePointsEqual * min_point_distance)
                    
            if option in ["sell", "SELL"]:
                # takeProfit_value = Buy price - (One point equals * Minimum Point Distance)
                takeProfit_value = current_price - (label_onePointsEqual * min_point_distance)

        elif tp_type == "points":
            if option in ["buy", "BUY", "sell", "SELL"]:
                takeProfit_value = takeProfit_point
                
    else: # For Negative scenario
        if option in ["buy", "BUY"]:
            takeProfit_value = current_price - (label_onePointsEqual * min_point_distance)
                
        if option in ["sell", "SELL"]:
            takeProfit_value = current_price + (label_onePointsEqual * min_point_distance)

    print("Take Profit Value", takeProfit_value)
    populate_element(element=takeProfit_input, text=takeProfit_value)

    return takeProfit_value

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - OCT PLACE MARKET ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def trade_oct_market_order(driver, indicator_type, chart_fullscreen=None, set_Chart: bool = False, set_OCT: bool = True):
    try:
        
        spinner_element(driver)

        if set_Chart:
            chart_minMax(driver, chart_fullscreen)

        if set_OCT:
            button_tradeModule(driver, module_type=ModuleType.ONE_CLICK_TRADING)
        
        # Input the size/volume
        input_size_volume(driver)
                
        indicator_type = button_buy_sell_type(driver, indicator_type)
        return indicator_type

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - PLACE MARKET ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def trade_market_order(driver, trade_type, option, chart_fullscreen=None, sl_type=None, tp_type=None, set_Chart: bool = False, set_fillPolicy: bool = False, set_stopLoss: bool = True,  stopLoss_flag: bool = True, set_takeProfit: bool = True, takeProfit_flag: bool = True):
    try:

        spinner_element(driver)

        if set_Chart:
            chart_minMax(driver, chart_fullscreen)
        
        button_tradeModule(driver, module_type=ModuleType.TRADE)

        # Retrieve the One Point Equal label data
        label_onePointsEqual = label_onePointEqual(driver, trade_type=ModuleType.TRADE)

        # Retrieve the current price based on order type and option
        current_price = get_current_price(driver, trade_type, option, partial_text="market")

        # Input the size/volume
        input_size_volume(driver)

        # Select the Fill Policy
        if set_fillPolicy:
            fillPolicy_type(driver, trade_type)

        if set_stopLoss: # if set_stopLoss is True
            calculate_stop_loss(driver, trade_type, sl_type, option, label_onePointsEqual, current_price, stopLoss_flag)

        if set_takeProfit: # if set_takeProfit is True
            calculate_take_profit(driver, trade_type, tp_type, option, label_onePointsEqual, current_price, takeProfit_flag)

        button_trade_action(driver, trade_type)
        
        spinner_element(driver)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                EDIT - MODIFY MARKET ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def modify_market_order(driver, trade_type, row_number, sl_type=None, tp_type=None, set_stopLoss: bool = True,  stopLoss_flag: bool = True, set_takeProfit: bool = True, takeProfit_flag: bool = True):
    try:

        # Perform order panel action based on trade type and row numbers
        button_orderPanel_action(driver, trade_type, row_number)
        
        # Get the current price from the market
        current_price = get_current_price(driver, trade_type)
        
        # Retrieve the label indicating points equal
        label_onePointsEqual = label_onePointEqual(driver, trade_type=ModuleType.EDIT)

        # Get the edit order type label
        option = get_edit_order_label(driver)

        if set_stopLoss: # if set_stopLoss is True
            calculate_stop_loss(driver, trade_type, sl_type, option, label_onePointsEqual, current_price, stopLoss_flag)

        if set_takeProfit: # if set_takeProfit is True
            calculate_take_profit(driver, trade_type, tp_type, option, label_onePointsEqual, current_price, takeProfit_flag)
            
        # Perform the trade action (Update Order)
        button_trade_action(driver, trade_type)
        
        spinner_element(driver)
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
  
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
        

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CLOSE - MARKET ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# For closing market and deleting pending order
def close_delete_order(driver, row_number, order_action, actions: list = None, trade_type=None, set_marketSize:bool = False, set_negMarket:bool = False, set_fillPolicy:bool = False, clearField: bool = False):
    try:

        spinner_element(driver)
        
        if trade_type == "close-order":
            _, lot_size, vol_step = button_tradeModule(driver, module_type=ModuleType.SPECIFICATION)

        # Clicking on the action (Edit / Close / Delete)
        button_orderPanel_action(driver, order_action, row_number)
        
        if set_marketSize:
            close_partialSize(driver, set_fillPolicy, clearField)
        
        # Test the (- / +) button, (Min / Max) button and validation check
        if set_negMarket:
            verify_button_behavior_at_min_max(driver, trade_type, lot_size=lot_size)
            verify_volume_minMax_buttons(driver, trade_type, actions, size_volume_step=vol_step)
            verify_invalid_size_volume_input(driver, trade_type)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""