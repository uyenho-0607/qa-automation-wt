from enums.main import ButtonModuleType, SLTPOption, TradeConstants, TradeDirectionOption, OrderExecutionType, AlertType


from constants.helper.error_handler import handle_exception
from constants.helper.element import spinner_element, populate_element

from common.desktop.module_chart.chart import chart_min_max
from common.desktop.module_trade.order_panel.order_panel_info import handle_track_close_edit
from common.desktop.module_trade.place_edit_order.price_related import get_current_price, get_edit_order_label, get_sl_point_distance, get_tp_point_distance, generate_min_point_disatance
from common.desktop.module_trade.order_placing_window.utils import oct_buy_sell_type, verify_volume_min_max_buttons, button_trade_module, get_label_one_point_equal, input_size_volume, fill_policy_type, handle_stop_loss, handle_take_profit, button_trade_action, handle_stop_loss, handle_take_profit, close_partial_size
from common.desktop.module_trade.order_placing_window.module_size_volume import verify_button_behavior_at_min_max, verify_invalid_size_volume_input

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE MARKET STOP LOSS VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def calculate_stop_loss(driver, trade_type: ButtonModuleType, sl_type: SLTPOption, option: TradeDirectionOption, label_one_points_equal, current_price, stop_loss_flag: AlertType = AlertType.POSITIVE):
    # Common logic
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
    populate_element(element=stop_loss_input, text=stop_loss_value)

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
    populate_element(element=take_profit_input, text=take_profit_value)

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

def trade_oct_market_order(driver, option: TradeDirectionOption, chart_fullscreen=None, trade_constants: TradeConstants = TradeConstants.NONE):
    try:
        
        spinner_element(driver)

        # if set_Chart:
        if TradeConstants.SET_CHART in trade_constants or chart_fullscreen:
            chart_min_max(driver, chart_fullscreen)

        # if set_OCT:
        if TradeConstants.SET_OCT in trade_constants:
            button_trade_module(driver, trade_type=ButtonModuleType.ONE_CLICK_TRADING)
        
        # Input the size/volume
        input_size_volume(driver)
        
        option = oct_buy_sell_type(driver, option)
        
        return option

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


def trade_market_order(driver, option: TradeDirectionOption, trade_type: ButtonModuleType = ButtonModuleType.TRADE, chart_fullscreen=None, sl_type: SLTPOption = None, tp_type: SLTPOption = None, trade_constants: TradeConstants = TradeConstants.NONE, stop_loss_flag: AlertType = AlertType.POSITIVE, take_profit_flag: AlertType = AlertType.POSITIVE):
    try:

        spinner_element(driver)

        if TradeConstants.SET_CHART in trade_constants or chart_fullscreen:
            chart_min_max(driver, chart_fullscreen)
        
        button_trade_module(driver, trade_type)

        # Retrieve the One Point Equal label data
        label_one_points_equal = get_label_one_point_equal(driver, trade_type)

        # Retrieve the current price based on order type and option
        current_price = get_current_price(driver, trade_type, option, order_type=OrderExecutionType.MARKET)

        # Input the size/volume
        input_size_volume(driver)

        # Set the Fill Policy if required
        if TradeConstants.SET_FILL_POLICY in trade_constants:
            fill_policy_type(driver, trade_type)

        # Set Stop Loss if specified or required
        if TradeConstants.SET_STOP_LOSS in trade_constants or sl_type:
            calculate_stop_loss(driver, trade_type, sl_type, option, label_one_points_equal, current_price, stop_loss_flag)

        # Set Take Profit if specified or required
        if TradeConstants.SET_TAKE_PROFIT in trade_constants or tp_type:
            calculate_take_profit(driver, trade_type, tp_type, option, label_one_points_equal, current_price, take_profit_flag)

        button_trade_action(driver, trade_type)
        
        spinner_element(driver)

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

def modify_market_order(driver, trade_type: ButtonModuleType = ButtonModuleType.EDIT, sl_type: SLTPOption = None, tp_type: SLTPOption = None, trade_constants: TradeConstants = TradeConstants.NONE, stop_loss_flag: AlertType = AlertType.POSITIVE, take_profit_flag: AlertType = AlertType.POSITIVE):
    try:

        # Perform order panel action based on trade type and row numbers
        handle_track_close_edit(driver, trade_type)
        
        # Get the current price from the market
        current_price = get_current_price(driver, trade_type)
        
        # Retrieve the label indicating points equal
        label_one_points_equal = get_label_one_point_equal(driver, trade_type)

        # Get the edit order type label
        option = get_edit_order_label(driver)

        if TradeConstants.SET_STOP_LOSS in trade_constants or sl_type:
            calculate_stop_loss(driver, trade_type, sl_type, option, label_one_points_equal, current_price, stop_loss_flag)

        if TradeConstants.SET_TAKE_PROFIT in trade_constants or tp_type:
            calculate_take_profit(driver, trade_type, tp_type, option, label_one_points_equal, current_price, take_profit_flag)
            
        # Perform the trade action (Update Order)
        button_trade_action(driver, trade_type)
        
        spinner_element(driver)
        
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
def close_delete_order(driver, actions: list = None, trade_type: ButtonModuleType = ButtonModuleType.CLOSE, close_options: TradeConstants = TradeConstants.NONE):
    try:

        spinner_element(driver)
        
        # Clicking on the action (Edit / Close / Delete)
        handle_track_close_edit(driver, trade_type)
        
        # if set_market_size:
        if TradeConstants.SET_CLOSE_MARKET_SIZE in close_options:
            close_partial_size(driver, close_options)
        
        # Test the (- / +) button, (Min / Max) button and validation check
        # if set_negMarket:
        if TradeConstants.SET_NEG_MARKET in close_options:
            _, lot_size, vol_step = button_trade_module(driver, trade_type=ButtonModuleType.SPECIFICATION)

            verify_button_behavior_at_min_max(driver, trade_type, lot_size=lot_size)
            verify_volume_min_max_buttons(driver, trade_type, actions, size_volume_step=vol_step)
            verify_invalid_size_volume_input(driver, trade_type)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""