from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception
from constants.helper.element import populate_element_with_wait, spinner_element

from common.mobileweb.module_chart.chart import chart_minMax
from common.mobileweb.module_trade.order_panel.orderPanel_info import button_orderPanel_action
from common.mobileweb.module_trade.place_edit_order.price_related import get_current_price, get_edit_order_label, get_sl_point_distance, get_tp_point_distance, pointsDistance
from common.mobileweb.module_trade.order_placing_window.utils import label_onePointEqual, button_preTrade, trade_placingModal, input_size_volume, button_OCT_buy_sell_type, fillPolicy_type, handle_stopLoss, handle_takeProfit, button_trade_action, handle_stopLoss, handle_takeProfit, close_partialSize
# from common.mobileweb.module_trade.order_placing_window.opw_button_action import button_preTrade, trade_placingModal


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
        if option in ["buy", "BUY", "sell", "SELL"]:
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
        if option in ["buy", "BUY", "sell", "SELL"]:
            takeProfit_value = takeProfit_point
    
    print("tp value", takeProfit_value)
    populate_element_with_wait(driver, element=takeProfit_input, text=takeProfit_value)

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

def trade_oct_market_order(driver, option, chart_fullscreen=None, set_Chart: bool = False):
    try:
        
        spinner_element(driver)

        if set_Chart:
            chart_minMax(driver, chart_fullscreen)
        
        # Input the size/volume
        input_size_volume(driver, desired_state="units", swap=False)
        
        button_OCT_buy_sell_type(driver, option)

    except Exception as e:
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


def trade_market_order(driver, trade_type, option, chart_fullscreen=None, fill_policy=None, sl_type=None, tp_type=None, set_Chart: bool = False, pre_trade: bool = False, set_fillPolicy: bool = False, set_stopLoss: bool = True, set_takeProfit: bool = True):
    try:

        spinner_element(driver)

        if set_Chart:
            chart_minMax(driver, chart_fullscreen)
        
        if pre_trade:
            button_preTrade(driver)
        
        # Retrieve the current price based on order type and option
        current_price = get_current_price(driver, trade_type, option, partial_text="market")
        
        trade_placingModal(driver)

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

def modify_market_order(driver, trade_type, row_number, sl_type=None, tp_type=None, set_stopLoss: bool = True, set_takeProfit: bool = True): 
    try:
                
        # Perform order panel action based on trade type and row numbers
        button_orderPanel_action(driver, trade_type, row_number)
        
        # spinner_element(driver)
        
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
        

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CLOSE - MARKET ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# For closing market and deleting pending order
def close_delete_order(driver, row_number, order_action, set_marketSize:bool = False, fillPolicy: bool = False, clearField: bool = False, delete_button: bool = False):
    
    try:
        
        # Clicking on the action (Edit / Close / Delete)
        button_orderPanel_action(driver, order_action, row_number, delete_button)
        
        if set_marketSize:
            # delay(0.5)
            close_partialSize(driver, fillPolicy, clearField)

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""