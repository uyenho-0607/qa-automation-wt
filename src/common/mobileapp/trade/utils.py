# Chart
from common.mobileapp.trade.chart import minMax_Chart, trade_close

# Snackbar Message
from common.mobileapp.trade.snackbar import get_trade_snackbar_banner, get_bulk_snackbar_banner, get_neg_snackbar_banner

# Order Placing Window
from common.mobileapp.trade.orderPlacingWindow import toggle_radioButton_OCT, label_onePointEqual, button_buy_sell_type, button_OCT_buy_sell_type, dropdown_orderType, swap_units_volume, swap_units_volume, btn_minMax_size, input_size_volume, close_partialSize, fillPolicy_type, handle_entryPrice, btn_minMax_price, manage_entryPrice, handle_stopLoss, handle_stopLimitPrice, btn_minMax_stopLimitPrice, manage_stopLimitPrice, btn_minMax_stopLoss, manage_stopLoss, handle_takeProfit, btn_minMax_takeProfit, manage_takeProfit, select_specified_date, select_time_option, select_specified_date_and_time, expiry, button_trade_action, trade_ordersConfirmationDetails, compare_dataframes, process_and_print_data

# Place / Edit Order
from common.mobileapp.trade.place_edit_order.price_related import get_random_point_distance, pointsDistance, get_edit_order_label, get_market_high_low_prices, get_current_price

from common.mobileapp.trade.place_edit_order.order_market import calculate_stop_loss, calculate_take_profit, trade_oct_market_order, trade_market_order, modify_market_order, close_delete_order

from common.mobileapp.trade.place_edit_order.order_limit import calculate_limit_entryPrice, calculate_limit_stopLoss, calculate_limit_takeProfit, trade_limit_order, modify_limit_order

from common.mobileapp.trade.place_edit_order.order_stop import calculate_stop_entryPrice, calculate_stop_stopLoss, calculate_stop_takeProfit, trade_stop_order, modify_stop_order

from common.mobileapp.trade.place_edit_order.order_stoplimit import calculate_stopLimit_entryPrice, calculate_stopLimit_Price, calculate_stopLimit_stopLoss, calculate_stopLimit_takeProfit, trade_stopLimit_order, modify_stopLimit_order

# Order Panel
from common.mobileapp.trade.orderPanel_info import asset_symbolName, type_orderPanel, button_orderPanel_action, get_orderID, extract_order_info, get_order_panel_name, review_pending_orderIDs, check_orderIDs_in_table

# Notification
from common.mobileapp.trade.notification import notification_type, get_orderNotification_msg, get_noti_ordersDetails, process_order_notifications

# Bulk Close / Delete
from common.mobileapp.trade.bulk_close_delete import extract_rgb_from_color, process_profit_loss, button_bulk_operation

# Order History
from common.mobileapp.trade.order_history import calendar_datePicker, OH_closeDate

# Common Function
from common.mobileapp.trade.common_function import get_table_body, get_table_headers


__all__ = [
    
    # """
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    #                                                 ORDER - CHART
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    # """

    # Chart
    'get_chart_symbol_name',
    'minMax_Chart',
    'trade_close',
    
    
    # """
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    #                                                 SNACKBAR MESSAGE
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    # """

    # Snackbar
    'get_trade_snackbar_banner',
    'get_neg_snackbar_banner', 
    'get_bulk_snackbar_banner',
    

    # """
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    #                                                 ORDER PLACING / EDIT WINDOW
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    # """

    # orderPlacingWindow
    'toggle_radioButton_OCT',
    'label_onePointEqual',
    'button_buy_sell_type',
    'button_OCT_buy_sell_type',
    'dropdown_orderType',
    'swap_units_volume',
    'swap_units_volume',
    'btn_minMax_size',
    'input_size_volume',
    'close_partialSize',
    'fillPolicy_type',
    'handle_entryPrice',
    'btn_minMax_price',
    'manage_entryPrice',
    'handle_stopLimitPrice',
    'btn_minMax_stopLimitPrice',
    'manage_stopLimitPrice',
    'handle_stopLoss',
    'btn_minMax_stopLoss',
    'manage_stopLoss',
    'handle_takeProfit',
    'btn_minMax_takeProfit',
    'manage_takeProfit',
    'select_specified_date',
    'select_time_option',
    'select_specified_date_and_time',
    'expiry',
    'button_trade_action',
    'trade_ordersConfirmationDetails',
    'compare_dataframes',
    'process_and_print_data',
    


    # """
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    #                                                 ORDER - PRICE RELATED
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    # """

    """Place / Edit Rrder """
    # PriceRelated.py    
    'get_random_point_distance',
    'get_random_point_distance', 
    'pointsDistance', 
    'get_edit_order_label', 
    'get_market_high_low_prices',
    'get_current_price', 
    

    # """
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    #                                                 ORDER - MARKET
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    # """

    # order_market.py
    'calculate_stop_loss',
    'calculate_take_profit',
    'trade_oct_market_order', 
    'trade_market_order',
    'modify_market_order',
    'close_delete_order',
    

    # """
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    #                                                 ORDER - LIMIT
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    # """
    
    # order_limit.py
    'calculate_limit_entryPrice',
    'calculate_limit_stopLoss',
    'calculate_limit_takeProfit',
    'trade_limit_order',
    'modify_limit_order',
    
    
    # """
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    #                                                 ORDER - STOP
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    # """

    # order_stop.py
    'calculate_stop_entryPrice',
    'calculate_stop_stopLoss',
    'calculate_stop_takeProfit',
    'trade_stop_order',
    'modify_stop_order',
    
    
    # """
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    #                                                 ORDER - STOP LIMIT
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    # """

    # order_stoplimit.py
    'calculate_stopLimit_entryPrice',
    'calculate_stopLimit_Price',
    'calculate_stopLimit_stopLoss',
    'calculate_stopLimit_takeProfit', 
    'trade_stopLimit_order',
    'modify_stopLimit_order',
    
    
    # """
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    #                                                 ORDER - NOTIFICATION
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    # """


    # Notification
    'notification_type',
    'get_orderNotification_msg',
    'get_noti_ordersDetails',
    'process_order_notifications',
    
    
    # """
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    #                                                 ORDER PANEL
    # ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    # """
    
    # orderPanel
    'asset_symbolName',
    'type_orderPanel',
    'button_orderPanel_action',
    'get_orderID',
    'extract_order_info',
    'get_order_panel_name',
    'review_pending_orderIDs',
    'check_orderIDs_in_table',
    
    
    # Bulk Close / Delete
    'extract_rgb_from_color',
    'process_profit_loss',
    'button_bulk_operation',
    
    
    # Order History
    'calendar_datePicker',
    'OH_closeDate',
 
 
    # Common Function
    'get_table_body',
    'get_table_headers'
    
]