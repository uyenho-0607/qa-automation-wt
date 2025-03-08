from constants.helper.error_handler import handle_exception
from constants.helper.element import spinner_element, populate_element

from common.desktop.module_chart.chart import chart_minMax
from common.desktop.module_trade.order_panel.order_panel_info import button_orderPanel_action
from common.desktop.module_trade.place_edit_order.price_related import store_entryPrice, get_current_price, get_edit_order_label, get_random_point_distance, get_sl_point_distance, get_tp_point_distance, pointsDistance
from common.desktop.module_trade.order_placing_window.utils import button_tradeModule, label_onePointEqual, input_size_volume, handle_entryPrice, handle_stopLimitPrice, handle_stop_loss, handle_takeProfit, expiry, button_trade_action


# Define a global variable
entryPrice = None
stopLimitPrice = None

# To store the Stop Limit Price variable
def store_stopLimitPrice():
    global stopLimitPrice  # Declare the use of the global variable
    print("Stored Stop Limit Price Value:", stopLimitPrice)
    return stopLimitPrice


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE STOP LIMIT ENTRY PRICE VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def calculate_stopLimit_entryPrice(driver, trade_type, option, label_onePointsEqual, current_price, entryPrice_flag: bool = True):
    global entryPrice  # Declare the use of the global variable

    entryPrice_input = handle_entryPrice(driver, trade_type)

    min_point_distance = get_random_point_distance(option, trade_type)
    
    if entryPrice_flag: # For Positive scenario
        if option in ["buy", "BUY STOP LIMIT"]:
            # EntryPrice = Buy price + (One point equals * Minimum Point Distance)
            entryPrice = current_price + (label_onePointsEqual * min_point_distance)
            
        elif option in ["sell", "SELL STOP LIMIT"]:
            # EntryPrice = Sell price - (One point equals * Minimum Point Distance)
            entryPrice = current_price - (label_onePointsEqual * min_point_distance)
    else: # For Negative scenario
        if option in ["buy", "BUY STOP LIMIT"]:
            entryPrice = current_price - (label_onePointsEqual * min_point_distance)
            
        elif option in ["sell", "SELL STOP LIMIT"]:
            entryPrice = current_price + (label_onePointsEqual * min_point_distance)
        
    print("Entry Price Value", entryPrice)
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
                                                TRADE / EDIT - CALCULATE STOP LIMIT PRICE VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def calculate_stopLimit_Price(driver, trade_type, option, label_onePointsEqual, stopLimitPrice_flag: bool = True):

    global stopLimitPrice  # Declare the use of the global variable

    stopLimitPrice_input = handle_stopLimitPrice(driver, trade_type)

    min_point_distance = get_random_point_distance(option, trade_type)

    entryPrice_value = store_entryPrice(entryPrice)

    if stopLimitPrice_flag: # For Positive scenario
        if option in ["buy", "BUY STOP LIMIT"]:
            # stopLimitPrice = Price(SL) - (One point equals * Minimum Point Distance)
            stopLimitPrice = entryPrice_value - (label_onePointsEqual * min_point_distance)
        elif option in ["sell", "SELL STOP LIMIT"]:
            # stopLimitPrice = Price(SL) + (One point equals * Minimum Point Distance)
            stopLimitPrice = entryPrice_value + (label_onePointsEqual * min_point_distance)
            
    else: # For Negative scenario
        if option in ["buy", "BUY STOP LIMIT"]:
            stopLimitPrice = entryPrice_value + (label_onePointsEqual * min_point_distance)
        elif option in ["sell", "SELL STOP LIMIT"]:
            stopLimitPrice = entryPrice_value - (label_onePointsEqual * min_point_distance)

    print("Stop Limit Price Value", stopLimitPrice)
    populate_element(element=stopLimitPrice_input, text=stopLimitPrice)

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

def calculate_stopLimit_stopLoss(driver, trade_type, sl_type, option, label_onePointsEqual, stopLoss_flag: bool = True):

    min_point_distance = pointsDistance(trade_type)

    stopLoss_point = get_sl_point_distance(option, trade_type)

    stopLimitPrice_value = store_stopLimitPrice()

    stopLoss_input = handle_stop_loss(driver, trade_type, sl_type)

    if stopLoss_flag: # For Positive scenario
        if sl_type == "price":
            if option in ["buy", "BUY STOP LIMIT"]:
                # stopLoss_value = Stop Limit Price - (One point equals * Minimum Point Distance)
                stopLoss_value = stopLimitPrice_value - (label_onePointsEqual * min_point_distance)
                    
            elif option in ["sell", "SELL STOP LIMIT"]:
                # stopLoss_value = Stop Limit Price + (One point equals * Minimum Point Distance)
                stopLoss_value = stopLimitPrice_value + (label_onePointsEqual * min_point_distance)
                        
        elif sl_type == "points":
            if option in ["buy", "BUY STOP LIMIT", "sell", "SELL STOP LIMIT"]:
                stopLoss_value = stopLoss_point
    else: # For Negative scenario
        if option in ["buy", "BUY STOP LIMIT"]:
            stopLoss_value = stopLimitPrice_value + (label_onePointsEqual * min_point_distance)
                
        elif option in ["sell", "SELL STOP LIMIT"]:
            stopLoss_value = stopLimitPrice_value - (label_onePointsEqual * min_point_distance)

    print("Stop Loss Value", stopLoss_value)
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

def calculate_stopLimit_takeProfit(driver, trade_type, tp_type, option, label_onePointsEqual, takeProfit_flag: bool = True):
    
    min_point_distance = pointsDistance(trade_type)

    takeProfit_point = get_tp_point_distance(option, trade_type)

    stopLimitPrice_value = store_stopLimitPrice()

    takeProfit_input = handle_takeProfit(driver, trade_type, tp_type)

    if takeProfit_flag: # For Positive scenario
        if tp_type == "price":
            if option in ["buy", "BUY STOP LIMIT"]:
                # takeProfit_value = Stop Limit Price + (One point equals * Minimum Point Distance)
                takeProfit_value = stopLimitPrice_value + (label_onePointsEqual * min_point_distance)
                    
            elif option in ["sell", "SELL STOP LIMIT"]:
                # takeProfit_value = Stop Limit Price - (One point equals * Minimum Point Distance)
                takeProfit_value = stopLimitPrice_value - (label_onePointsEqual * min_point_distance)
                        
        elif tp_type == "points":
            if option in ["buy", "BUY STOP LIMIT", "sell", "SELL STOP LIMIT"]:
                takeProfit_value = takeProfit_point
    else: # For Negative scenario
        if option in ["buy", "BUY STOP LIMIT"]:
            takeProfit_value = stopLimitPrice_value - (label_onePointsEqual * min_point_distance)
                
        elif option in ["sell", "SELL STOP LIMIT"]:
            takeProfit_value = stopLimitPrice_value + (label_onePointsEqual * min_point_distance)

    print("Take Profit Value", takeProfit_value)
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

def trade_stopLimit_order(driver, trade_type, option, expiryType, expiryDate=None, targetMonth=None, hour_option=None, min_option=None, sl_type=None, tp_type=None, chart_fullscreen=None, set_Chart: bool = False, entryPrice_flag: bool = True, stopLimitPrice_flag: bool = True, set_stopLoss: bool = True, stopLoss_flag: bool = True, set_takeProfit: bool = True, takeProfit_flag: bool = True, specifiedDate: bool = False):
    try:
        
        spinner_element(driver)

        if set_Chart:
            chart_minMax(driver, chart_fullscreen)

        button_tradeModule(driver, module_Type="trade")

        # Retrieve the One Point Equal label data
        label_onePointsEqual = label_onePointEqual(driver, trade_type="trade")
        
        # Retrieve the current price based on order type and option
        current_price = get_current_price(driver, trade_type, option, partial_text="stop-limit")

        # Input the size/volume
        input_size_volume(driver)
        
        calculate_stopLimit_entryPrice(driver, trade_type, option, label_onePointsEqual, current_price, entryPrice_flag)
            
        calculate_stopLimit_Price(driver, trade_type, option, label_onePointsEqual, stopLimitPrice_flag)

        if set_stopLoss: # if set_stopLoss is true
            calculate_stopLimit_stopLoss(driver, trade_type, sl_type, option, label_onePointsEqual, stopLoss_flag)

        if set_takeProfit: # if set_takeProfit is true
            calculate_stopLimit_takeProfit(driver, trade_type, tp_type, option, label_onePointsEqual, takeProfit_flag)

        expiry(driver, trade_type, expiryType, expiryDate, targetMonth, hour_option, min_option, specifiedDate)
        
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

def modify_stopLimit_order(driver, trade_type, row_number, expiryType, expiryDate=None, targetMonth=None, hour_option=None, min_option=None, sl_type=None, tp_type=None, entryPrice_flag: bool = True, stopLimitPrice_flag: bool = True, set_stopLoss: bool = True, stopLoss_flag: bool = True, set_takeProfit: bool = True, takeProfit_flag: bool = True, specifiedDate: bool = False):
    try:
        
        button_orderPanel_action(driver, trade_type, row_number)

        current_price = get_current_price(driver, trade_type)

        label_onePointsEqual = label_onePointEqual(driver, trade_type="edit")

        # To retrieve the order type value
        option = get_edit_order_label(driver)

        calculate_stopLimit_entryPrice(driver, trade_type, option, label_onePointsEqual, current_price, entryPrice_flag)
            
        calculate_stopLimit_Price(driver, trade_type, option, label_onePointsEqual, stopLimitPrice_flag)

        if set_stopLoss:
            calculate_stopLimit_stopLoss(driver, trade_type, sl_type, option, label_onePointsEqual, stopLoss_flag)

        if set_takeProfit: # if set_takeProfit is True
            calculate_stopLimit_takeProfit(driver, trade_type, tp_type, option, label_onePointsEqual, takeProfit_flag)
                
        expiry(driver, trade_type, expiryType, expiryDate, targetMonth, hour_option, min_option, specifiedDate)
         
        button_trade_action(driver, trade_type)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""