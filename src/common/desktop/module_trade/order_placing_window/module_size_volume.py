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

def swap_units_volume(driver, desired_state: str):
    """
    This function toggles between two radio button states: 'units' and 'volume'.
    It checks the current state and performs the toggle only if the desired state is different from the current one.

    Arguments:
    - desired_state: The state to which the button should be toggled, either 'units' or 'volume'.

    Returns:
    - str: The final state after attempting the swap (either 'units' or 'volume').

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Define both possible 'data-testid' values for the radio button states
        swap_options = {
            "units": "trade-swap-to-units",
            "volume": "trade-swap-to-volume"
        }

        # Verify if the desired state is valid
        if desired_state not in swap_options:
            raise ValueError(f"Invalid desired state: '{desired_state}'. Must be either 'units' or 'volume'.")

        # Identify the current state of the radio button (checked/unchecked)
        current_state = None
        
        for state, testid in swap_options.items():
            try:
                # Check the visibility of the element and capture the current state
                element = visibility_of_element_by_testid(driver, testid)
                current_state = state
                attach_text(f"Current button state: Swap to {state.capitalize()}", name="Swap Current Status")

                # If the current state matches the desired state, no action is needed
                if state == desired_state:
                    attach_text(f"Desired state is '{desired_state}' no action needed.", name="Toggle Button Status")
                    return desired_state  # Return after swapping
                else:
                    # Log the action of swapping and perform the toggle
                    attach_text(f"Swapping to'{desired_state.capitalize()}' as desired.", name="Updated Status")
                    swap_button = find_element_by_testid(driver, testid) # Perform the swap
                    click_element(swap_button)
                    return desired_state  # Return after swapping

            except Exception:
                # If the element is not found, continue checking the other state
                continue

        # If no valid state is found (i.e., neither state exists in the DOM)
        if current_state is None:
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

def input_size_volume(driver, desired_state: str = "units"):
    """
    This function inputs a random value into the 'size' or 'volume' input field based on the current state.
    The state toggles between 'units' and 'volume', and random values are generated accordingly.

    Arguments:
    - desired_state: The desired state ('units' or 'volume').

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Ensure the state is set correctly (either 'units' or 'volume')
        state = swap_units_volume(driver, desired_state)
    
        # Locate the input field for 'size' or 'volume'
        size_input = find_element_by_testid(driver, data_testid="trade-input-volume")
                
        # Determine state and value range based on 'swap' and 'desired_state'
        if state == "units": # (swap to volume)
            min_val, max_val = 1, 100
        else:  # If state is 'volume' (swap to units)
            min_val, max_val = 1000, 10000

        # Randomly decide whether to generate an integer or a decimal within the specified range
        if random.choice([True, False]):
            # Generate a random integer within the specified range
            random_value = random.randint(min_val, max_val)
        else:
            # Generate a random decimal within the specified range, rounded to two decimal places
            random_value = round(random.uniform(min_val, max_val), 2)
        
        # Populate the input field with the random value
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

def close_partialSize(driver, set_fillPolicy: bool = False, clearField: bool = False):
    """
    This function handles the partial close of an order by generating a random value between 0 and the maximum allowed
    value and submitting the close order request.

    Arguments:
    - set_fillPolicy (bool): Whether to set the fill policy before submitting the order.
    - clearField (bool): Whether to clear the input field before populating it with the new value.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        
        # Locate the element containing the maximum value (e.g., "Max: 100.0")
        max_value_element = find_element_by_testid(driver, data_testid="close-order-input-volume-max-value")

        # Extract the max value text and convert it to a float
        max_value_text = max_value_element.text.split()[1]  # Assuming the text is like "Max: 100.0"
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
        
        # If clearField is True, clear the input field before entering the new value
        if clearField:
            # Select all text and delete the selected text
            clear_input_field(partialClose_input)
            populate_element_with_wait(driver, element=partialClose_input, text=str(random_value))

        # If set_fillPolicy is True, set the fill policy before submitting the order
        if set_fillPolicy:
            fillPolicy_type(driver, trade_type="close-order")

        # Find the submit button and click it to submit the partial close order
        action_button = find_element_by_testid(driver, data_testid="close-order-button-submit")
        click_element(element=action_button)
        # click_element_with_wait(driver, element=action_button)

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
    """
    This function simulates clicks on the min/max button for adjusting the trade volume size,
    checks if the volume size is incremented or decremented correctly, and ensures the correct
    final value based on the number of clicks and placeholder increment.

    Arguments:
    - minMax: The operation type, either 'increase' or 'decrease'.
    - number_of_clicks: The number of clicks to simulate on the min/max button.

    Raises:
    - ValueError: If 'minMax' is neither 'increase' nor 'decrease'.
    - AssertionError: If the increment or decrement does not match the expected value.
    """
    try:
        # Step 1: Set the units to 'volume'
        swap_units_volume(driver, desired_state="units")
        
        # Step 2: Short delay to ensure element visibility (if required)
        delay(0.5)
        
        # Step 3: Locate the min/max button and volume input field
        button_minMax = find_element_by_testid(driver, data_testid=f"trade-input-volume-{minMax}")
        input_field = find_element_by_testid(driver, data_testid=f"trade-input-volume")

        # Step 4: Get the initial value of the input field and set it to 0.0 if empty
        initial_value_str = input_field.get_attribute("value")
        initial_value = float(initial_value_str) if initial_value_str.strip() else 0.0

        # Step 5: Get the placeholder value to determine the increment size
        placeholder_value = input_field.get_attribute('placeholder')
        increment = float(re.search(r'([\d\.]+)', placeholder_value).group(1))

        # Step 6: Perform the clicks and check the results
        for i in range(number_of_clicks):
            click_element(button_minMax)
            
            # Get the updated value after the click and set it to 0.0 if empty
            updated_value_str = input_field.get_attribute("value")
            updated_value = float(updated_value_str) if updated_value_str.strip() else 0.0
            print(f"Size - updated value after click {i+1}: {updated_value}")

            # Step 7: Verify that each increment/decrement matches the expected change
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
            
            # Assert if the final value doesn't match the expected value
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