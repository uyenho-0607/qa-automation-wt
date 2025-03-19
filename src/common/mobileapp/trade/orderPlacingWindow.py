import re
import random
import traceback
import pandas as pd

from tabulate import tabulate
from datetime import datetime

from selenium.webdriver.common.by import By

from constants.helper.driver import delay
from constants.helper.element_android_app import click_element, click_element_with_wait, clear_input_field, find_element_by_testid, find_list_of_elements_by_xpath, find_list_of_elements_by_testid, find_element_by_xpath, find_element_by_xpath_with_wait, spinner_element, find_visible_element_by_testid, get_label_of_element, populate_element_with_wait, javascript_click
from constants.helper.screenshot import take_screenshot, attach_text



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - TOGGLE ON / OFF OCT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
        
def toggle_radioButton_OCT(driver, desired_state="unchecked"):
    try:
        # Define both possible 'data-testid' values for the radio button states
        radio_states = {
            "unchecked": "toggle-oct",
            "checked": "toggle-oct-checked"
        }

        # Identify the current state of the radio button (checked/unchecked)
        current_state = None
        for state, testid in radio_states.items():
            try:
                
                oct_button = find_element_by_testid(driver, testid)
                current_state = state
                print(f"Radio button is currently in the '{state}' state.")

                # If the current state matches the desired state, no action is needed
                if state == desired_state:
                    print(f"Desired state is '{desired_state}', no action needed.")
                    return

                # Perform the toggle to the desired state
                print(f"Toggling to '{desired_state}' as desired.")
                click_element(oct_button)

                # Confirm the action if needed
                if desired_state == "checked":
                    oct_confirm = find_visible_element_by_testid(driver, data_testid="oct-modal-button-confirm")
                    click_element(oct_confirm)
                return
            
            except Exception:
                # If the element is not found, continue checking the other state
                continue

        # If no valid state is found
        if current_state is None:
            raise Exception("Unable to determine the current state of the radio button.")

    except Exception as e:
        # Capture screenshot and log the error in case of failure
        take_screenshot(driver, "toggle_radioButton_OCT_01 - Exception Screenshot")
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE MODULE - ONE POINTS EQUALS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def label_onePointEqual(driver, trade_type):
    try:
        
        # Locate the One Ppoint Equal label element
        onePointsEqual = find_visible_element_by_testid(driver, data_testid=f"{trade_type}-one-point-equal-label")
        label_onePointsEqual = get_label_of_element(onePointsEqual)

        # Regular expression to find the number after "equals:"
        onePointsEqual_value = re.search(r"[\d.]+", label_onePointsEqual).group()
        
        return float(onePointsEqual_value)

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "onePointEqual_label - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - BUY / SELL BUTTON INDICATOR
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_tradeModule(driver):
    try:
        spinner_element(driver)
        
        button_trade = find_visible_element_by_testid(driver, data_testid="trade-button-order")
        # click_element(button_trade)
        click_element_with_wait(driver, element=button_trade)

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "oct_trade_button - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - BUY / SELL BUTTON INDICATOR
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_buy_sell_type(driver, indicator_type):
    try:
        spinner_element(driver)
        
        order_execution = find_element_by_testid(driver, data_testid=f"trade-button-order-{indicator_type}")
        # click_element_with_wait(driver, element=order_execution)
        click_element(order_execution)
        
    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "button_buy_sell_type - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE OCT - BUY / SELL BUTTON INDICATOR
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_OCT_buy_sell_type(driver, option):
    try:
        
        order_execution = find_element_by_testid(driver, data_testid=f"trade-button-oct-order-{option}")
        click_element_with_wait(driver, element=order_execution)

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "button_OCT_buy_sell_type - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - ORDER TYPE DROPDOWN SELECTION (MARKET / LIMIT / STOP / STOP LIMIT)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def dropdown_orderType(driver, partial_text=None):
    try:
        
        type_dropdown = find_visible_element_by_testid(driver, data_testid="trade-dropdown-order-type")
        click_element(type_dropdown)

        orderType_options = find_visible_element_by_testid(driver, data_testid=f"trade-dropdown-order-type-{partial_text}")
        click_element(orderType_options)
        
        return partial_text
        
    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "dropdown_orderType - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - SWAP BETWEEN SIZE (VOLUME) / UNITS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def swap_units_volume(driver, desired_state):
    try:
        # Define both possible 'data-testid' values for the radio button states
        swap_options = {
            "units": "trade-swap-to-units",
            "volume": "trade-swap-to-volume"
        }

        # Identify the current state of the radio button (checked/unchecked)
        current_state = None
        for state, testid in swap_options.items():
            try:

                find_visible_element_by_testid(driver, testid)
                current_state = state
                print(f"Current button state: Swap to {state.capitalize()}")

                # If the current state matches the desired state, no action is needed
                if state == desired_state:
                    print(f"Desired state is '{desired_state}', no action needed.")
                    return desired_state  # Return after swapping
                else:
                    print(f"Swapping to '{desired_state.capitalize()}' as desired.")
                    swap_button = find_element_by_testid(driver, testid) # Perform the swap
                    click_element(swap_button)
                    return desired_state  # Return after swapping

            except Exception:
                # If the element is not found, continue checking the other state
                continue

        # If no valid state is found
        if current_state is None:
            return desired_state == False
            # raise Exception("Unable to determine current swap state.")
            
    except Exception as e:
        # Capture screenshot and log the error in case of failure
        take_screenshot(driver, "swap_units_volume - Exception Screenshot")
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - BUTTON MIN / MAX SIZE (VOLUME) (+ / - BUTTON)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def btn_minMax_size(driver, minMax, number_of_clicks):
    try:
        
        delay(0.2)
        
        # Find the button for increasing or decreasing the trade input volume
        button_minMax = find_element_by_testid(driver, data_testid=f"trade-input-volume-{minMax}")
        
        # Find the input field for the trade volume
        input_field = find_element_by_testid(driver, data_testid=f"trade-input-volume")

        # Get the initial value of the input field and set it to 0.0 if empty
        initial_value_str = input_field.get_attribute("value")
        initial_value = float(initial_value_str) if initial_value_str.strip() else 0.0

        # Get the placeholder attribute, which holds the increment value (e.g., "0.01")
        placeholder_value = input_field.get_attribute('placeholder')

        # Extract the increment value from the placeholder using regular expression
        increment = float(re.search(r'([\d\.]+)', placeholder_value).group(1))

        # Loop through the number of clicks specified
        for i in range(number_of_clicks):
            # Click the button (either increase or decrease)
            click_element(button_minMax)
            
            # Get the updated value after the click and set it to 0.0 if the field is empty
            updated_value_str = input_field.get_attribute("value")
            updated_value = float(updated_value_str) if updated_value_str.strip() else 0.0
            
            # Check if the value has incremented or decremented by the correct amount
            if minMax == "increase":
                difference = updated_value - initial_value
                assert abs(difference - increment) < 1e-6, f"Value did not increment by {increment} after click {i+1}. Difference: {difference:.6f}"
            elif minMax == "decrease":
                difference = initial_value - updated_value
                assert abs(difference - increment) < 1e-6, f"Value did not decrement by {increment} after click {i+1}. Difference: {difference:.6f}"
            else:
                raise ValueError("Invalid value for minMax. Must be 'increase' or 'decrease'.")

            # Update the initial value to the current value for the next iteration
            initial_value = updated_value

            # Final check: ensure total increment or decrement matches the expected value
            final_value = float(input_field.get_attribute("value"))
            expected_value = initial_value + (increment * number_of_clicks) if minMax == "increase" else initial_value - (increment * number_of_clicks)
            
            # Assert that the final value is correct
            assert abs(final_value - expected_value), f"Final value does not match expected value. Expected: {expected_value:.2f}, Got: {final_value:.2f}"

            # Log the number of clicks and the final value
            attach_text(str(number_of_clicks), f"{minMax.capitalize()} button clicked {i+1} times")
            attach_text(f"{final_value:.2f}", f"Final value: {final_value:.2f}")
            
    except Exception as e:
        take_screenshot(driver, "btn_minMax_size - Exception Screenshot")
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - SIZE / VOLUME FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def input_oct_size_volume(driver):
    try:

        # Find the input field for trade volume using its data-testid
        size_input = find_visible_element_by_testid(driver, data_testid="trade-input-volume")

        # Randomly decide whether to generate an integer or a decimal
        if random.choice([True, False]):  # Randomly choose between True (integer) or False (decimal)
            # Generate a random integer between 1 and 100
            random_value = random.randint(1, 100)
        else:
            # Generate a random decimal between 1 and 100 with two decimal places
            random_value = round(random.uniform(1, 100), 2)
        
        # Convert the random value to a string
        random_value_str = str(random_value)
        
        # Populate the input field with the random value
        populate_element_with_wait(driver, element=size_input, text=random_value_str)
        
    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "input_size_volume - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"
        


def input_size_volume(driver, desired_state="units"):
    try:
        
        # Swap the state to either 'units' or 'volume' depending on the desired state
        state = swap_units_volume(driver, desired_state)
    
        # Find the input field for trade volume using its data-testid
        size_input = find_element_by_testid(driver, data_testid="trade-input-volume")
        
        if state == "units":
            # Randomly decide whether to generate an integer or a decimal
            if random.choice([True, False]):  # Randomly choose between True (integer) or False (decimal)
                # Generate a random integer between 1 and 100
                random_value = random.randint(1, 100)
            else:
                # Generate a random decimal between 1 and 100 with two decimal places
                random_value = round(random.uniform(1, 100), 2)
        else:
            # Generate a random integer between 1000 and 10000 if the desired state is 'units'
            random_value = random.randint(1000, 10000)
        
        # Convert the random value to a string
        random_value_str = str(random_value)
        
        # Populate the input field with the random value
        populate_element_with_wait(driver, element=size_input, text=random_value_str)
        
    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "input_size_volume - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CLOSE - PARTIAL SIZE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def close_partialSize(driver, close_button, fillPolicy_type = None ,fillPolicy: bool = False, clearField: bool = False):
    try:
        
        # Find the element containing the maximum value label
        max_value_element = find_element_by_testid(driver, data_testid="close-order-input-volume-max-value")

        # Extract the maximum value text from the element
        max_value_text = max_value_element.text.split()[1]  # Assuming it's in text format
        
        # Convert the maximum value to a float (handle both integer and decimal values)
        max_value = float(max_value_text)
                
        # Determine the appropriate minimum value step based on the magnitude of max_value
        if max_value < 0.1:
            min_value_step = 0.01  # Small step for values less than 0.1
        elif max_value < 1.0:
            min_value_step = 0.1   # Larger step for values less than 1.0
        else:
            min_value_step = 0.01  # Default to 0.01 step for larger values

        # Randomly decide whether to generate an integer or a decimal
        if random.choice([True, False]) and max_value >= 1.0:  # Only generate integers if max_value >= 1.0
            # Generate a random integer between 0 and the retrieved maximum value
            random_value = random.randint(0, int(max_value))
        else:
            # Generate a random decimal between 0 and the retrieved maximum value with the appropriate step
            random_value = round(random.uniform(min_value_step, max_value), 2)

        # Find the input field for partial close size
        partialClose_input = find_element_by_testid(driver, data_testid="close-order-input-volume")

        if clearField:
            # Select all text and delete the selected text
            clear_input_field(partialClose_input)
            populate_element_with_wait(driver, element=partialClose_input, text=str(random_value))

        if fillPolicy:
            # If fill policy is provided, interact with the dropdown to select the appropriate option
            dropdown_fillPolicy = find_element_by_testid(driver, data_testid="close-order-dropdown-fill-policy")
            click_element_with_wait(driver, element=dropdown_fillPolicy)
            
            # Select the specific fill policy option from the dropdown
            fillPolicy_options = find_element_by_testid(driver, data_testid=f"close-order-dropdown-fill-policy-{fillPolicy_type}")
            click_element_with_wait(driver, element=fillPolicy_options)

        # Find the button to confirm the close action and click it
        action_button = find_element_by_testid(driver, data_testid=close_button)
        click_element_with_wait(driver, element=action_button)

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "close_partialSize - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / CLOSE - FILL POLICY DROPDOWN TYPE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def fillPolicy_type(driver, trade_type, fill_policy):
    try:
        
        # Click on the fill policy dropdown for the given trade type
        fillPolicy_type = find_element_by_testid(driver, data_testid=f"{trade_type}-dropdown-fill-policy")
        click_element_with_wait(driver, element=fillPolicy_type)
        
        # Select the specific fill policy option from the dropdown
        fillPolicy_options = find_element_by_testid(driver, data_testid=f"{trade_type}-dropdown-fill-policy-{fill_policy}")
        click_element_with_wait(driver, element=fillPolicy_options)
        
    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "fillPolicy_type - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - LOCATE THE ENTRY PRICE FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_entryPrice(driver, trade_type):
    # Find the entry price input field based on the trade type (e.g., 'edit', 'new')
    entryPrice_element = find_element_by_testid(driver, data_testid=f"{trade_type}-input-price")
    
    # If the trade type is 'edit', clear the input field before proceeding
    if trade_type == "edit":
        clear_input_field(entryPrice_element)
        
    # Return the entry price element for further use
    return entryPrice_element
    
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - BUTTON MIN / MAX ENTRY PRICE (+ / - BUTTON)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def btn_minMax_price(driver, trade_type, minMax, number_of_clicks):
    try:
        
        # Locate the min/max button based on trade type and minMax action (increase or decrease)
        button_minMax = find_element_by_testid(driver, data_testid=f"{trade_type}-input-price-{minMax}")
        javascript_click(driver, button_minMax)

        # Locate the input field where the price is displayed
        input_field = find_element_by_testid(driver, data_testid=f"{trade_type}-input-price")

        # Get the initial value of the input field, set to 0.0 if empty
        initial_value_str = input_field.get_attribute("value")
        initial_value = float(initial_value_str) if initial_value_str.strip() else 0.0

        # Get the increment value (e.g., 0.01) using label_onePointEqual
        increment = label_onePointEqual(driver, trade_type)

        for i in range(number_of_clicks):
            # Click the min/max button
            click_element(button_minMax)
            
            # Get the updated value after the click and set it to 0.0 if empty
            updated_value_str = input_field.get_attribute("value")
            updated_value = float(updated_value_str) if updated_value_str.strip() else 0.0
            
            # Calculate the difference to ensure the value is incrementing/decrementing correctly
            if minMax == "increase":
                difference = updated_value - initial_value
                assert abs(difference - increment) < 1e-6, f"Value did not increment by {increment} after click {i+1}. Difference: {difference:.6f}"
            elif minMax == "decrease":
                difference = initial_value - updated_value
                assert abs(difference - increment) < 1e-6, f"Value did not decrement by {increment} after click {i+1}. Difference: {difference:.6f}"
            else:
                raise ValueError("Invalid value for minMax. Must be 'increase' or 'decrease'.")

            # Update initial_value to be the updated_value for the next iteration
            initial_value = updated_value

            # Final check: ensure total increment or decrement matches the expected value
            final_value = float(input_field.get_attribute("value"))
            expected_value = initial_value + (increment * number_of_clicks) if minMax == "increase" else initial_value - (increment * number_of_clicks)
            
            # Assert that the final value is correct
            assert abs(final_value - expected_value), f"Final value does not match expected value. Expected: {expected_value:.2f}, Got: {final_value:.2f}"

            # Attach text logs for the clicks and final value for reporting
            attach_text(str(number_of_clicks), f"{minMax.capitalize()} button clicked {i+1} times")
            attach_text(f"{final_value}", f"Final value: {final_value}")
            
    except Exception as e:
        take_screenshot(driver, "btn_minMax_size - Exception Screenshot")
        assert False, f"{str(e)}\n{traceback.format_exc()}"

        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - INPUT / CLEAR THE ENTRY PRICE FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def manage_entryPrice(driver, trade_type, price_field=None):
    # Remove the trailing ".0" if it exists
    if price_field.endswith(".0"):
        price_field = price_field[:-2]

    try:
        
        price_input = handle_entryPrice(driver, trade_type)

        if trade_type == 'edit':
            clear_input_field(price_input)
          
        populate_element_with_wait(driver, element=price_input, text=price_field)

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "manageEntryPrice - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - STOP LIMIT PRICE FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_stopLimitPrice(driver, trade_type):
    stopLimitPrice_element = find_element_by_testid(driver, data_testid=f"{trade_type}-input-stop-limit-price")
    if trade_type == "edit":
        clear_input_field(stopLimitPrice_element)

    return stopLimitPrice_element

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - BUTTON MIN / MAX STOP LIMIT PRICE (+ / - BUTTON)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def btn_minMax_stopLimitPrice(driver, trade_type, minMax, number_of_clicks):
    try:

        # Locate the min/max button
        button_minMax = find_element_by_testid(driver, data_testid=f"{trade_type}-input-stop-limit-price-{minMax}")
        click_element(button_minMax)

        # Locate the input field where the price is displayed
        input_field = find_element_by_testid(driver, data_testid=f"{trade_type}-input-stop-limit-price")

        # Get the initial value of the input field, set to 0.0 if empty
        initial_value_str = input_field.get_attribute("value")
        initial_value = float(initial_value_str) if initial_value_str.strip() else 0.0
        print("intial", initial_value)

        # Get the increment (one point equal to a specific value, like 0.01)
        increment = label_onePointEqual(driver, trade_type)
        print("One point equals:", increment)

        for i in range(number_of_clicks):
            click_element(button_minMax)
            
            # Get the updated value after the click and set it to 0.0 if empty
            updated_value_str = input_field.get_attribute("value")
            updated_value = float(updated_value_str) if updated_value_str.strip() else 0.0
            
            # Check if each increment is exactly 0.01 (without rounding)
            if minMax == "increase":
                difference = updated_value - initial_value
                assert abs(difference - increment) < 1e-6, f"Value did not increment by {increment} after click {i+1}. Difference: {difference:.6f}"
            elif minMax == "decrease":
                difference = initial_value - updated_value
                assert abs(difference - increment) < 1e-6, f"Value did not decrement by {increment} after click {i+1}. Difference: {difference:.6f}"
            else:
                raise ValueError("Invalid value for minMax. Must be 'increase' or 'decrease'.")

            # Update initial_value to be the updated_value for the next iteration
            initial_value = updated_value

            # Final check: ensure total increment or decrement matches the expected value
            final_value = float(input_field.get_attribute("value"))
            expected_value = initial_value + (increment * number_of_clicks) if minMax == "increase" else initial_value - (increment * number_of_clicks)
            
            # Assert that the final value is correct
            assert abs(final_value - expected_value), f"Final value does not match expected value. Expected: {expected_value:.2f}, Got: {final_value:.2f}"

            # Attach text logs for the clicks and final value for reporting
            attach_text(str(number_of_clicks), f"{minMax.capitalize()} button clicked {i+1} times")
            attach_text(f"{final_value:.2f}", f"Final value: {final_value:.2f}")
            
    except Exception as e:
        take_screenshot(driver, "btn_minMax_size - Exception Screenshot")
        assert False, f"{str(e)}\n{traceback.format_exc()}"


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - INPUT / CLEAR THE STOP LIMIT PRICE FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def manage_stopLimitPrice(driver, trade_type, price_field=None):

    # Remove the trailing ".0" from the price if it exists
    if price_field.endswith(".0"):
        price_field = price_field[:-2]

    try:
        # Locate the stop-limit price input field based on trade_type
        price_input = find_element_by_testid(driver, data_testid=f"{trade_type}-input-stop-limit-price")
        
        # If the trade is being edited, clear the input field before populating it
        if trade_type == 'edit':
            clear_input_field(price_input)
            
        # Populate the price field with the given price value
        populate_element_with_wait(driver, element=price_input, text=price_field)

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "octStopLimitPrice - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - STOP LOSS FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_stopLoss(driver, trade_type, sl_type):
    # Locate the stop-loss input element based on trade_type and stop-loss type
    stop_loss_element = find_element_by_testid(driver, data_testid=f"{trade_type}-input-stoploss-{sl_type}")
    
    # If the trade is being edited, clear the stop-loss input field
    if trade_type == "edit":
        clear_input_field(stop_loss_element)

    # Return the stop-loss element for further actions if required
    return stop_loss_element

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - BUTTON MIN / MAX STOP LOSS (+ / - BUTTON)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def btn_minMax_stopLoss(driver, trade_type, type, minMax, number_of_clicks):
    try:
        
        # Locate the min/max button based on trade type, stop-loss type, and action (increase/decrease)
        button_minMax = find_element_by_testid(driver, data_testid=f"{trade_type}-input-stoploss-{type}-{minMax}")
        click_element(button_minMax)

        # Locate the input field for the stop-loss value
        input_field = find_element_by_testid(driver, data_testid=f"{trade_type}-input-stoploss-{type}")

        # Determine the initial value based on value_type (either float or int)
        initial_value_str = input_field.get_attribute("value")
        
        if type == "price":
            # Convert input value to float, default to 0.0 if empty
            initial_value = float(initial_value_str) if initial_value_str.strip() else 0.0
            
            # Retrieve the increment value for price
            increment = label_onePointEqual(driver, trade_type)
        elif type == "points":
            # Convert input value to int, default to 0 if empty
            initial_value = int(initial_value_str) if initial_value_str.strip() else 0
            # Set increment for points to 1
            increment = 1
        else:
            raise ValueError("Invalid value type. Must be 'price' or 'points'.")

        # Loop through the specified number of clicks
        for i in range(number_of_clicks):
            click_element(button_minMax)

            # Get the updated value based on value_type
            updated_value_str = input_field.get_attribute("value")
            updated_value = float(updated_value_str) if type == "price" else int(updated_value_str)

            # Check if increment/decrement is as expected
            if minMax == "increase":
                difference = updated_value - initial_value
            elif minMax == "decrease":
                difference = initial_value - updated_value
            else:
                raise ValueError("Invalid value for minMax. Must be 'increase' or 'decrease'.")

            # Assert that the difference is correct based on the type
            if type == "price":
                assert abs(difference - increment) < 1e-6, f"Value did not change by {increment} after click {i+1}. Difference: {difference:.6f}"
            else:  # for "points"
                assert abs(difference - increment) == 0, f"Value did not change by {increment} after click {i+1}. Difference: {difference}"

            # Update initial_value for next iteration
            initial_value = updated_value

            # Attach text logs for the clicks and final value for reporting
            attach_text(str(number_of_clicks), f"{minMax.capitalize()} button clicked {i+1} times")
            attach_text(f"{updated_value:.6f}" if type == "price" else str(updated_value), f"Final value: {updated_value:.6f}" if type == "price" else f"Final value: {updated_value}")

        # Final check: ensure total increment or decrement matches the expected value
        final_value = float(input_field.get_attribute("value")) if type == "price" else int(input_field.get_attribute("value"))
        expected_value = initial_value + (increment * number_of_clicks) if minMax == "increase" else initial_value - (increment * number_of_clicks)
        
        # Assert that the final value is correct
        assert abs(final_value - expected_value), f"Final value does not match expected value. Expected: {expected_value}, Got: {final_value}"

    except Exception as e:
        take_screenshot(driver, "btn_minMax_size - Exception Screenshot")
        assert False, f"{str(e)}\n{traceback.format_exc()}"


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - INPUT / CLEAR THE STOP LOSS FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def manage_stopLoss(driver, trade_type, type, stopLoss_field=None):

    # Remove the trailing ".0" if it exists
    if stopLoss_field.endswith(".0"):
        stopLoss_field = stopLoss_field[:-2]
    
    try:
        # Locate the input field for stop loss
        stopLoss_input = find_element_by_testid(driver, data_testid=f"{trade_type}-input-stoploss-{type}")
        
        # Clear the field if editing
        if trade_type == 'edit':
            clear_input_field(stopLoss_input)

        # Populate the field with the provided stop loss value
        populate_element_with_wait(driver, element=stopLoss_input, text=stopLoss_field)
        
    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "manageStopLoss - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - TAKE PROFIT FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Retrieve the Take Profit (Price / Points) field
def handle_takeProfit(driver, trade_type, tp_type):
    
    # Locate the Take Profit input field
    takeProfit_element = find_element_by_testid(driver, data_testid=f"{trade_type}-input-takeprofit-{tp_type}")
    
    # Clear the input field if in edit mode
    if trade_type == "edit":
        clear_input_field(takeProfit_element)
        
    # Return the take-profit element for further actions if required
    return takeProfit_element

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - BUTTON MIN / MAX TAKE PROFIT (+ / - BUTTON)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def btn_minMax_takeProfit(driver, trade_type, type, minMax, number_of_clicks):
    try:
        # Locate and click the min/max button
        button_minMax = find_element_by_testid(driver, data_testid=f"{trade_type}-input-takeprofit-{type}-{minMax}")
        click_element(button_minMax)

        # Locate the input field and determine the initial value and increment
        input_field = find_element_by_testid(driver, data_testid=f"{trade_type}-input-takeprofit-{type}")

        # Determine the initial value based on value_type (either float or int)
        initial_value_str = input_field.get_attribute("value")
        
        if type == "price":
            # Convert input value to float, default to 0.0 if empty
            initial_value = float(initial_value_str) if initial_value_str.strip() else 0.0
            
            # Retrieve the increment value for price
            increment = label_onePointEqual(driver, trade_type)
        elif type == "points":
            # Convert input value to int, default to 0 if empty
            initial_value = int(initial_value_str) if initial_value_str.strip() else 0
            
            # Set increment for points to 1
            increment = 1
        else:
            raise ValueError("Invalid value type. Must be 'price' or 'points'.")

        for i in range(number_of_clicks):
            click_element(button_minMax)

            # Get the updated value based on value_type
            updated_value_str = input_field.get_attribute("value")
            updated_value = float(updated_value_str) if type == "price" else int(updated_value_str)

            # Check if increment/decrement is as expected
            if minMax == "increase":
                difference = updated_value - initial_value
            elif minMax == "decrease":
                difference = initial_value - updated_value
            else:
                raise ValueError("Invalid value for minMax. Must be 'increase' or 'decrease'.")

            # Assert that the difference is correct based on the type
            if type == "price":
                assert abs(difference - increment) < 1e-6, f"Value did not change by {increment} after click {i+1}. Difference: {difference:.6f}"
            else:  # for "points"
                assert abs(difference - increment) == 0, f"Value did not change by {increment} after click {i+1}. Difference: {difference}"

            # Update initial_value for next iteration
            initial_value = updated_value

            # Attach text logs for the clicks and final value for reporting
            attach_text(str(number_of_clicks), f"{minMax.capitalize()} button clicked {i+1} times")
            attach_text(f"{updated_value:.6f}" if type == "price" else str(updated_value), f"Final value: {updated_value:.6f}" if type == "price" else f"Final value: {updated_value}")

        # Final check: ensure total increment or decrement matches the expected value
        final_value = float(input_field.get_attribute("value")) if type == "price" else int(input_field.get_attribute("value"))
        expected_value = initial_value + (increment * number_of_clicks) if minMax == "increase" else initial_value - (increment * number_of_clicks)
        
        # Final check: ensure total increment or decrement matches the expected value
        assert abs(final_value - expected_value), f"Final value does not match expected value. Expected: {expected_value}, Got: {final_value}"

    except Exception as e:
        take_screenshot(driver, "btn_minMax_size - Exception Screenshot")
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - INPUT / CLEAR THE TAKE PROFIT FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def manage_takeProfit(driver, trade_type, type, takeProfit_field=None):

    # Remove the trailing ".0" if it exists
    if takeProfit_field.endswith(".0"):
        takeProfit_field = takeProfit_field[:-2]
    
    try:
        # Locate the input field for take profit
        takeProfit_input = find_element_by_testid(driver, data_testid=f"{trade_type}-input-takeprofit-{type}")

        # Clear the field if editing
        if trade_type == 'edit':
            clear_input_field(takeProfit_input)
            
        # Populate the field with the provided stop loss value
        populate_element_with_wait(driver, element=takeProfit_input, text=takeProfit_field)
        
    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "manageTakeProfit - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - SPECIFIED DATE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def select_specified_date(driver, trade_type, expiryDate, targetMonth):
    try:    
        # Click on the input field for choosing date
        date_field = find_element_by_testid(driver, data_testid=f"{trade_type}-input-expiry-date")
        javascript_click(driver, element=date_field)
        # click_element_with_wait(driver, element=date_field)

        while True:
            year_month = find_element_by_xpath_with_wait(driver, "//button[@class='react-calendar__navigation__label']").text
            currentMonth = datetime.strptime(year_month, "%b %Y")
            if currentMonth == targetMonth:
                break
            else:
                next_btn = find_element_by_xpath_with_wait(driver, "//button[contains(@class, 'react-calendar__navigation__next-button')]")
                click_element_with_wait(driver, element=next_btn)

        start_date_picker = find_element_by_xpath_with_wait(driver, f"//div[contains(@class, 'month-view__days')]/button[not(contains(@class, 'neighboringMonth'))]/abbr[.='{expiryDate}']")
        click_element_with_wait(driver, element=start_date_picker)
        
    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "select_specified_date - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - SPECIFIED TIME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def select_time_option(driver, trade_type, option_type, option_value):
    try:
        
        # Find the time options container
        time_options_container = find_element_by_testid(driver, data_testid=f"{trade_type}-input-expiry-time-{option_type}")
        
        # Find the specific time option element
        time_option = time_options_container.find_element(By.XPATH, f"//div[text()='{option_value}']")
        
        javascript_click(driver, element=time_option)
        
    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "select_time_option - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
        

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - SPECIFIED DATE AND TIME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def select_specified_date_and_time(driver, trade_type, expiryDate, targetMonth, hour_option, min_option):
    try:
        
        # Select the specified date
        select_specified_date(driver, trade_type, expiryDate, targetMonth)

        # Click on the input field for choosing time.
        time_field = find_element_by_testid(driver, data_testid=f"{trade_type}-input-expiry-time")

        javascript_click(driver, element=time_field)
        # click_element_with_wait(driver, element=time_field)

        # Find and click the hour option
        select_time_option(driver, trade_type, "hour", hour_option)

        # Find and click the minute option
        select_time_option(driver, trade_type, "minute", min_option)
        
    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "select_specified_date_and_time - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - EXPIRY FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def expiry(driver, trade_type, expiryType, expiryDate, targetMonth, hour_option, min_option, specifiedDate: bool = False):
    try:

        # Click on the expiry dropdown
        expiry_dropdown = find_element_by_testid(driver, data_testid=f"{trade_type}-dropdown-expiry")
        javascript_click(driver, element=expiry_dropdown)
        # click_element_with_wait(driver, element=expiry_dropdown)

        # Select the Expiry option dropdown
        expiry_options = find_element_by_testid(driver, data_testid=f"{trade_type}-dropdown-expiry-{expiryType}")
        click_element_with_wait(driver, element=expiry_options)
        
        if specifiedDate: # IF TRUE
            if expiryType == "specified-date":
                select_specified_date(driver, trade_type, expiryDate, targetMonth)
            elif expiryType == "specified-date-and-time":
                select_specified_date_and_time(driver, trade_type, expiryDate, targetMonth, hour_option, min_option)

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "expiry - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - PLACE / UPDATE BUTTON
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_trade_action(driver, trade_type):
    try:

        # Locate the trade action button using the provided trade_type
        trade_action = find_element_by_testid(driver, data_testid=f"{trade_type}-button-order")
        assert trade_action is not None, f"Trade action button not found for {trade_type}"

        # Click the button and wait for the action to complete
        click_element_with_wait(driver, element=trade_action)

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "button_trade_action - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - TRADE CONFIRMATION DIALOG DETAILS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def trade_ordersConfirmationDetails(driver, trade_type):
    try:

        result = []

        # Retrieve headers for trade confirmation
        # trade_order_header_elements = find_list_of_elements_by_xpath(driver, "//*[contains(@data-testid, 'confirmation-label')]")
        trade_order_header_elements = find_list_of_elements_by_xpath(driver, "//*[contains(@resource-id, 'confirmation-label')]")

        trade_confirmation_headers = [header.text for header in trade_order_header_elements]
        
        # Handle different table headers ("Price" or "Entry Price") for consistency
        for i, header in enumerate(trade_confirmation_headers):
            if header in ("Price"):
                trade_confirmation_headers[i] = "Entry Price"
                break
            
        # Retrieve order type
        # //*[contains(@resource-id, 'confirmation-order-type')]
        order_type_element = find_element_by_xpath(driver, "//*[contains(@resource-id, 'confirmation-order-type')]")
        trade_confirmation_headers.append("Type")

        # Retrieve symbol name
        symbol_name_element = find_element_by_xpath(driver, "//*[contains(@resource-id, 'confirmation-symbol')]")
        trade_confirmation_headers.append("Symbol")
        
        # Wait for the elements to be present and extract their text
        elements = find_list_of_elements_by_testid(driver, data_testid=f"{trade_type}-confirmation-value")

        for element in elements:
            result.append(get_label_of_element(element))

        label_order_type = get_label_of_element(order_type_element)
        result.append(label_order_type)

        label_symbol_name = get_label_of_element(symbol_name_element)
        result.append(label_symbol_name)
        
        # Handle "edit" trade type and extract order number if available
        if trade_type == "edit":

            # Check if "order_number_element" exists
            order_number_elements = find_element_by_testid(driver, data_testid=f"edit-confirmation-order-id")
            extracted_orderID = get_label_of_element(order_number_elements)

            if order_number_elements:       
                order_number = re.search(r'\d+', extracted_orderID).group()
                
                # Append the order number to the result list
                result.append(order_number)
                
                # Add the new header for order number only if it exists
                trade_confirmation_headers.append("Order No.")

        # Create a DataFrame using the data
        trade_order_details = pd.DataFrame([result], columns=trade_confirmation_headers)
        trade_order_details['Section'] = "Trade Confirmation Details"
        
        # Transpose DataFrame and format it for output
        master_df_transposed = trade_order_details.set_index('Section').T.fillna('-')
        overall = tabulate(master_df_transposed, headers='keys', tablefmt='grid', stralign='center')
        attach_text(overall, name="Trade Confirmation Details")

        # To click on the confirm button
        button_confirmation = find_element_by_testid(driver, data_testid=f"{trade_type}-confirmation-button-confirm")
        
        # button_confirmation = visibility_of_element_by_xpath(driver, "//*[contains(@resource-id, 'button-confirm')]")
        
        click_element_with_wait(driver, element=button_confirmation)
        
        # spinner_element(driver)

        # return trade_order_details

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "trade_ordersConfirmationDetails - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - COMPARE THE DATA TO ENSURE IT MATCH
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def compare_dataframes(driver=main_driver, df1, df2, name1, name2, required_columns):
    """
    Compare two dataframes and assert if the required columns match between them.

    Args:
    - df1 (DataFrame): First dataframe
    - df2 (DataFrame): Second dataframe
    - name1 (str): Name of the first dataframe for reporting
    - name2 (str): Name of the second dataframe for reporting
    - required_columns (list): List of column names required for comparison

    Raises:
    - AssertionError: If the required columns do not match between the two dataframes
    """
    try:
            
        # Check if inputs are valid DataFrames
        if not isinstance(df1, pd.DataFrame):
            raise TypeError(f"df1 is not a DataFrame, it is a {type(df1)}")
        if not isinstance(df2, pd.DataFrame):
            raise TypeError(f"df2 is not a DataFrame, it is a {type(df2)}")

        # Concatenate the dataframes
        master_df = pd.concat([df1, df2])

        # Group by 'Order No.' if it exists, otherwise treat as a single group
        if 'Order No.' in df1.columns and 'Order No.' in df2.columns:
            grouped = master_df.groupby('Order No.')
        else:
            grouped = [('All', master_df)]

        for orderID, group in grouped:
            # Transpose the group dataframe and fill missing values with '-'
            group_transposed = group.set_index('Section').T.fillna('-')

            # Convert the transposed dataframe to a formatted table using tabulate
            formatted_table = tabulate(group_transposed, tablefmt='grid', stralign='center', headers='keys')

            # Attach the formatted table as an attachment in allure report or print for debugging
            attach_text(formatted_table, name=f"Table Comparison for {name1} and {name2} - {orderID}")

            # Extract the index values from the transposed DataFrame
            desired_index = group_transposed.index.tolist()

            # Check if the required columns exist in the index of the transposed dataframe
            if set(required_columns).issubset(desired_index):
                # Get values of 'df1' and 'df2' columns using the desired index
                df1_values = group_transposed.loc[desired_index, name1]
                df2_values = group_transposed.loc[desired_index, name2]

                # Find mismatched values
                mismatched = (df1_values != df2_values) & df1_values.index.isin(required_columns)

                if mismatched.any():
                    # Display mismatched values
                    error_message = f"Values do not match for {orderID} in the following fields:\n"
                    mismatched_details = pd.DataFrame({
                        'Field': df1_values[mismatched].index,
                        f'{name1} Value': df1_values[mismatched],
                        f'{name2} Value': df2_values[mismatched]
                    })
                    error_message += mismatched_details.to_string(index=False)

                    # Raise an assertion error with the error message
                    assert False, error_message

                else:
                    attach_text(f"All values match for {orderID}", name="Values Comparison Result")
            else:
                # Required columns not found in the index
                missing_columns = set(required_columns) - set(desired_index)
                attach_text(f"Missing columns for {orderID}: {missing_columns}", name="Missing Data")
                assert False, f"Required columns not found in the index for {orderID}"

    except Exception as e:
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                PRINT DATA
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def process_and_print_data(*dfs, group_by_order_no: bool = False):
    try:
            
        # Concatenate the dataframes
        master_df = pd.concat(dfs)
        
        if group_by_order_no:
            # Group by 'Order No.'
            grouped = master_df.groupby('Order No.')
            
            for order_no, group in grouped:
                # Transpose the group dataframe and fill missing values with '-'
                group_transposed = group.set_index('Section').T.fillna('-')
                
                # Print the tabulated data with the 'Result' column for each group
                overall = tabulate(group_transposed, headers='keys', tablefmt='grid', stralign='center')
                attach_text(overall, name=f"Table for Order No.: {order_no}")
        else:
            # Transpose the concatenated dataframe and fill missing values with '-'
            master_df_transposed = master_df.set_index('Section').T.fillna('-')
            
            # Print the tabulated data with the 'Result' column for the overall dataframe
            overall = tabulate(master_df_transposed, headers='keys', tablefmt='grid', stralign='center')
            attach_text(overall, name="Overall Table Comparison")

    except Exception as e:
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""