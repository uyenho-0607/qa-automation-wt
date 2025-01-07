
from constants.helper.error_handler import handle_exception
from constants.helper.element import populate_element, spinner_element

from common.desktop.module_trade.order_panel.orderPanel_info import button_orderPanel_action
from common.desktop.module_trade.order_placing_window.opw_button_action import label_onePointEqual, button_trade_action, button_tradeModule
from common.desktop.module_trade.place_edit_order.price_related import store_entryPrice, get_current_price, get_edit_order_label, get_random_point_distance, pointsDistance
from common.desktop.module_trade.order_placing_window.utils import input_size_volume, handle_entryPrice, handle_stopLoss, handle_takeProfit


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE STOP ENTRY PRICE VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def calculate_stop_entryPrice(driver, trade_type, option, label_onePointsEqual, current_price):
    global entryPrice  # Declare the use of the global variable

    entryPrice_input = handle_entryPrice(driver, trade_type)

    min_point_distance = get_random_point_distance(option, trade_type)
    
    if option in ["buy", "BUY STOP"]:
        entryPrice = current_price - (label_onePointsEqual * min_point_distance)
        
    elif option in ["sell", "SELL STOP"]:
        entryPrice = current_price + (label_onePointsEqual * min_point_distance)
        
    populate_element(element=entryPrice_input, text=entryPrice)

    # To store the entryPrice
    store_entryPrice(entryPrice)
    
    return entryPrice
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE STOP STOP LOSS VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def calculate_stop_stopLoss(driver, trade_type, sl_type, option, label_onePointsEqual):
    
    min_point_distance = pointsDistance(trade_type)

    entryPrice_value = store_entryPrice(entryPrice)
    
    stopLoss_input = handle_stopLoss(driver, trade_type, sl_type)

    if option in ["buy", "BUY STOP"]:
        stopLoss_value = entryPrice_value + (label_onePointsEqual * min_point_distance)
        
    elif option in ["sell", "SELL STOP"]:
        stopLoss_value = entryPrice_value - (label_onePointsEqual * min_point_distance)

    populate_element(element=stopLoss_input, text=stopLoss_value)

    return stopLoss_value

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE LIMIT TAKE PROFIT VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def calculate_stop_takeProfit(driver, trade_type, tp_type, option, label_onePointsEqual):
    
    min_point_distance = pointsDistance(trade_type)

    entryPrice_value = store_entryPrice(entryPrice)

    takeProfit_input = handle_takeProfit(driver, trade_type, tp_type)

    if option in ["buy", "BUY STOP"]:
        takeProfit_value = entryPrice_value - (label_onePointsEqual * min_point_distance)

    elif option in ["sell", "SELL STOP"]:
        takeProfit_value = entryPrice_value + (label_onePointsEqual * min_point_distance)
        
    populate_element(element=takeProfit_input, text=takeProfit_value)

    return takeProfit_value

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - PLACE STOP ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def neg_trade_stop_order(driver, trade_type, option, sl_type="price", tp_type="price", set_entryPrice: bool = True, set_stopLoss: bool = True, set_takeProfit: bool = True):
    try:

        spinner_element(driver)

        button_tradeModule(driver, module_Type="trade")

        # Retrieve the One Point Equal label data
        label_onePointsEqual = label_onePointEqual(driver, trade_type="trade")
        
        # Retrieve the current price based on order type and option
        current_price = get_current_price(driver, trade_type, option, partial_text="stop")

        # Input the size/volume
        input_size_volume(driver)
    
        if set_entryPrice: # if set_entryPrice is true
            calculate_stop_entryPrice(driver, trade_type, option, label_onePointsEqual, current_price)
            
        if set_stopLoss:
            calculate_stop_stopLoss(driver, trade_type, sl_type, option, label_onePointsEqual)

        if set_takeProfit: # if set_takeProfit is True
            calculate_stop_takeProfit(driver, trade_type, tp_type, option, label_onePointsEqual)
        
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
                                                EDIT - MODIFY STOP ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def neg_modify_stop_order(driver, trade_type, row_number, sl_type="price", tp_type="price", set_entryPrice:bool = True, set_stopLoss: bool = True, set_takeProfit: bool = True):
    try:

        button_orderPanel_action(driver, trade_type, row_number)

        current_price = get_current_price(driver, trade_type)

        label_onePointsEqual = label_onePointEqual(driver, trade_type="edit")
        
        option = get_edit_order_label(driver)

        if set_entryPrice: # if set_entryPrice is true
            calculate_stop_entryPrice(driver, trade_type, option, label_onePointsEqual, current_price)
            
        if set_stopLoss:
            calculate_stop_stopLoss(driver, trade_type, sl_type, option, label_onePointsEqual)

        if set_takeProfit: # if set_takeProfit is True
            calculate_stop_takeProfit(driver, trade_type, tp_type, option, label_onePointsEqual)
         
        button_trade_action(driver, trade_type)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""