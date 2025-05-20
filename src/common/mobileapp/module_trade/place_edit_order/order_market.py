from enums.main import SwapOptions, ButtonModuleType, SLTPOption, TradeConstants, TradeDirectionOption, OrderExecutionType, AlertType

from constants.helper.error_handler import handle_exception
from constants.helper.element import populate_element_with_wait, spinner_element

# from common.mobileapp.module_chart.chart import chart_min_max
from common.mobileapp.module_trade.order_panel.order_panel_info import handle_track_close_edit
from common.mobileapp.module_trade.place_edit_order.price_related import get_current_price, get_edit_order_label, get_sl_point_distance, get_tp_point_distance, generate_min_point_disatance
from common.mobileapp.module_trade.order_placing_window.utils import get_label_one_point_equal, button_pre_trade, trade_placing_modal, input_size_volume, oct_buy_sell_type, fill_policy_type, handle_stop_loss, handle_take_profit, button_trade_action, close_partial_size


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE MARKET STOP LOSS VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def calculate_stop_loss(driver, trade_type: ButtonModuleType, sl_type: SLTPOption, option: TradeDirectionOption, label_one_points_equal, current_price, stop_loss_flag: AlertType = AlertType.POSITIVE):
    
    min_point_distance = generate_min_point_disatance(trade_type)
    
    stop_loss_point = get_sl_point_distance(option, trade_type)

    stop_loss_input = handle_stop_loss(driver, trade_type, sl_type)

    # Define the calculation logic for BUY and SELL options
    price_adjustment = label_one_points_equal * min_point_distance
    # BUY = Sell Price - (One point equals * Minimum Point Distance)
    # SELL = Buy Price + (One point equals * Minimum Point Distance)

    direction_map = {
        TradeDirectionOption.BUY: current_price - price_adjustment,
        TradeDirectionOption.SELL: current_price + price_adjustment
    }

    # For Positive scenario, use the price adjustment map
    if stop_loss_flag == AlertType.POSITIVE:
        if sl_type == SLTPOption.PRICE:
            stop_loss_value = direction_map.get(option, stop_loss_point)  # Default to stop_loss_point if not found
        else:
            stop_loss_value = stop_loss_point
    else:
        # For Negative scenario, reverse the price adjustment
        reverse_direction_map = {
            TradeDirectionOption.BUY: current_price + price_adjustment,
            TradeDirectionOption.SELL: current_price - price_adjustment
        }
        
        stop_loss_value = reverse_direction_map.get(option, stop_loss_point)  # Default to stop_loss_point if not found

    # Populate the element with the calculated stop loss value
    populate_element_with_wait(driver, element=stop_loss_input, text=stop_loss_value)

    return stop_loss_value

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE MARKET TAKE PROFIT VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def calculate_take_profit(driver, trade_type: ButtonModuleType, tp_type: SLTPOption, option: TradeDirectionOption, label_one_points_equal, current_price, take_profit_flag: AlertType = AlertType.POSITIVE):
    # Common logic
    min_point_distance = generate_min_point_disatance(trade_type)
    
    take_profit_point = get_tp_point_distance(option, trade_type)
    
    take_profit_input = handle_take_profit(driver, trade_type, tp_type)

    # Define the calculation logic for BUY and SELL options
    price_adjustment = label_one_points_equal * min_point_distance
    # BUY = Sell Price + (One point equals * Minimum Point Distance)
    # SELL = Buy Price - (One point equals * Minimum Point Distance)
    
    direction_map = {
        TradeDirectionOption.BUY: current_price + price_adjustment,
        TradeDirectionOption.SELL: current_price - price_adjustment,
    }

    # For Positive scenario, use the price adjustment map
    if take_profit_flag == AlertType.POSITIVE:
        if tp_type == SLTPOption.PRICE:
            take_profit_value = direction_map.get(option, take_profit_point)  # Default to stop_loss_point if not found
        else:
            take_profit_value = take_profit_point
    else:
        # For Negative scenario, reverse the price adjustment
        reverse_direction_map = {
            TradeDirectionOption.BUY: current_price - price_adjustment,
            TradeDirectionOption.SELL: current_price + price_adjustment,
        }
        
        take_profit_value = reverse_direction_map.get(option, take_profit_point)  # Default to stop_loss_point if not found

    # Populate the element with the calculated stop loss value
    populate_element_with_wait(driver, element=take_profit_input, text=take_profit_value)

    return take_profit_value


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - OCT PLACE MARKET ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def trade_oct_market_order(driver, option: TradeDirectionOption):
    try:
        
        spinner_element(driver)
        
        # Input the size/volume
        input_size_volume(driver, desired_state=SwapOptions.UNITS, swap=False)
        
        oct_buy_sell_type(driver, option)

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


def trade_market_order(driver, option: TradeDirectionOption, trade_type: ButtonModuleType = ButtonModuleType.TRADE, sl_type=None, tp_type=None, trade_constants: TradeConstants = TradeConstants.NONE):
    
    try:

        # Wait for any loading spinner to disappear
        spinner_element(driver)
        
        # Perform pre-trade actions if required
        if TradeConstants.PRE_TRADE in trade_constants:
            button_pre_trade(driver)

        # Retrieve the current market price based on the order type and direction
        current_price = get_current_price(driver, trade_type, option, order_type=OrderExecutionType.MARKET)
        
        trade_placing_modal(driver)

        # Retrieve the value of "One Point Equal" label
        label_one_points_equal = get_label_one_point_equal(driver, trade_type)

        # Input the size/volume
        input_size_volume(driver)
        
        # Set the Fill Policy if required
        if TradeConstants.SET_FILL_POLICY in trade_constants:
            fill_policy_type(driver, trade_type)
        
        # Set Stop Loss if specified or required
        elif TradeConstants.SET_STOP_LOSS in trade_constants or sl_type:
            calculate_stop_loss(driver, trade_type, sl_type, option, label_one_points_equal, current_price)

        # Set Take Profit if specified or required
        elif TradeConstants.SET_TAKE_PROFIT in trade_constants or tp_type:
            calculate_take_profit(driver, trade_type, tp_type, option, label_one_points_equal, current_price)

        # Execute the trade action
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

def modify_market_order(driver, trade_type: ButtonModuleType = ButtonModuleType.EDIT, sl_type=None, tp_type=None, trade_constants: TradeConstants = TradeConstants.NONE): 
    try:
                
        # Perform order panel action based on trade type
        handle_track_close_edit(driver, trade_type)
        
        # Get the current price from the market
        current_price = get_current_price(driver, trade_type)
        
        # Retrieve the label indicating points equal
        label_one_points_equal = get_label_one_point_equal(driver, trade_type)
        
        # Get the edit order type label
        option = get_edit_order_label(driver)

        if TradeConstants.SET_STOP_LOSS in trade_constants or sl_type: # if set_stopLoss is True
            calculate_stop_loss(driver, trade_type, sl_type, option, label_one_points_equal, current_price)

        elif TradeConstants.SET_TAKE_PROFIT in trade_constants or tp_type: # if set_takeProfit is True
            calculate_take_profit(driver, trade_type, tp_type, option, label_one_points_equal, current_price)
            
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
def close_delete_order(driver, trade_type: ButtonModuleType = ButtonModuleType.CLOSE, close_options: TradeConstants = TradeConstants.NONE):
    
    try:
        
        # Clicking on the action (Edit / Close / Delete)
        handle_track_close_edit(driver, trade_type, close_options)
        
        # if set_market_size:
        if TradeConstants.SET_CLOSE_MARKET_SIZE in close_options:
            # delay(0.5)
            close_partial_size(driver, close_options)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""