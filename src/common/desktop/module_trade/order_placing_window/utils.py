
from common.desktop.module_trade.order_placing_window.module_OCT import toggle_radioButton_OCT
from common.desktop.module_trade.order_placing_window.module_size_volume import swap_units_volume, input_size_volume, close_partialSize, btn_minMax_size
from common.desktop.module_trade.order_placing_window.module_fill_policy import fillPolicy_type
from common.desktop.module_trade.order_placing_window.module_entry_price import handle_entryPrice, btn_minMax_price 
from common.desktop.module_trade.order_placing_window.module_stopLimitPrice import handle_stopLimitPrice, btn_minMax_stopLimitPrice 
from common.desktop.module_trade.order_placing_window.module_stopLoss import handle_stopLoss, btn_minMax_stopLoss
from common.desktop.module_trade.order_placing_window.module_takeProfit import handle_takeProfit, btn_minMax_takeProfit
from common.desktop.module_trade.order_placing_window.module_expiry import select_specified_date, select_time_option, select_specified_date_and_time, expiry
from common.desktop.module_trade.order_placing_window.module_confirmation_modal import trade_ordersConfirmationDetails
from common.desktop.module_trade.order_placing_window.opw_button_action import label_onePointEqual, button_tradeModule, button_buy_sell_type, button_OCT_buy_sell_type, dropdown_orderType, button_trade_action



__all__ = [
    
    # Toggle OCT
    'toggle_radioButton_OCT',
    
    # Size / Volume
    'swap_units_volume',
    'input_size_volume',
    'close_partialSize',
    'btn_minMax_size',
    
    # Fill Policy
    'fillPolicy_type',
    
    # Entry Price
    'handle_entryPrice',
    'btn_minMax_price',
        
    # Stop Limit Price
    'handle_stopLimitPrice',
    'btn_minMax_stopLimitPrice',

    # Stop Loss
    'handle_stopLoss',
    'btn_minMax_stopLoss',
    # 'calculate_stop_loss',
    
    # Take Profit
    'handle_takeProfit',
    'btn_minMax_takeProfit',
    # 'calculate_takeProfit',
    
    # Expiry
    'select_specified_date',
    'select_time_option',
    'select_specified_date_and_time',
    'expiry',
    
    # Trade / Edit Confirmation Modal
    'trade_ordersConfirmationDetails',
    
    # Button Actions
    'label_onePointEqual',
    'button_tradeModule',
    'button_buy_sell_type',
    'button_OCT_buy_sell_type',
    'dropdown_orderType',
    'button_trade_action'
]