import re
import random

from enums.main import ButtonModuleType, SwapOptions, TradeConstants
from constants.element_ids import DataTestID

from constants.helper.driver import delay

from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element_android_app import get_label_of_element, click_element, click_element_with_wait, clear_input_field, find_element_by_testid, find_element_by_testid_with_wait, find_visible_element_by_testid, populate_element_with_wait

from common.mobileapp.module_trade.order_placing_window.module_fill_policy import fill_policy_type


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - SWAP BETWEEN SIZE (VOLUME) / UNITS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def swap_units_volume(driver, desired_state: SwapOptions):
    try:
        
        # Define both possible 'data-testid' values for the radio button states
        swap_options = {
            SwapOptions.UNITS: DataTestID.TRADE_SWAP_TO_UNITS,
            SwapOptions.VOLUME:  DataTestID.TRADE_SWAP_TO_VOLUME
        }

        # Identify the current state of the radio button (checked/unchecked)
        current_state = None
        for state, testid in swap_options.items():
            try:

                # find_visible_element_by_testid(driver, testid)
                find_element_by_testid_with_wait(driver, data_testid=testid)
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
            # return desired_state == False
            raise Exception("Unable to determine current swap state.")

    except Exception as e:
        # Handle any exceptions that occur during the execution
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

def input_size_volume(driver, desired_state: SwapOptions = SwapOptions.UNITS, swap: bool = True):
    try:
        delay(2)
        
        size_input = find_element_by_testid_with_wait(driver, data_testid=DataTestID.TRADE_INPUT_VOLUME)
        
        # Determine state and value range based on 'swap' and 'desired_state'
        if swap: # If swap is true
            state = swap_units_volume(driver, desired_state)
            if state == SwapOptions.UNITS: # (swap to volume)
                min_val, max_val = 1, 100
            else: # (swap to units)
                min_val, max_val = 1000, 10000
        else: # OCT enable
            min_val, max_val = 1, 100

        # Randomly decide whether to generate an integer or a decimal within the specified range
        if random.choice([True, False]):
            # Generate a random integer within the specified range
            random_value = random.randint(min_val, max_val)
        else:
            # Generate a random decimal within the specified range, rounded to two decimal places
            random_value = round(random.uniform(min_val, max_val), 2)

        # Populate the input field with the generated value
        populate_element_with_wait(driver, element=size_input, text=str(random_value))

    except Exception as e:
        # Handle any exceptions that occur during the execution
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

def close_partial_size(driver, close_options: TradeConstants = TradeConstants.NONE):
    try:
        
        # Find the element containing the maximum value label
        max_value_element = find_element_by_testid(driver, data_testid=DataTestID.CLOSE_ORDER_INPUT_VOLUME_MAX_VALUE)

        # Extract the maximum value text from the element
        # max_value_text = max_value_element.text.split()[1]  # Assuming it's in text format
        max_value_text = get_label_of_element(element=max_value_element).split()[1]
        print("max value", max_value_text)
        
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
            random_value = random.randint(1, int(max_value))
        else:
            # Generate a random decimal between 0 and the retrieved maximum value with the appropriate step
            random_value = round(random.uniform(min_value_step, max_value), 2)

        # Find the input field for partial close size
        partialClose_input = find_element_by_testid(driver, data_testid=DataTestID.CLOSE_ORDER_INPUT_VOLUME)

        if TradeConstants.CLEAR_FIELD in close_options:
            # Select all text and delete the selected text
            clear_input_field(partialClose_input)
            populate_element_with_wait(driver, element=partialClose_input, text=str(random_value))

        if TradeConstants.SET_FILL_POLICY in close_options:
            fill_policy_type(driver, trade_type=ButtonModuleType.CLOSE)

        # Find the button to confirm the close action and click it
        action_button = find_element_by_testid(driver, data_testid=DataTestID.CLOSE_ORDER_BUTTON_SUBMIT)
        click_element_with_wait(driver, element=action_button)

    except Exception as e:
        # Handle any exceptions that occur during the execution
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

def btn_minMax_size(driver, minMax: str, number_of_clicks: int):
    try:
        
        delay(0.2)
        
        # Find the button for increasing or decreasing the trade input volume
        button_min_max = find_visible_element_by_testid(driver, data_testid=f"trade-input-volume-{minMax}")
        
        # Find the input field for the trade volume
        input_field = find_visible_element_by_testid(driver, data_testid=DataTestID.TRADE_INPUT_VOLUME)

        # Get the initial value of the input field and set it to 0.0 if empty
        initial_value_str = input_field.get_attribute("text")
        initial_value = float(initial_value_str) if initial_value_str.strip() else 0.0

        # Get the placeholder attribute, which holds the increment value (e.g., "0.01")
        placeholder_value = input_field.get_attribute('text')

        # Extract the increment value from the placeholder using regular expression
        increment = float(re.search(r'([\d\.]+)', placeholder_value).group(1))

        # Loop through the number of clicks specified
        for i in range(number_of_clicks):
            # Click the button (either increase or decrease)
            click_element(button_min_max)
            
            # Get the updated value after the click and set it to 0.0 if the field is empty
            updated_value_str = input_field.get_attribute("text")
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
            attach_text(str(number_of_clicks), name=f"{minMax.capitalize()} button clicked {i+1} times")
            attach_text(f"{final_value:.2f}", name=f"Final value: {final_value:.2f}")
            
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""