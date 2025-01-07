
from constants.helper.error_handler import handle_exception
from constants.helper.element import populate_element, spinner_element

from common.desktop.module_trade.order_panel.orderPanel_info import button_orderPanel_action
from common.desktop.module_trade.order_placing_window.opw_button_action import label_onePointEqual, button_trade_action, button_tradeModule
from common.desktop.module_trade.place_edit_order.price_related import store_entryPrice, get_current_price, get_edit_order_label, get_random_point_distance, pointsDistance
from common.desktop.module_trade.order_placing_window.utils import input_size_volume, handle_entryPrice, handle_stopLimitPrice, handle_stopLoss, handle_takeProfit


# Define a global variable
entryPrice = None
stopLimitPrice = None

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE STOP LIMIT ENTRY PRICE VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def calculate_stopLimit_entryPrice(driver, trade_type, option, label_onePointsEqual, current_price,  entryPrice_flag : bool = True):
    global entryPrice  # Declare the use of the global variable

    entryPrice_input = handle_entryPrice(driver, trade_type)

    min_point_distance = get_random_point_distance(option, trade_type)
    
    if entryPrice_flag: # for negative Price
        if option in ["buy", "BUY STOP LIMIT"]:
            entryPrice = current_price - (label_onePointsEqual * min_point_distance)
            
        elif option in ["sell", "SELL STOP LIMIT"]:
            entryPrice = current_price + (label_onePointsEqual * min_point_distance)

    populate_element(element=entryPrice_input, text=entryPrice)

    # To store the entryPrice
    store_entryPrice(entryPrice)
    
    return entryPrice

# # To store the Stop Limit Entry Price variable
# def store_stopLimit_entryPrice():
#     global entryPrice  # Declare the use of the global variable
#     print("Stored Limit Entry Price Value:", entryPrice)
#     return entryPrice


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""




"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE STOP LIMIT PRICE VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def calculate_stopLimit_Price(driver, trade_type, option, label_onePointsEqual):

    global stopLimitPrice  # Declare the use of the global variable

    stopLimitPrice_input = handle_stopLimitPrice(driver, trade_type)

    min_point_distance = get_random_point_distance(option, trade_type)

    entryPrice_value = store_entryPrice(entryPrice)

    if option in ["buy", "BUY STOP LIMIT"]:
        stopLimitPrice = entryPrice_value + (label_onePointsEqual * min_point_distance)
        
    elif option in ["sell", "SELL STOP LIMIT"]:
        stopLimitPrice = entryPrice_value - (label_onePointsEqual * min_point_distance)

    populate_element(element=stopLimitPrice_input, text=stopLimitPrice)

    return stopLimitPrice


# To store the Stop Limit Price variable
def store_stopLimitPrice():
    global stopLimitPrice  # Declare the use of the global variable
    print("Stored Stop Limit Price Value:", stopLimitPrice)
    return stopLimitPrice

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE STOP LIMIT STOP LOSS VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def calculate_stopLimit_stopLoss(driver, trade_type, sl_type, option, label_onePointsEqual):

    min_point_distance = pointsDistance(trade_type)

    stopLimitPrice_value = store_stopLimitPrice()

    stopLoss_input = handle_stopLoss(driver, trade_type, sl_type)

    if option in ["buy", "BUY STOP LIMIT"]:
        stopLoss_value = stopLimitPrice_value + (label_onePointsEqual * min_point_distance)
            
    elif option in ["sell", "SELL STOP LIMIT"]:
        stopLoss_value = stopLimitPrice_value - (label_onePointsEqual * min_point_distance)

    populate_element(element=stopLoss_input, text=stopLoss_value)

    return stopLoss_value
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE STOP LIMIT TAKE PROFIT VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def calculate_stopLimit_takeProfit(driver, trade_type, tp_type, option, label_onePointsEqual):
    
    min_point_distance = pointsDistance(trade_type)

    stopLimitPrice_value = store_stopLimitPrice()

    takeProfit_input = handle_takeProfit(driver, trade_type, tp_type)

    if option in ["buy", "BUY STOP LIMIT"]:
        takeProfit_value = stopLimitPrice_value - (label_onePointsEqual * min_point_distance)
            
    elif option in ["sell", "SELL STOP LIMIT"]:
        takeProfit_value = stopLimitPrice_value + (label_onePointsEqual * min_point_distance)

    populate_element(element=takeProfit_input, text=takeProfit_value)

    return takeProfit_value

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - PLACE STOP LIMIT ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def neg_trade_stopLimit_order(driver, trade_type, option, sl_type="price", tp_type="price", set_entryPrice: bool = True, entryPrice_flag: bool = True, set_stopLimitPrice:bool = True, set_stopLoss: bool = True, set_takeProfit: bool = True):
    try:
        
        spinner_element(driver)

        button_tradeModule(driver, module_Type="trade")

        # Retrieve the One Point Equal label data
        label_onePointsEqual = label_onePointEqual(driver, trade_type="trade")
        
        # Retrieve the current price based on order type and option
        current_price = get_current_price(driver, trade_type, option, partial_text="stop-limit")

        # Input the size/volume
        input_size_volume(driver)
        
        if set_entryPrice: # if set_entryPrice is true
            calculate_stopLimit_entryPrice(driver, trade_type, option, label_onePointsEqual, current_price, entryPrice_flag)
            
        if set_stopLimitPrice: # if set_entryPrice is true
            calculate_stopLimit_Price(driver, trade_type, option, label_onePointsEqual)

        if set_stopLoss: # if set_stopLoss is true
            calculate_stopLimit_stopLoss(driver, trade_type, sl_type, option, label_onePointsEqual)

        if set_takeProfit: # if set_takeProfit is true
            calculate_stopLimit_takeProfit(driver, trade_type, tp_type, option, label_onePointsEqual)
        
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
                                                EDIT - MODIFY STOP LIMIT ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def neg_modify_stopLimit_order(driver, trade_type, row_number, sl_type="price", tp_type="price", set_entryPrice:bool = True, entryPrice_flag: bool = True, set_stopLimitPrice: bool = True, set_stopLoss: bool = True, set_takeProfit: bool = True):
    try:
        
        button_orderPanel_action(driver, trade_type, row_number)

        current_price = get_current_price(driver, trade_type)

        label_onePointsEqual = label_onePointEqual(driver, trade_type="edit")

        # To retrieve the order type value
        option = get_edit_order_label(driver)

        if set_entryPrice: # if set_entryPrice is true
            calculate_stopLimit_entryPrice(driver, trade_type, option, label_onePointsEqual, current_price, entryPrice_flag)
            
        if set_stopLimitPrice: # if set_entryPrice is true
            calculate_stopLimit_Price(driver, trade_type, option, label_onePointsEqual)

        if set_stopLoss:
            calculate_stopLimit_stopLoss(driver, trade_type, sl_type, option, label_onePointsEqual)

        if set_takeProfit: # if set_takeProfit is True
            calculate_stopLimit_takeProfit(driver, trade_type, tp_type, option, label_onePointsEqual)
         
        button_trade_action(driver, trade_type)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""