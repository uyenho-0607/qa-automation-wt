from constants.helper.error_handler import handle_exception
from constants.helper.element import spinner_element, populate_element

from common.desktop.module_chart.chart import chart_minMax
from common.desktop.module_trade.order_panel.order_panel_info import button_orderPanel_action
from common.desktop.module_trade.place_edit_order.price_related import store_entryPrice, get_current_price, get_edit_order_label, get_random_point_distance, get_sl_point_distance, get_tp_point_distance, pointsDistance
from common.desktop.module_trade.order_placing_window.utils import button_tradeModule, label_onePointEqual, input_size_volume, handle_entryPrice, handle_stop_loss, handle_takeProfit, expiry, button_trade_action



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE LIMIT ENTRY PRICE VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
#  entryPrice_flag : bool = True
def calculate_limit_entryPrice(driver, trade_type, option, label_onePointsEqual, current_price, entryPrice_flag: bool = True):
    global entryPrice  # Declare the use of the global variable

    entryPrice_input = handle_entryPrice(driver, trade_type)

    min_point_distance = get_random_point_distance(option, trade_type)
    
    if entryPrice_flag: # For Positive scenario
        if option in ["buy", "BUY LIMIT"]:
            # EntryPrice = Buy price - (One point equals * Minimum Point Distance)
            entryPrice = current_price - (label_onePointsEqual * min_point_distance)
        elif option in ["sell", "SELL LIMIT"]:
            # EntryPrice = Sell price + (One point equals * Minimum Point Distance)
            entryPrice = current_price + (label_onePointsEqual * min_point_distance)
    else: # For Negative scenario
        if option in ["buy", "BUY LIMIT"]:
            entryPrice = current_price + (label_onePointsEqual * min_point_distance)
        elif option in ["sell", "SELL LIMIT"]:
            entryPrice = current_price - (label_onePointsEqual * min_point_distance)
        
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
                                                TRADE / EDIT - CALCULATE LIMIT STOP LOSS VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def calculate_limit_stopLoss(driver, trade_type, sl_type, option, label_onePointsEqual, stopLoss_flag: bool = True):
    
    min_point_distance = pointsDistance(trade_type)

    stopLoss_point = get_sl_point_distance(option, trade_type)
    
    entryPrice_value = store_entryPrice(entryPrice)
    
    stopLoss_input = handle_stop_loss(driver, trade_type, sl_type)

    if stopLoss_flag: # For Positive scenario
        if sl_type == "price":
            if option in ["buy", "BUY LIMIT"]:
                # stopLoss_value = Price(L) - (One point equals * Minimum Point Distance)
                stopLoss_value = entryPrice_value - (label_onePointsEqual * min_point_distance)
                
            elif option in ["sell", "SELL LIMIT"]:
                # stopLoss_value = Price(L) + (One point equals * Minimum Point Distance)
                stopLoss_value = entryPrice_value + (label_onePointsEqual * min_point_distance)
                        
        elif sl_type == "points":
            if option in ["buy", "BUY LIMIT", "sell", "SELL LIMIT"]:
                stopLoss_value = stopLoss_point
    else: # For Negative scenario
        if option in ["buy", "BUY LIMIT"]:
            stopLoss_value = entryPrice_value + (label_onePointsEqual * min_point_distance)
            
        elif option in ["sell", "SELL LIMIT"]:
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

def calculate_limit_takeProfit(driver, trade_type, tp_type, option, label_onePointsEqual, takeProfit_flag: bool = True):

    min_point_distance = pointsDistance(trade_type)

    takeProfit_point = get_tp_point_distance(option, trade_type)
    
    entryPrice_value = store_entryPrice(entryPrice)

    takeProfit_input = handle_takeProfit(driver, trade_type, tp_type)

    if takeProfit_flag: # For Positive scenario
        if tp_type == "price":
            if option in ["buy", "BUY LIMIT"]:
                # takeProfit_value = Price(L) + (One point equals * Minimum Point Distance)
                takeProfit_value = entryPrice_value + (label_onePointsEqual * min_point_distance)

            elif option in ["sell", "SELL LIMIT"]:
                # takeProfit_value = Price(L) - (One point equals * Minimum Point Distance)
                takeProfit_value = entryPrice_value - (label_onePointsEqual * min_point_distance)
                        
        elif tp_type == "points":
            if option in ["buy", "BUY LIMIT", "sell", "SELL LIMIT"]:
                takeProfit_value = takeProfit_point
    else: # For Negative scenario
        if option in ["buy", "BUY LIMIT"]:
            takeProfit_value = entryPrice_value - (label_onePointsEqual * min_point_distance)

        elif option in ["sell", "SELL LIMIT"]:
            takeProfit_value = entryPrice_value + (label_onePointsEqual * min_point_distance)

    populate_element(element=takeProfit_input, text=takeProfit_value)

    return takeProfit_value

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - PLACE LIMIT ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def trade_limit_order(driver, trade_type, option, expiryType, expiryDate=None, targetMonth=None, hour_option=None, min_option=None, sl_type=None, tp_type=None, chart_fullscreen=None, set_Chart: bool = False, entryPrice_flag: bool = True, set_stopLoss: bool = True, stopLoss_flag: bool = True, set_takeProfit: bool = True, takeProfit_flag: bool = True, specifiedDate: bool = False):
    try:
        spinner_element(driver)

        if set_Chart:
            chart_minMax(driver, chart_fullscreen)

        button_tradeModule(driver, module_Type="trade")
        
        # Retrieve the One Point Equal label data
        label_onePointsEqual = label_onePointEqual(driver, trade_type="trade")
        
        # Retrieve the current price based on order type and option
        current_price = get_current_price(driver, trade_type, option, partial_text="limit")

        # Input the size/volume
        input_size_volume(driver)
    
        calculate_limit_entryPrice(driver, trade_type, option, label_onePointsEqual, current_price, entryPrice_flag)
            
        if set_stopLoss:
            calculate_limit_stopLoss(driver, trade_type, sl_type, option, label_onePointsEqual, stopLoss_flag)

        if set_takeProfit: # if set_takeProfit is True
            calculate_limit_takeProfit(driver, trade_type, tp_type, option, label_onePointsEqual, takeProfit_flag)

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
                                                EDIT - MODIFY LIMIT ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def modify_limit_order(driver, trade_type, row_number, expiryType, expiryDate=None, targetMonth=None, hour_option=None, min_option=None, sl_type=None, tp_type=None, entryPrice_flag: bool = True, set_stopLoss: bool = True, stopLoss_flag: bool = True, set_takeProfit: bool = True, takeProfit_flag: bool = True, specifiedDate: bool = False):
    try:
        
        button_orderPanel_action(driver, trade_type, row_number)

        current_price = get_current_price(driver, trade_type)

        label_onePointsEqual = label_onePointEqual(driver, trade_type="edit")

        option = get_edit_order_label(driver)

        calculate_limit_entryPrice(driver, trade_type, option, label_onePointsEqual, current_price, entryPrice_flag)
            
        if set_stopLoss: # if set_stopLoss is true
            calculate_limit_stopLoss(driver, trade_type, sl_type, option, label_onePointsEqual, stopLoss_flag)

        if set_takeProfit: # if set_takeProfit is True
            calculate_limit_takeProfit(driver, trade_type, tp_type, option, label_onePointsEqual, takeProfit_flag)

        expiry(driver, trade_type, expiryType, expiryDate, targetMonth, hour_option, min_option, specifiedDate)
         
        button_trade_action(driver, trade_type)
    
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""