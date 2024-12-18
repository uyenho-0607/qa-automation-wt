import traceback

from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import take_screenshot
from constants.helper.element import populate_element_with_wait, spinner_element

from common.desktop.module_trade.order_panel.orderPanel_info import button_orderPanel_action
from common.desktop.module_trade.place_edit_order.price_related import get_current_price, get_edit_order_label, pointsDistance
from common.desktop.module_trade.order_placing_window.opw_button_action import label_onePointEqual, button_trade_action, button_tradeModule
from common.desktop.module_trade.order_placing_window.utils import input_size_volume, fillPolicy_type, handle_stopLoss, handle_takeProfit


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE MARKET STOP LOSS VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def calculate_stop_loss(driver, trade_type, sl_type, option, label_onePointsEqual, current_price):
    
    min_point_distance = pointsDistance(trade_type)

    stopLoss_input = handle_stopLoss(driver, trade_type, sl_type)

    if sl_type == "price":
        if option in ["buy", "BUY"]:
            # stopLoss_value = Sell price - (One point equals * Minimum Point Distance)
            stopLoss_value = current_price + (label_onePointsEqual * min_point_distance)
            print("current price sl buy", current_price)

        if option in ["sell", "SELL"]:
            # stopLoss_value = Buy price + (One point equals * Minimum Point Distance)
            stopLoss_value = current_price - (label_onePointsEqual * min_point_distance)
            print("current price sl sell", current_price)

    populate_element_with_wait(driver, element=stopLoss_input, text=stopLoss_value)

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

def calculate_take_profit(driver, trade_type, tp_type, option, label_onePointsEqual, current_price):
    
    min_point_distance = pointsDistance(trade_type)

    takeProfit_input = handle_takeProfit(driver, trade_type, tp_type)
    
    if tp_type == "price":
        if option in ["buy", "BUY"]:
            # takeProfit_value = Sell price + (One point equals * Minimum Point Distance)
            takeProfit_value = current_price - (label_onePointsEqual * min_point_distance)
            print("current price tp buy", current_price)
                
        if option in ["sell", "SELL"]:
            # takeProfit_value = Buy price - (One point equals * Minimum Point Distance)
            takeProfit_value = current_price + (label_onePointsEqual * min_point_distance)
            print("current price tp sell", current_price)
    
    populate_element_with_wait(driver, element=takeProfit_input, text=takeProfit_value)

    return takeProfit_value

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - PLACE MARKET ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def neg_trade_market_order(driver, trade_type, option, sl_type="price", tp_type="price", set_fillPolicy: bool = False, set_stopLoss: bool = True, set_takeProfit: bool = True, set_Chart: bool = False):
    try:

        spinner_element(driver)
        
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
            calculate_stop_loss(driver, trade_type, sl_type, option, label_onePointsEqual, current_price)

        if set_takeProfit: # if set_takeProfit is True
            calculate_take_profit(driver, trade_type, tp_type, option, label_onePointsEqual, current_price)

        button_trade_action(driver, trade_type)

        # return high_price, low_price
    
    except Exception as e:
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

def neg_modify_market_order(driver, trade_type, row_number, sl_type="price", tp_type="price", set_stopLoss: bool = True, set_takeProfit: bool = True): 
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
            calculate_stop_loss(driver, trade_type, sl_type, option, label_onePointsEqual, current_price)

        if set_takeProfit: # if set_takeProfit is True
            calculate_take_profit(driver, trade_type, tp_type, option, label_onePointsEqual, current_price)

        # Perform the trade action (Update Order)
        button_trade_action(driver, trade_type)

    except Exception as e:
        handle_exception(driver, e)
  
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""