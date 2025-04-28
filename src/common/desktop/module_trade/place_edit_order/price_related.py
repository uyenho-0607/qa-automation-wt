import random

from enums.main import ButtonModuleType, SLTPOption, TradeDirectionOption, OrderExecutionType, AlertType

from constants.element_ids import DataTestID

from constants.helper.error_handler import handle_exception
from constants.helper.element import spinner_element, populate_element, click_element_with_wait, find_element_by_testid, get_label_of_element, find_visible_element_by_testid
from common.desktop.module_trade.order_placing_window.utils import dropdown_order_type, handle_entry_price, handle_stop_limit_price, handle_stop_loss, handle_take_profit



# Define a global variable
stop_limit_price = None

# To store the Stop Limit Price variable
def log_stop_limit_price():
    global stop_limit_price  # Declare the use of the global variable
    return stop_limit_price


# To store the Entry Price variable
def log_entry_price(entry_price):
    return entry_price


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - GENERATE A RANDOM VALUE FOR PENDING ORDER ENTRY PRICE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

"""
                            PENDING ORDER (ENTRY PRICE)
      ORDER TYPE        TYPE                     BUY                 SELL
        LIMIT        ENTRY PRICE          BELOW MARKET PRICE    ABOVE MARKET PRICE
        STOP         ENTRY PRICE          ABOVE MARKET PRICE    BELOW MARKET PRICE
        STOP LIMIT   ENTRY PRICE          ABOVE MARKET PRICE    BELOW MARKET PRICE
        STOP LIMIT   STOP LIMIT PRICE     BELOW MARKET PRICE    ABOVE MARKET PRICE

"""

def get_random_point_distance(option, trade_type: ButtonModuleType):
    """
    Returns a random point distance based on the given option and trade type.

    - option: The type of trade option (e.g., "buy", "sell limit", "sell stop").
    - trade_type: The type of trade (e.g., "trade", "edit").
    :return: A random point distance value within a specified range.
    """
    
    # Determine point distance based on option and trade type
    if option in ["buy", "buy limit", "sell stop", "sell stop limit"]:
        if trade_type == ButtonModuleType.TRADE:
            min_point_distance = random.randint(500, 700) # Adjust the range as needed
        else: # For edit
            min_point_distance = random.randint(200, 300) # Adjust the range as needed
    
    elif option in ["sell", "sell limit", "buy stop", "buy stop limit"]:
        if trade_type == ButtonModuleType.TRADE:
            min_point_distance = random.randint(900, 1000) # Adjust the range as needed
        else: # For edit
            min_point_distance = random.randint(800, 900) # Adjust the range as needed
    else:
        raise ValueError("Invalid option provided")

    print(f"{trade_type} min point distance for entry price", min_point_distance)
    return min_point_distance

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - GENERATE A RANDOM VALUE FOR STOP LOSS / TAKE PROFIT POINTS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def generate_min_point_disatance(trade_type: ButtonModuleType):
    """
    Returns a random multiplier based on the trade type.
    
    Arguments:
    - trade_type: The type of trade (either "trade" or "edit").
    
    Returns: 
    - A random multiplier within the specified range.
    """
    if trade_type == ButtonModuleType.TRADE:
        multiplier = random.randint(200, 400) # Generate a random integer between 100 and 200
    else: # for edit 
        multiplier = random.randint(80, 100) # Generate a random integer between 80 and 100
    
    print(f"{trade_type} min point distance generate: ", multiplier)
    return multiplier



# Get the Stop Loss Points
def get_sl_point_distance(option, trade_type: ButtonModuleType):
    """
    Returns a stop-loss point distance based on the trade type and option provided.

    Arguments:
    - option: The trade option (buy/sell).
    - trade_type: The type of trade (either "trade" or "edit").
    
    Returns:
    - A random stop-loss point distance based on the conditions.
    """

    # Check if the option is valid
    if option in ["buy", "buy limit", "buy stop", "buy stop limit"]:
        if trade_type == ButtonModuleType.TRADE:
            stop_loss_point = random.randint(200, 400) # Adjust the range as needed
        else: # For edit
            stop_loss_point = random.randint(100, 200) # Adjust the range as needed
    
    elif option in ["sell", "sell limit", "sell stop", "sell stop limit"]:
        if trade_type == ButtonModuleType.TRADE:
            stop_loss_point = random.randint(800, 1500) # Adjust the range as needed
        else: # For edit
            stop_loss_point = random.randint(500, 800) # Adjust the range as needed
    else:
        raise ValueError(f"Invalid option '{option}' provided. Expected 'buy' or 'sell' related options.")

    print(f"{trade_type} stop loss min point", stop_loss_point)

    return stop_loss_point




# Get the Take Profit Points
def get_tp_point_distance(option, trade_type: ButtonModuleType):
    """
    Returns a take-profit point distance based on the trade type and option provided.

    Arguments:
    - option: The trade option (buy/sell).
    - trade_type: The type of trade (either "trade" or "edit").
    
    Returns:
    - A random take-profit point distance based on the conditions.
    """
    # Check if the option is valid and determine take-profit point distance
    if option in ["buy", "buy limit", "buy stop", "buy stop limit"]:
        if trade_type == ButtonModuleType.TRADE:
            take_profit_point = random.randint(1000, 2000) # Adjust the range as needed
        else: # For edit
            take_profit_point = random.randint(400, 900) # Adjust the range as needed
    
    elif option in ["sell", "sell limit", "sell stop", "sell stop limit"]:
        if trade_type == ButtonModuleType.TRADE:
            take_profit_point = random.randint(400, 500) # Adjust the range as needed
        else: # For edit
            take_profit_point = random.randint(200, 400) # Adjust the range as needed
    else:
        raise ValueError(f"Invalid option '{option}' provided. Expected 'buy' or 'sell' related options.")

    print(f"{trade_type} take profit min point", take_profit_point)
    return take_profit_point


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - GET EDIT ORDER CURRENT PRICE LABEL
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_edit_order_label(driver):
    """
    Retrieves the label for the edit order confirmation type.

    Returns:
    - The label text for the edit order type, if found.
    """
    try:
        # Find the element that contains the order type
        indicatorType = find_element_by_testid(driver, data_testid=DataTestID.EDIT_CONFIRMATION_ORDER_TYPE)
        
        # Retrieve the label associated with the order type
        indicatorLabel = get_label_of_element(indicatorType).lower()
        
        return indicatorLabel
    
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - GET CURRENT BUY / SELL PRICE VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_current_price(driver, trade_type, option: TradeDirectionOption = None, order_type: OrderExecutionType = None):
    """
    Retrieves the current price for a given trade type and option (buy/sell).

    Arguments:
    - trade_type: Type of trade ('trade' or 'edit')
    - option: 'buy' or 'sell' for the trade order
    - partial_text: Optional, used for finding the order type in dropdowns
    
    Returns:
    - Current price for the order type
    """
    try:
    
        spinner_element(driver)
        
        direction = {
            TradeDirectionOption.BUY: DataTestID.TRADE_BUTTON_ORDER_BUY,
            TradeDirectionOption.SELL: DataTestID.TRADE_BUTTON_ORDER_SELL
        }
        live_price_value = {
            TradeDirectionOption.BUY: DataTestID.TRADE_LIVE_BUY_PRICE,
            TradeDirectionOption.SELL: DataTestID.TRADE_LIVE_SELL_PRICE
        }
        
        if trade_type == ButtonModuleType.TRADE and option in direction:
            # find the buy or sell button
            btn_buy_sell = find_visible_element_by_testid(driver, data_testid=direction[option])
            click_element_with_wait(driver, element=btn_buy_sell)
            
            order_type = dropdown_order_type(driver, order_type)

            if order_type == OrderExecutionType.MARKET:
                # Retrieve the opposite price for market orders without clicking
                opposite_option = TradeDirectionOption.SELL if option == TradeDirectionOption.BUY else TradeDirectionOption.BUY
                opposite_price_element = find_element_by_testid(driver, data_testid=live_price_value[opposite_option])
                price_value = get_label_of_element(opposite_price_element).replace(',', '')
                print(f"Market Order - {option.name} Option: {opposite_option.name} Price: {price_value}")
                
            else:
                # Retrieve the main price for Pending Orders
                price_element = find_element_by_testid(driver, data_testid=live_price_value[option])
                price_value = get_label_of_element(price_element).replace(',', '')
                print(f"Pending Order - {option.name} Price: {price_value}")
            
            return float(price_value)

        else:  # For Edit
            find_visible_element_by_testid(driver, data_testid=DataTestID.EDIT_CONFIRMATION_MODAL)
            price_element = find_element_by_testid(driver, data_testid=DataTestID.EDIT_SYMBOL_PRICE)
            current_price = float(get_label_of_element(price_element).replace(',', ''))
            print("Edit - Current Price:", current_price)
            return float(current_price)
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE ENTRY PRICE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def calculate_pending_entry_price(driver, trade_type: ButtonModuleType, option: TradeDirectionOption, order_type: OrderExecutionType, label_one_points_equal, current_price, entry_price_flag: AlertType = AlertType.POSITIVE):
    global entry_price  # Declare the use of the global variable

    entry_price_input = handle_entry_price(driver, trade_type)

    min_point_distance = get_random_point_distance(option, trade_type)
    
    price_adjustment = label_one_points_equal * min_point_distance
    # BUY: Buy price - (One point equals * Minimum Point Distance)
    # SELL: Sell price + (One point equals * Minimum Point Distance)
    
    # Define price direction maps
    positive_direction_map = {
        OrderExecutionType.LIMIT: {
            TradeDirectionOption.BUY: current_price - price_adjustment,
            TradeDirectionOption.BUY_LIMIT: current_price - price_adjustment,
            TradeDirectionOption.SELL: current_price + price_adjustment,
            TradeDirectionOption.SELL_LIMIT: current_price + price_adjustment
        },
        OrderExecutionType.STOP: {
            TradeDirectionOption.BUY: current_price + price_adjustment,
            TradeDirectionOption.BUY_STOP: current_price + price_adjustment,
            TradeDirectionOption.SELL: current_price - price_adjustment,
            TradeDirectionOption.SELL_STOP: current_price - price_adjustment
        },
        OrderExecutionType.STOP_LIMIT: {
            TradeDirectionOption.BUY: current_price + price_adjustment,
            TradeDirectionOption.BUY_STOP_LIMIT: current_price + price_adjustment,
            TradeDirectionOption.SELL: current_price - price_adjustment,
            TradeDirectionOption.SELL_STOP_LIMIT: current_price - price_adjustment
        }
    }

    negative_direction_map = {
        OrderExecutionType.LIMIT: {
            TradeDirectionOption.BUY: current_price + price_adjustment,
            TradeDirectionOption.BUY_LIMIT: current_price + price_adjustment,
            TradeDirectionOption.SELL: current_price - price_adjustment,
            TradeDirectionOption.SELL_LIMIT: current_price - price_adjustment
        },
        OrderExecutionType.STOP: {
            TradeDirectionOption.BUY: current_price - price_adjustment,
            TradeDirectionOption.BUY_STOP: current_price - price_adjustment,
            TradeDirectionOption.SELL: current_price + price_adjustment,
            TradeDirectionOption.SELL_STOP: current_price + price_adjustment
        },
        OrderExecutionType.STOP_LIMIT: {
            TradeDirectionOption.BUY: current_price - price_adjustment,
            TradeDirectionOption.BUY_STOP_LIMIT: current_price - price_adjustment,
            TradeDirectionOption.SELL: current_price + price_adjustment,
            TradeDirectionOption.SELL_STOP_LIMIT: current_price + price_adjustment
        }
    }

    if entry_price_flag == AlertType.POSITIVE:
        entry_price = positive_direction_map[order_type][option]
    else:
        entry_price = negative_direction_map[order_type][option]

    populate_element(element=entry_price_input, text=entry_price)
    log_entry_price(entry_price)

    return entry_price

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE STOP LIMIT PRICE VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def calculate_stop_limit_price(driver, trade_type: ButtonModuleType, option: TradeDirectionOption, label_one_points_equal, stop_limit_price_flag: AlertType = AlertType.POSITIVE):
    global stop_limit_price  # Declare the use of the global variable

    stop_limit_price_input = handle_stop_limit_price(driver, trade_type)

    min_point_distance = get_random_point_distance(option, trade_type)

    # Determine the base price based on stop limit or entry price
    price_value = log_entry_price(entry_price)

    price_adjustment = label_one_points_equal * min_point_distance
    # BUY = Stop Limit Price - (One point equals * Minimum Point Distance)
    # SELL = Stop Limit Price + (One point equals * Minimum Point Distance)
    

    # Define price direction maps
    positive_direction_map = {
        TradeDirectionOption.BUY: price_value - price_adjustment,
        TradeDirectionOption.BUY_STOP_LIMIT: price_value - price_adjustment,
        TradeDirectionOption.SELL: price_value + price_adjustment,
        TradeDirectionOption.SELL_STOP_LIMIT: price_value + price_adjustment
    }

    negative_direction_map = {
        TradeDirectionOption.BUY: price_value + price_adjustment,
        TradeDirectionOption.BUY_STOP_LIMIT: price_value + price_adjustment,
        TradeDirectionOption.SELL: price_value - price_adjustment,
        TradeDirectionOption.SELL_STOP_LIMIT: price_value - price_adjustment
    }

    if stop_limit_price_flag == AlertType.POSITIVE:
        stop_limit_price = positive_direction_map.get(option, price_value)
    else:
        stop_limit_price = negative_direction_map.get(option, price_value)

    populate_element(element=stop_limit_price_input, text=stop_limit_price)

    return stop_limit_price


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - CALCULATE STOP LOSS VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def calculate_pending_stop_loss(driver, trade_type, sl_type, option, label_one_points_equal, stop_loss_flag: AlertType = AlertType.POSITIVE, is_stop_limit: bool = False):  # Flag to differentiate between Stop Limit and Limit
    # Common logic
    min_point_distance = generate_min_point_disatance(trade_type)
    stop_loss_point = get_sl_point_distance(option, trade_type)
    stop_loss_input = handle_stop_loss(driver, trade_type, sl_type)

    # Determine the base price based on stop limit or entry price
    price_value = log_stop_limit_price() if is_stop_limit else log_entry_price(entry_price)

    # Define the calculation logic for BUY and SELL options
    price_adjustment = label_one_points_equal * min_point_distance
    # BUY = Price(S) - (One point equals * Minimum Point Distance)
    # SELL = Price(S) + (One point equals * Minimum Point Distance)

    direction_map = {
        TradeDirectionOption.BUY: price_value - price_adjustment,
        TradeDirectionOption.BUY_LIMIT: price_value - price_adjustment,
        TradeDirectionOption.BUY_STOP: price_value - price_adjustment,
        TradeDirectionOption.BUY_STOP_LIMIT: price_value - price_adjustment,
        
        TradeDirectionOption.SELL: price_value + price_adjustment,
        TradeDirectionOption.SELL_LIMIT: price_value + price_adjustment,
        TradeDirectionOption.SELL_STOP: price_value + price_adjustment,
        TradeDirectionOption.SELL_STOP_LIMIT: price_value + price_adjustment
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
            TradeDirectionOption.BUY: price_value + price_adjustment,
            TradeDirectionOption.BUY_LIMIT: price_value + price_adjustment,
            TradeDirectionOption.BUY_STOP: price_value + price_adjustment,
            TradeDirectionOption.BUY_STOP_LIMIT: price_value + price_adjustment,
            
            TradeDirectionOption.SELL: price_value - price_adjustment,
            TradeDirectionOption.SELL_LIMIT: price_value - price_adjustment,
            TradeDirectionOption.SELL_STOP: price_value - price_adjustment,
            TradeDirectionOption.SELL_STOP_LIMIT: price_value - price_adjustment
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
                                                TRADE / EDIT - CALCULATE STOP LIMIT TAKE PROFIT VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def calculate_pending_take_profit(driver, trade_type, tp_type, option, label_one_points_equal, take_profit_flag: AlertType = AlertType.POSITIVE, is_stop_limit: bool = False):  # Flag to differentiate between Stop Limit and Limit
    # Common logic
    min_point_distance = generate_min_point_disatance(trade_type)
    take_profit_point = get_sl_point_distance(option, trade_type)
    take_profit_input = handle_take_profit(driver, trade_type, tp_type)

    # Determine the base price based on stop limit or entry price
    price_value = log_stop_limit_price() if is_stop_limit else log_entry_price(entry_price)

    # Define the calculation logic for BUY and SELL options
    price_adjustment = label_one_points_equal * min_point_distance
    # BUY = Price(S) + (One point equals * Minimum Point Distance)
    # SELL = Price(S) - (One point equals * Minimum Point Distance)
    
    direction_map = {
        TradeDirectionOption.BUY: price_value + price_adjustment,
        TradeDirectionOption.BUY_LIMIT: price_value + price_adjustment,
        TradeDirectionOption.BUY_STOP: price_value + price_adjustment,
        TradeDirectionOption.BUY_STOP_LIMIT: price_value + price_adjustment,
        
        TradeDirectionOption.SELL: price_value - price_adjustment,
        TradeDirectionOption.SELL_LIMIT: price_value - price_adjustment,
        TradeDirectionOption.SELL_STOP: price_value - price_adjustment,
        TradeDirectionOption.SELL_STOP_LIMIT: price_value - price_adjustment
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
            TradeDirectionOption.BUY: price_value - price_adjustment,
            TradeDirectionOption.BUY_LIMIT: price_value - price_adjustment,
            TradeDirectionOption.BUY_STOP: price_value - price_adjustment,
            TradeDirectionOption.BUY_STOP_LIMIT: price_value - price_adjustment,
            
            TradeDirectionOption.SELL: price_value + price_adjustment,
            TradeDirectionOption.SELL_LIMIT: price_value + price_adjustment,
            TradeDirectionOption.SELL_STOP: price_value + price_adjustment,
            TradeDirectionOption.SELL_STOP_LIMIT: price_value + price_adjustment
        }
        
        take_profit_value = reverse_direction_map.get(option, take_profit_point)  # Default to stop_loss_point if not found

    # Populate the element with the calculated stop loss value
    populate_element(element=take_profit_input, text=take_profit_value)

    return take_profit_value

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""