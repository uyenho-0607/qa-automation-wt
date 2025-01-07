from constants.helper.error_handler import handle_exception
from constants.helper.element import spinner_element, populate_element

from common.desktop.module_chart.chart import chart_minMax
from common.desktop.module_trade.order_panel.orderPanel_info import button_orderPanel_action
from common.desktop.module_trade.place_edit_order.price_related import get_current_price, get_edit_order_label, get_sl_point_distance, get_tp_point_distance, pointsDistance
from common.desktop.module_trade.order_placing_window.utils import button_tradeModule, label_onePointEqual, input_size_volume, button_OCT_buy_sell_type, fillPolicy_type, handle_stopLoss, handle_takeProfit, button_trade_action, handle_stopLoss, handle_takeProfit, close_partialSize


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE MARKET STOP LOSS VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def calculate_stop_loss(driver, trade_type, sl_type, option, label_onePointsEqual, current_price, stopLoss_flag: bool = True):
    
    min_point_distance = pointsDistance(trade_type)
    
    stopLoss_point = get_sl_point_distance(option, trade_type)

    stopLoss_input = handle_stopLoss(driver, trade_type, sl_type)

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

def trade_oct_market_order(driver, option, chart_fullscreen=None, set_Chart: bool = False, set_OCT: bool = True):
    try:
        
        spinner_element(driver)

        if set_Chart:
            chart_minMax(driver, chart_fullscreen)

        if set_OCT:
            button_tradeModule(driver, module_Type="one-click-trading")
        
        # Input the size/volume
        input_size_volume(driver)
        
        button_OCT_buy_sell_type(driver, option)

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

        # spinner_element(driver)

        if set_Chart:
            chart_minMax(driver, chart_fullscreen)
        
        button_tradeModule(driver, module_Type="trade")

        # Retrieve the One Point Equal label data
        label_onePointsEqual = label_onePointEqual(driver, trade_type="trade")
        
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
        label_onePointsEqual = label_onePointEqual(driver, trade_type="edit")
        
        # Get the edit order type label
        option = get_edit_order_label(driver)

        if set_stopLoss: # if set_stopLoss is True
            calculate_stop_loss(driver, trade_type, sl_type, option, label_onePointsEqual, current_price, stopLoss_flag)

        if set_takeProfit: # if set_takeProfit is True
            calculate_take_profit(driver, trade_type, tp_type, option, label_onePointsEqual, current_price, takeProfit_flag)
            
        # Perform the trade action (Update Order)
        button_trade_action(driver, trade_type)
        
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
def close_delete_order(driver, row_number, order_action, set_marketSize:bool = False, set_fillPolicy:bool = False, clearField: bool = False, delete_button: bool = False):
    try:
 
        # Clicking on the action (Edit / Close / Delete)
        button_orderPanel_action(driver, order_action, row_number, delete_button)
        
        if set_marketSize:
            close_partialSize(driver, set_fillPolicy, clearField)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""