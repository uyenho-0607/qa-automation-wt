import traceback

from constants.helper.driver import delay
from constants.helper.screenshot import take_screenshot
from constants.helper.element_android_app import populate_element_with_wait, spinner_element

from common.mobileapp.trade.chart import minMax_Chart
from common.mobileapp.trade.place_edit_order.price_related import get_current_price, get_edit_order_label, get_sl_point_distance, get_tp_point_distance, pointsDistance
from common.mobileapp.trade.orderPanel_info import button_orderPanel_action, extract_order_info
from common.mobileapp.trade.orderPlacingWindow import button_OCT_buy_sell_type, button_trade_action, fillPolicy_type, close_partialSize, handle_stopLoss, handle_takeProfit, input_oct_size_volume, input_size_volume, label_onePointEqual


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE MARKET STOP LOSS VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def calculate_stop_loss(driver, trade_type, sl_type, option, label_onePointsEqual, current_price):
    
    min_point_distance = pointsDistance(trade_type)
    
    stopLoss_point = get_sl_point_distance(option, trade_type)

    stopLoss_input = handle_stopLoss(driver, trade_type, sl_type)

    if sl_type == "price":
        if option in ["buy", "BUY"]:
            # stopLoss_value = Sell price - (One point equals * Minimum Point Distance)
            stopLoss_value = current_price - (label_onePointsEqual * min_point_distance)
            print("current price sl buy", current_price)

        if option in ["sell", "SELL"]:
            # stopLoss_value = Buy price + (One point equals * Minimum Point Distance)
            stopLoss_value = current_price + (label_onePointsEqual * min_point_distance)
            print("current price sl sell", current_price)

    elif sl_type == "points":
        if option in ["buy", "BUY"]:
            # stopLoss_value = (Sell price - Price field) / One point equal
            # stopLoss_value = int((current_price - low_price) / label_onePointsEqual)
            stopLoss_value = stopLoss_point
        
        if option in ["sell", "SELL"]:
            # stopLoss_value = (Price field - Buy price) / One point equal
            # stopLoss_value = int((high_price - current_price) / label_onePointsEqual)
            stopLoss_value = stopLoss_point

    # if trade_type == "edit":
    #     clear_input_field(stopLoss_input)
    print("sl value", stopLoss_value)
    populate_element_with_wait(driver, element=stopLoss_input, text=stopLoss_value)
    # take_screenshot(driver, f"{trade_type.capitalize()}_Stop_Loss")

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

    takeProfit_point = get_tp_point_distance(option, trade_type)

    takeProfit_input = handle_takeProfit(driver, trade_type, tp_type)
    
    if tp_type == "price":
        if option in ["buy", "BUY"]:
            # takeProfit_value = Sell price + (One point equals * Minimum Point Distance)
            takeProfit_value = current_price + (label_onePointsEqual * min_point_distance)
            print("current price tp buy", current_price)
                
        if option in ["sell", "SELL"]:
            # takeProfit_value = Buy price - (One point equals * Minimum Point Distance)
            takeProfit_value = current_price - (label_onePointsEqual * min_point_distance)
            print("current price tp sell", current_price)

    elif tp_type == "points":
        if option in ["buy", "BUY"]:
            # takeProfit_value = (Price field - Sell price) / One point equal
            # takeProfit_value = int((high_price - current_price) / label_onePointsEqual)
            takeProfit_value = takeProfit_point

        if option in ["sell", "SELL"]:
            # takeProfit_value = (Buy price - Price field) / One point equal
            # takeProfit_value = int((current_price - low_price) / label_onePointsEqual)
            takeProfit_value = takeProfit_point
    
    print("tp value", takeProfit_value)
    populate_element_with_wait(driver, element=takeProfit_input, text=takeProfit_value)
    # take_screenshot(driver, f"{trade_type.capitalize()}_Take_Profit")

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
            minMax_Chart(driver, chart_fullscreen)
        
        input_oct_size_volume(driver)
        
        button_OCT_buy_sell_type(driver, option)

        # return high_price, low_price

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
                                                TRADE - PLACE MARKET ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def trade_market_order(driver, trade_type, option, chart_fullscreen=None, fill_policy=None, sl_type=None, tp_type=None, set_fillPolicy: bool = False, set_stopLoss: bool = True, set_takeProfit: bool = True, set_Chart: bool = False):
    try:

        spinner_element(driver)

        if set_Chart:
            minMax_Chart(driver, chart_fullscreen)
            
        # Retrieve the current price based on order type and option
        current_price = get_current_price(driver, trade_type, option, partial_text="market")
        
        # Retrieve the One Point Equal label data
        label_onePointsEqual = label_onePointEqual(driver, trade_type="trade")
        
        # Input the size/volume
        input_size_volume(driver)

        # Select the Fill Policy
        if set_fillPolicy:
            fillPolicy_type(driver, trade_type, fill_policy)

        if set_stopLoss: # if set_stopLoss is True
            calculate_stop_loss(driver, trade_type, sl_type, option, label_onePointsEqual, current_price)

        if set_takeProfit: # if set_takeProfit is True
            calculate_take_profit(driver, trade_type, tp_type, option, label_onePointsEqual, current_price)

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
                                                EDIT - MODIFY MARKET ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def modify_market_order(driver, trade_type, row_numbers, sl_type=None, tp_type=None, set_stopLoss: bool = True, set_takeProfit: bool = True): 
    try:
                
        # Perform order panel action based on trade type and row numbers
        button_orderPanel_action(driver, trade_type, row_numbers)
        
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

        # return orderIDs, trade_order_df
        
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
                                                CLOSE - MARKET ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# For closing market and deleting pending order
def close_delete_order(driver, tab_order_type, section_name, row_number, order_action, close_button=None, fillPolicy_type=None, set_marketSize:bool = False, fillPolicy: bool = False, clearField: bool = False, delete_button: bool = False):
    try:
        # Retrieve the table info    
        orderIDs, orderPanel_df = extract_order_info(driver, tab_order_type, section_name, row_number)
        
        # Clicking on the action (Edit / Close / Delete)
        button_orderPanel_action(driver, order_action, row_number, delete_button)
        
        if set_marketSize:
            delay(0.5)
            close_partialSize(driver, close_button, fillPolicy_type, fillPolicy, clearField)
        
        return orderIDs, orderPanel_df

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "Exception Screenshot")
        # Handle potential errors during element interaction
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""