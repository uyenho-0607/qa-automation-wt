import random
import traceback

from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element_with_wait, find_element_by_testid, get_label_of_element, visibility_of_element_by_testid, spinner_element

from common.desktop.module_trade.order_placing_window.opw_button_action import dropdown_orderType



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

def get_random_point_distance(option, trade_type):
    if option in ["buy", "BUY LIMIT", "SELL STOP", "SELL STOP LIMIT"]:
        if trade_type == "trade":
            min_point_distance = random.randint(500, 700) # Adjust the range as needed
        else: # For edit
            min_point_distance = random.randint(200, 300) # Adjust the range as needed
    
    elif option in ["sell", "SELL LIMIT", "BUY STOP", "BUY STOP LIMIT"]:
        if trade_type == "trade":
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
# To generate a random value point (For Price Formula)
def pointsDistance(trade_type):
    try:
        if trade_type == "trade":
            multiplier = random.randint(400, 600) # Generate a random integer between 400 and 600
        else: # for edit 
            multiplier = random.randint(200, 400) # Generate a random integer between 200 and 400
        
        print(f"{trade_type} multiplier", multiplier)
        return multiplier
    except Exception as e:
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"



# Get the Stop Loss Points
def get_sl_point_distance(option, trade_type):
    if option in ["buy", "BUY", "BUY LIMIT", "BUY STOP", "BUY STOP LIMIT"]:
        if trade_type == "trade":
            stopLoss_point = random.randint(400, 800) # Adjust the range as needed
        else: # For edit
            stopLoss_point = random.randint(200, 300) # Adjust the range as needed
    
    elif option in ["sell", "SELL", "SELL LIMIT", "SELL STOP", "SELL STOP LIMIT"]:
        if trade_type == "trade":
            stopLoss_point = random.randint(800, 1500) # Adjust the range as needed
        else: # For edit
            stopLoss_point = random.randint(500, 800) # Adjust the range as needed
    else:
        raise ValueError("Invalid option provided")

    print(f"{trade_type} stop loss min point", stopLoss_point)

    return stopLoss_point




# Get the Take Profit Points
def get_tp_point_distance(option, trade_type):
    if option in ["buy", "BUY", "BUY LIMIT", "BUY STOP", "BUY STOP LIMIT"]:
        if trade_type == "trade":
            takeProfit_point = random.randint(1000, 2000) # Adjust the range as needed
        else: # For edit
            takeProfit_point = random.randint(400, 900) # Adjust the range as needed
    
    elif option in ["sell", "SELL", "SELL LIMIT", "SELL STOP", "SELL STOP LIMIT"]:
        if trade_type == "trade":
            takeProfit_point = random.randint(600, 1000) # Adjust the range as needed
        else: # For edit
            takeProfit_point = random.randint(200, 600) # Adjust the range as needed
    else:
        raise ValueError("Invalid option provided")

    print(f"{trade_type} take profit min point", takeProfit_point)
    return takeProfit_point


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
    try:
        indicatorType = find_element_by_testid(driver, data_testid="edit-confirmation-order-type")
        indicatorLabel = get_label_of_element(indicatorType)
        return indicatorLabel
    
    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - GET 24HR HIGH / LOW PRICE VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_market_high_low_prices(driver):
    try:
        
        delay(0.5)
        high_price_element = find_element_by_testid(driver, data_testid="symbol-24hr-high")
        high_price_value = get_label_of_element(high_price_element).replace(',', '')
        high_price_value = float(high_price_value)
        print("original 24hr high price", high_price_value)

        low_price_element = find_element_by_testid(driver, data_testid="symbol-24hr-low")
        low_price_value = get_label_of_element(low_price_element).replace(',', '')
        low_price_value = float(low_price_value)
        print("original 24hr low price", low_price_value)

        # Generate a random percentage between 10% and 50%, rounded to 2 decimal places
        random_percentage = round(random.uniform(0.1, 0.5), 3)
        print("%", random_percentage)
        
        # Calculate the adjusted value based on the random percentage
        high_price = float(high_price_value - (high_price_value * random_percentage))
        print("adjusted high price", high_price)
        
        low_price = float(low_price_value - (low_price_value * random_percentage))
        print("adjusted low price", low_price)

        return high_price, low_price
    
    except Exception as e:
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

def get_current_price(driver, trade_type, option=None, partial_text=None):
    try:
        
        spinner_element(driver)
        
        if trade_type == "trade" and option in ["buy", "sell"]:
            # find the buy or sell button
            priceValue = visibility_of_element_by_testid(driver, data_testid=f"{trade_type}-button-order-{option}")
            click_element_with_wait(driver, element=priceValue)
            
            order_type = dropdown_orderType(driver, partial_text)

            if order_type == "market":
                # Retrieve the opposite price for market orders without clicking
                opposite_option = "sell" if option == "buy" else "buy"
                opposite_price_element = find_element_by_testid(driver, data_testid=f"trade-live-{opposite_option}-price")
                opposite_price = get_label_of_element(opposite_price_element).replace(',', '')
                print(f"Market Order - {option.capitalize()} Option: {opposite_option.capitalize()} Price: {opposite_price}")
                return float(opposite_price)
            else:
                # Retrieve the main price for Pending Orders
                price_element = find_element_by_testid(driver, data_testid=f"trade-live-{option}-price")
                price_value = get_label_of_element(price_element).replace(',', '')
                print(f"Pending Order - {option.capitalize()} Price: {price_value}")
                return float(price_value)
    
        else:  # For Edit
            price_element = visibility_of_element_by_testid(driver, data_testid="edit-symbol-price")
            current_price = get_label_of_element(price_element).replace(',', '')
            print("Edit - Current Price: ", current_price)
            return float(current_price)
        
    except Exception as e:
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""