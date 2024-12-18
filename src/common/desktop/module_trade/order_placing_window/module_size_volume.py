import re
import random

from constants.helper.driver import delay
from constants.helper.element import click_element, click_element_with_wait, visibility_of_element_by_testid, clear_input_field, find_element_by_testid, populate_element_with_wait
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text
from common.desktop.module_trade.order_placing_window.module_fill_policy import fillPolicy_type


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
                element = visibility_of_element_by_testid(driver, testid)
                current_state = state
                attach_text(f"Current button state: Swap to {state.capitalize()}", name="Swap Current Status")

                # If the current state matches the desired state, no action is needed
                if state == desired_state:
                    attach_text(f"Desired state is '{desired_state}' no action needed.", name="Toggle Button Status")
                    return desired_state  # Return after swapping
                else:
                    attach_text(f"Swapping to'{desired_state.capitalize()}' as desired.", name="Updated Status")
                    swap_button = find_element_by_testid(driver, testid) # Perform the swap
                    click_element(swap_button)
                    return desired_state  # Return after swapping

            except Exception:
                # If the element is not found, continue checking the other state
                continue

        # If no valid state is found
        if current_state is None:
            raise Exception("Unable to determine current swap state.")

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - SIZE / VOLUME FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def input_size_volume(driver, desired_state="units"):
    try:
        
        state = swap_units_volume(driver, desired_state)
    
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
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CLOSE - PARTIAL SIZE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def close_partialSize(driver, set_fillPolicy: bool = False, clearField: bool = False):
    try:
        
        # Find the element containing the maximum value label
        max_value_element = find_element_by_testid(driver, data_testid="close-order-input-volume-max-value")

        # Extract the maximum value text from the element
        max_value_text = max_value_element.text.split()[1]  # Assuming it's in text format
        
        # Convert the maximum value to a float (handle both integer and decimal values)
        max_value = float(max_value_text)
                
        # Determine the appropriate minimum value step based on the magnitude of max_value
        if max_value < 0.1:
            min_value_step = 0.01
        elif max_value < 1.0:
            min_value_step = 0.1
        else:
            min_value_step = 0.01  # Default to 0.01 step for larger values

        # Randomly decide whether to generate an integer or a decimal
        if random.choice([True, False]) and max_value >= 1.0:  # Only generate integers if max_value >= 1.0
            # Generate a random integer between 1 and the retrieved maximum value
            random_value = random.randint(1, int(max_value))
        else:
            # Generate a random decimal between 0 and the retrieved maximum value with the appropriate step
            random_value = round(random.uniform(min_value_step, max_value), 2)
            
        partialClose_input = find_element_by_testid(driver, data_testid="close-order-input-volume")
        
        if clearField:
            # Select all text and delete the selected text
            clear_input_field(partialClose_input)
            populate_element_with_wait(driver, element=partialClose_input, text=str(random_value))

        if set_fillPolicy:
            fillPolicy_type(driver, trade_type="close-order")

        # action_button = find_element_by_testid(driver, data_testid=close_button)
        action_button = find_element_by_testid(driver, data_testid="close-order-button-submit")
        click_element_with_wait(driver, element=action_button)

    except Exception as e:
        handle_exception(driver, e)

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
        
        swap_units_volume(driver, desired_state="units")
        
        delay(0.5)
        
        button_minMax = find_element_by_testid(driver, data_testid=f"trade-input-volume-{minMax}")
        
        input_field = find_element_by_testid(driver, data_testid=f"trade-input-volume")

        # Get the initial value of the input field and set it to 0.0 if empty
        initial_value_str = input_field.get_attribute("value")
        initial_value = float(initial_value_str) if initial_value_str.strip() else 0.0

        # Get the placeholder attribute
        placeholder_value = input_field.get_attribute('placeholder')
        increment = float(re.search(r'([\d\.]+)', placeholder_value).group(1))

        for i in range(number_of_clicks):
            click_element(button_minMax)
            
            # Get the updated value after the click and set it to 0.0 if empty
            updated_value_str = input_field.get_attribute("value")
            updated_value = float(updated_value_str) if updated_value_str.strip() else 0.0
            print(f"Size - updated value after click {i+1}: {updated_value}")

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
            
            assert abs(final_value - expected_value), f"Final value does not match expected value. Expected: {expected_value:.2f}, Got: {final_value:.2f}"

            attach_text(str(number_of_clicks), name=f"{minMax.capitalize()} button clicked {i+1} times")
            attach_text(f"{final_value:.2f}", name=f"Final value: {final_value:.2f}")
            
    except Exception as e:
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""