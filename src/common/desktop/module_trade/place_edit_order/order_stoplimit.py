from enums.main import ButtonModuleType, ExpiryType, TradeConstants, TradeDirectionOption, OrderExecutionType, AlertType

from constants.helper.error_handler import handle_exception
from constants.helper.element import spinner_element

from common.desktop.module_chart.chart import chart_minMax
from common.desktop.module_trade.order_panel.order_panel_info import handle_track_close_edit
from common.desktop.module_trade.order_placing_window.utils import button_trade_module, get_label_one_point_equal, input_size_volume, expiry, button_trade_action
from common.desktop.module_trade.place_edit_order.price_related import  get_current_price, get_edit_order_label, calculate_pending_entry_price, calculate_stopLimit_Price, calculate_pending_stop_loss, calculate_pending_take_profit


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - PLACE STOP LIMIT ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def trade_stop_limit_order(driver,  option: TradeDirectionOption, expiry_type: ExpiryType, trade_type: ButtonModuleType = ButtonModuleType.TRADE, 
                          order_type: OrderExecutionType = OrderExecutionType.STOP_LIMIT,
                          expiry_date=None, target_month=None, hour_option=None, min_option=None, sl_type=None, tp_type=None, chart_fullscreen=None, 
                          trade_constants: TradeConstants = TradeConstants.NONE, entry_price_flag: AlertType = AlertType.POSITIVE, 
                          stopLimitPrice_flag: AlertType = AlertType.POSITIVE, stop_loss_flag: AlertType = AlertType.POSITIVE, take_profit_flag: AlertType = AlertType.POSITIVE):
    try:
        
        spinner_element(driver)

        if TradeConstants.SET_CHART in trade_constants or chart_fullscreen:
            chart_minMax(driver, chart_fullscreen)

        button_trade_module(driver, trade_type)

        # Retrieve the One Point Equal label data
        label_one_points_equal = get_label_one_point_equal(driver, trade_type)
        
        # Retrieve the current price based on order type and option
        current_price = get_current_price(driver, trade_type, option, order_type=OrderExecutionType.STOP_LIMIT)

        # Input the size/volume
        input_size_volume(driver)
        
        calculate_pending_entry_price(driver, trade_type, option, order_type, label_one_points_equal, current_price, entry_price_flag)

        calculate_stopLimit_Price(driver, trade_type, option, label_one_points_equal, stopLimitPrice_flag)

        # Set Stop Loss if specified or required        
        if TradeConstants.SET_STOP_LOSS in trade_constants or sl_type:
            calculate_pending_stop_loss(driver, trade_type, sl_type, option, label_one_points_equal, stop_loss_flag, is_stopLimit=True)

        # Set Take Profit if specified or required
        if TradeConstants.SET_TAKE_PROFIT in trade_constants or tp_type:
            calculate_pending_take_profit(driver, trade_type, tp_type, option, label_one_points_equal, take_profit_flag, is_stopLimit=True)

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
                                                EDIT - MODIFY STOP LIMIT ORDER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def modify_stop_limit_order(driver, expiry_type: ExpiryType, trade_type: ButtonModuleType = ButtonModuleType.EDIT, 
                           order_type: OrderExecutionType = OrderExecutionType.STOP_LIMIT,
                           expiry_date=None, target_month=None, hour_option=None, min_option=None, sl_type=None, tp_type=None, 
                           trade_constants: TradeConstants = TradeConstants.NONE, entry_price_flag: AlertType = AlertType.POSITIVE,
                           stopLimitPrice_flag: AlertType = AlertType.POSITIVE, stop_loss_flag: AlertType = AlertType.POSITIVE, take_profit_flag: AlertType = AlertType.POSITIVE):
    try:
        
        handle_track_close_edit(driver, trade_type)

        current_price = get_current_price(driver, trade_type)

        label_one_points_equal = get_label_one_point_equal(driver, trade_type=ButtonModuleType.EDIT)

        # To retrieve the order type value
        option = get_edit_order_label(driver)

        calculate_pending_entry_price(driver, trade_type, option, order_type, label_one_points_equal, current_price, entry_price_flag)

        calculate_stopLimit_Price(driver, trade_type, option, label_one_points_equal, stopLimitPrice_flag)

        # Set Stop Loss if specified or required        
        if TradeConstants.SET_STOP_LOSS in trade_constants or sl_type:
            calculate_pending_stop_loss(driver, trade_type, sl_type, option, label_one_points_equal, stop_loss_flag, is_stopLimit=True)

        # Set Take Profit if specified or required
        if TradeConstants.SET_TAKE_PROFIT in trade_constants or tp_type:
            calculate_pending_take_profit(driver, trade_type, tp_type, option, label_one_points_equal, take_profit_flag, is_stopLimit=True)

        expiry(driver, trade_type, expiry_type, expiry_date, target_month, hour_option, min_option)
         
        button_trade_action(driver, trade_type)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""