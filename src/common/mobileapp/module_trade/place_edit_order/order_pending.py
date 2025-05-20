from enums.main import ButtonModuleType, ExpiryType, TradeConstants, TradeDirectionOption, OrderExecutionType, AlertType

from constants.helper.error_handler import handle_exception
from constants.helper.element import populate_element_with_wait, spinner_element

# from common.mobileapp.module_chart.chart import chart_min_max
from common.mobileapp.module_trade.order_panel.order_panel_info import handle_track_close_edit
from common.mobileapp.module_trade.place_edit_order.price_related import get_current_price, get_edit_order_label, calculate_pending_entry_price, calculate_stop_limit_price, calculate_pending_stop_loss, calculate_pending_take_profit
from common.mobileapp.module_trade.order_placing_window.utils import get_label_one_point_equal, button_pre_trade, trade_placing_modal, input_size_volume, button_trade_action, expiry
from enums.main import ButtonModuleType, OrderExecutionType



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - PLACE STOP ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def trade_pending_order(driver, order_type: OrderExecutionType, option: TradeDirectionOption, expiry_type: ExpiryType, trade_type: ButtonModuleType = ButtonModuleType.TRADE, 
                      expiry_date=None, target_month=None, hour_option=None, min_option=None, sl_type=None, tp_type=None, 
                      trade_constants: TradeConstants = TradeConstants.NONE, entry_price_flag: AlertType = AlertType.POSITIVE, 
                      stop_loss_flag: AlertType = AlertType.POSITIVE, take_profit_flag: AlertType = AlertType.POSITIVE):
    try:

        spinner_element(driver)
        
        # Expanded the trade layout
        if TradeConstants.PRE_TRADE in trade_constants:
            button_pre_trade(driver)
            
        # Retrieve the current price based on order type and option
        current_price = get_current_price(driver, trade_type, option, order_type)
        
        trade_placing_modal(driver)

        # Retrieve the One Point Equal label data
        label_one_points_equal = get_label_one_point_equal(driver, trade_type=ButtonModuleType.TRADE)
        
        # Input the size/volume
        input_size_volume(driver)

        calculate_pending_entry_price(driver, trade_type, option, order_type, label_one_points_equal, current_price, entry_price_flag)

        # if set_stop_limit_price is true
        if order_type == OrderExecutionType.STOP_LIMIT:
            calculate_stop_limit_price(driver, trade_type, option, label_one_points_equal)

        # Set Stop Loss if specified or required        
        if TradeConstants.SET_STOP_LOSS in trade_constants or sl_type:
            calculate_pending_stop_loss(driver, trade_type, sl_type, option, label_one_points_equal, stop_loss_flag)

        # Set Take Profit if specified or required
        elif TradeConstants.SET_TAKE_PROFIT in trade_constants or tp_type:
            calculate_pending_take_profit(driver, trade_type, tp_type, option, label_one_points_equal, take_profit_flag)

        expiry(driver, trade_type, expiry_type, expiry_date, target_month, hour_option, min_option)
        
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

def modify_pending_order(driver, expiry_type: ExpiryType, order_type: OrderExecutionType, trade_type: ButtonModuleType = ButtonModuleType.EDIT,
                       expiry_date=None, target_month=None, hour_option=None, min_option=None, sl_type=None, tp_type=None, 
                       trade_constants: TradeConstants = TradeConstants.NONE, entry_price_flag: AlertType = AlertType.POSITIVE, 
                       stop_loss_flag: AlertType = AlertType.POSITIVE, take_profit_flag: AlertType = AlertType.POSITIVE):
    try:

        handle_track_close_edit(driver, trade_type)

        current_price = get_current_price(driver, trade_type)

        label_one_points_equal = get_label_one_point_equal(driver, trade_type)

        option = get_edit_order_label(driver)

        calculate_pending_entry_price(driver, trade_type, option, order_type, label_one_points_equal, current_price, entry_price_flag)

        # if set_stop_limit_price is true
        if order_type == OrderExecutionType.STOP_LIMIT:
            calculate_stop_limit_price(driver, trade_type, option, label_one_points_equal)

        # Set Stop Loss if specified or required        
        if TradeConstants.SET_STOP_LOSS in trade_constants or sl_type:
            calculate_pending_stop_loss(driver, trade_type, sl_type, option, label_one_points_equal, stop_loss_flag)
            
        # Set Take Profit if specified or required
        elif TradeConstants.SET_TAKE_PROFIT in trade_constants or tp_type:
            calculate_pending_take_profit(driver, trade_type, tp_type, option, label_one_points_equal, take_profit_flag)

        expiry(driver, trade_type, expiry_type, expiry_date, target_month, hour_option, min_option)
         
        button_trade_action(driver, trade_type)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""