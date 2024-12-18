import traceback

from constants.helper.element_android_app import populate_element_with_wait, spinner_element
from constants.helper.screenshot import take_screenshot

from common.mobileapp.trade.orderPanel_info import button_orderPanel_action
from common.mobileapp.trade.orderPlacingWindow import button_trade_action, expiry, handle_entryPrice, handle_stopLoss, handle_takeProfit, input_size_volume, label_onePointEqual
from common.mobileapp.trade.chart import minMax_Chart
from common.mobileapp.trade.place_edit_order.price_related import get_current_price, get_edit_order_label, get_random_point_distance, get_sl_point_distance, get_tp_point_distance, pointsDistance


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE STOP ENTRY PRICE VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


# Define a global variable
entryPrice = None

def calculate_stop_entryPrice(driver, trade_type, option, label_onePointsEqual, current_price):
    global entryPrice  # Declare the use of the global variable

    entryPrice_input = handle_entryPrice(driver, trade_type)

    min_point_distance = get_random_point_distance(option, trade_type)
    
    if option in ["buy", "BUY STOP"]:
        # EntryPrice: Buy price + (One point equals * Minimum Point Distance)
        entryPrice = current_price + (label_onePointsEqual * min_point_distance)
        
    elif option in ["sell", "SELL STOP"]:
        # EntryPrice = Sell price - (One point equals * Minimum Point Distance)
        entryPrice = current_price - (label_onePointsEqual * min_point_distance)
    
    populate_element_with_wait(driver, element=entryPrice_input, text=entryPrice)

    print("Stop Entry Price Value", entryPrice)
    return entryPrice


# To store the Stop Entry Price variable
def store_stop_entryPrice():
    global entryPrice  # Declare the use of the global variable
    print("Stored Stop Entry Price Value:", entryPrice)
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

    stopLoss_point = get_sl_point_distance(option, trade_type)

    entryPrice_value = store_stop_entryPrice()
    
    stopLoss_input = handle_stopLoss(driver, trade_type, sl_type)

    if sl_type == "price":
        if option in ["buy", "BUY STOP"]:
            # stopLoss_value = Price(S) - (One point equals * Minimum Point Distance)
            stopLoss_value = entryPrice_value - (label_onePointsEqual * min_point_distance)
            
        elif option in ["sell", "SELL STOP"]:
            # stopLoss_value = Price(S) + (One point equals * Minimum Point Distance)
            stopLoss_value = entryPrice_value + (label_onePointsEqual * min_point_distance)
                    
    elif sl_type == "points":
        if option in ["buy", "BUY STOP"]:
            # stopLoss_value = (Price(S) - Price field) / One point equal
            # stopLoss_value = int((entryPrice_value - low_price) / label_onePointsEqual)
            stopLoss_value = stopLoss_point
        
        elif option in ["sell", "SELL STOP"]:
            # stopLoss_value = (Price field - Price(S)) / One point equal
            # stopLoss_value = int((high_price - entryPrice_value) / label_onePointsEqual)
            stopLoss_value = stopLoss_point

    populate_element_with_wait(driver, element=stopLoss_input, text=stopLoss_value)
    # take_screenshot(driver, f"{trade_type.capitalize()}_Stop_Loss")

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

    takeProfit_point = get_tp_point_distance(option, trade_type)

    entryPrice_value = store_stop_entryPrice()

    takeProfit_input = handle_takeProfit(driver, trade_type, tp_type)

    if tp_type == "price":
        if option in ["buy", "BUY STOP"]:
            # takeProfit_value = Price(S) + (One point equals * Minimum Point Distance)
            takeProfit_value = entryPrice_value + (label_onePointsEqual * min_point_distance)

        elif option in ["sell", "SELL STOP"]:
            # takeProfit_value = Price(S) - (One point equals * Minimum Point Distance)
            takeProfit_value = entryPrice_value - (label_onePointsEqual * min_point_distance)
                    
    elif tp_type == "points":
        if option in ["buy", "BUY STOP"]:
            # takeProfit_value = (Price field - Price(S)) / One point equal
            # takeProfit_value = int((high_price - entryPrice_value) / label_onePointsEqual)
            takeProfit_value = takeProfit_point
            
        elif option in ["sell", "SELL STOP"]:
            # takeProfit_value = (Price(S) - Price field) / One point equal
            # takeProfit_value = int((entryPrice_value - low_price) / label_onePointsEqual)
            takeProfit_value = takeProfit_point
        
    populate_element_with_wait(driver, element=takeProfit_input, text=takeProfit_value)
    # take_screenshot(driver, f"{trade_type.capitalize()}_Take_Profit")

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

def trade_stop_order(driver, trade_type, option, expiryType, expiryDate=None, targetMonth=None, hour_option=None, min_option=None, sl_type=None, tp_type=None, chart_fullscreen=None, set_Chart: bool = False, set_entryPrice: bool = True, set_stopLoss: bool = True, set_takeProfit: bool = True, specifiedDate: bool = False):
    try:

        spinner_element(driver)

        if set_Chart:
            minMax_Chart(driver, chart_fullscreen)
        
        # Retrieve the current price based on order type and option
        current_price = get_current_price(driver, trade_type, option, partial_text="stop")
        
        # Retrieve the One Point Equal label data
        label_onePointsEqual = label_onePointEqual(driver, trade_type="trade")
        
        # Input the size/volume
        input_size_volume(driver)

        if set_entryPrice: # if set_entryPrice is true
            calculate_stop_entryPrice(driver, trade_type, option, label_onePointsEqual, current_price)
            
        if set_stopLoss:
            # calculate_stop_stopLoss(driver, trade_type, sl_type, option, label_onePointsEqual, current_price, high_price, low_price)
            calculate_stop_stopLoss(driver, trade_type, sl_type, option, label_onePointsEqual)

        if set_takeProfit: # if set_takeProfit is True
            # calculate_stop_takeProfit(driver, trade_type, tp_type, option, label_onePointsEqual, current_price, high_price, low_price)
            calculate_stop_takeProfit(driver, trade_type, tp_type, option, label_onePointsEqual)

        expiry(driver, trade_type, expiryType, expiryDate, targetMonth, hour_option, min_option, specifiedDate)
        
        button_trade_action(driver, trade_type)
    
    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                EDIT - MODIFY STOP ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def modify_stop_order(driver, trade_type, row_number, expiryType, expiryDate=None, targetMonth=None, hour_option=None, min_option=None, sl_type=None, tp_type=None, set_entryPrice:bool = True, set_stopLoss: bool = True, set_takeProfit: bool = True, specifiedDate: bool = False):
    try:

        button_orderPanel_action(driver, trade_type, row_number)

        current_price = float(get_current_price(driver, trade_type))

        # label_onePointsEqual = editlabel_onePointEqual(driver)
        label_onePointsEqual = label_onePointEqual(driver, trade_type="edit")
        
        option = get_edit_order_label(driver)

        if set_entryPrice: # if set_entryPrice is true
            calculate_stop_entryPrice(driver, trade_type, option, label_onePointsEqual, current_price)
            
        if set_stopLoss:
            calculate_stop_stopLoss(driver, trade_type, sl_type, option, label_onePointsEqual)

        if set_takeProfit: # if set_takeProfit is True
            calculate_stop_takeProfit(driver, trade_type, tp_type, option, label_onePointsEqual)

        expiry(driver, trade_type, expiryType, expiryDate, targetMonth, hour_option, min_option, specifiedDate)
         
        button_trade_action(driver, trade_type)

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""