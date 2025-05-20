import random
from selenium.webdriver.common.by import By

from enums.main import ButtonModuleType, SwapOptions, TradeConstants
from constants.element_ids import DataTestID

from constants.helper.driver import delay
from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, get_label_of_element, find_visible_element_by_testid, clear_input_field, find_element_by_testid, populate_element_with_wait

from common.desktop.module_trade.order_placing_window.module_fill_policy import fill_policy_type
from common.desktop.module_trade.order_placing_window.opw_button_action import button_trade_module
from enums.main import ButtonModuleType


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - SWAP BETWEEN SIZE (VOLUME) / UNITS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def swap_units_volume(driver, desired_state: SwapOptions):
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
            SwapOptions.UNITS: DataTestID.TRADE_SWAP_TO_UNITS,
            SwapOptions.VOLUME:  DataTestID.TRADE_SWAP_TO_VOLUME
        }
        
        # Identify the current state of the radio button (checked/unchecked)
        current_state = None
        
        for state, testid in swap_options.items():
            try:
                # Check the visibility of the element and capture the current state
                find_visible_element_by_testid(driver, testid)
                current_state = state
                attach_text(f"Current button state: Swap to {state.capitalize()}", name="Swap Current Status")

                # If the current state matches the desired state, no action is needed
                if state == desired_state:
                    attach_text(f"Desired state is '{desired_state}' no action needed.", name="Toggle Button Status")
                    return desired_state  # Return after swapping
                else:
                    # Log the action of swapping and perform the toggle
                    attach_text(f"Swapping to '{desired_state.capitalize()}' as desired.", name="Updated Status")
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
                                                TRADE - SWAP VOLUME UNITS CALCULATION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def swap_units_volume_conversion(driver, module_type: ButtonModuleType, desired_state="volume"):
    try:
        delay(0.5)

        # Retrieve contract size and navigate to the trade module
        contract_size, _, _ = button_trade_module(driver, trade_type=ButtonModuleType.SPECIFICATION)
        if not contract_size or contract_size <= 0:
            raise ValueError("Invalid contract size fetched")
        print("Contract Size:", contract_size)

        button_trade_module(driver, module_type)
        
        delay(0.5)

        # Get the current input state and the entered value
        current_state, input_value = input_size_volume(driver, desired_state)
        print("Input Value:", input_value)
        print("Current State:", current_state)

        # Fetch label and displayed conversion value
        find_visible_element_by_testid(driver, data_testid="trade-volume-info-label")
        displayed_conversion_value = find_visible_element_by_testid(driver, data_testid="trade-volume-info-value")
        displayed_value = round(float(get_label_of_element(element=displayed_conversion_value)), 2)
        print("Displayed Value:", displayed_value)

        # Calculate the expected conversion value
        if current_state == "volume":
            expected_conversion_value = round(input_value * contract_size, 2)
        else:
            expected_conversion_value = round(input_value / contract_size, 2)
        print(f"Expected Conversion Value ({current_state}):", expected_conversion_value)

        # Compare values
        assert abs(expected_conversion_value == displayed_value), f"Mismatch: expected {expected_conversion_value}, got {displayed_value}"

    except Exception as error:
        handle_exception(driver, error)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - SIZE / VOLUME FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def input_size_volume(driver, desired_state: SwapOptions = SwapOptions.UNITS):
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
        print("state", state)
        
        delay(0.5)
    
        # Locate the input field for 'size' or 'volume'
        size_input = find_element_by_testid(driver, data_testid=DataTestID.TRADE_INPUT_VOLUME)
                
        # Determine state and value range based on 'swap' and 'desired_state'
        if state == SwapOptions.UNITS: # (swap to volume)
            min_val, max_val = 1, 20
        else:  # If state is 'volume' (swap to units)
            min_val, max_val = 10, 200

        # Randomly decide whether to generate an integer or a decimal within the specified range
        if random.choice([True, False]):
            # Generate a random integer within the specified range
            random_value = random.randint(min_val, max_val)
        else:
            # Generate a random decimal within the specified range, rounded to two decimal places
            random_value = round(random.uniform(min_val, max_val), 2)
            
        print("random generated size/volume", random_value)
        
        # Populate the input field with the random value
        populate_element_with_wait(driver, element=size_input, text=str(random_value))
        
        return state, random_value
        
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
        max_value_element = find_element_by_testid(driver, data_testid=DataTestID.CLOSE_ORDER_INPUT_VOLUME_MAX_VALUE)

        # Extract the max value text and convert it to a float
        max_value_text = max_value_element.text.split()[1]  # Assuming the text is like "Max: 100.0"
        max_value = float(max_value_text)
        print("max value", max_value)
                
        # Determine the appropriate minimum value step based on the magnitude of max_value
        if max_value < 0.1:
            min_value_step = 0.01
        elif max_value < 1.0:
            min_value_step = 0.1
        else:
            min_value_step = 0.01  # Default to 0.01 step for larger values

        # Randomly decide whether to generate an integer or a decimal
        if random.choice([True, False]) and max_value > 1.0:  # Only generate integers if max_value >= 1.0
            # Generate a random integer between 1 and the retrieved maximum value
            random_value = random.randint(1, int(max_value))
        else:
            # Generate a random decimal between 0 and the retrieved maximum value with the appropriate step
            random_value = round(random.uniform(min_value_step, max_value), 2)

        print("random value for partial close", random_value)
            
        partial_close_input = find_element_by_testid(driver, data_testid=DataTestID.CLOSE_ORDER_INPUT_VOLUME)
        
        # If clearField is True, clear the input field before entering the new value
        if TradeConstants.CLEAR_FIELD in close_options:
            # Select all text and delete the selected text
            clear_input_field(partial_close_input)
            populate_element_with_wait(driver, element=partial_close_input, text=str(random_value))

        # If set_fillPolicy is True, set the fill policy before submitting the order
        if TradeConstants.SET_FILL_POLICY in close_options:
            fill_policy_type(driver, trade_type=ButtonModuleType.CLOSE)

        # Find the submit button and click it to submit the partial close order
        action_button = find_element_by_testid(driver, data_testid=DataTestID.CLOSE_ORDER_BUTTON_SUBMIT)
        click_element(element=action_button)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - BUTTON MIN / MAX SIZE (VOLUME) (+ / - BUTTON)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def verify_volume_min_max_buttons(driver, trade_type, actions: list, size_volume_step=None):
    """
    This function simulates clicks on the min/max button for adjusting the trade volume size,
    checks if the volume size is incremented or decremented correctly, considering the step's precision,
    and ensures the correct final value based on the number of clicks and step increment.

    Arguments:
    - trade_type: The type of trade (e.g., 'trade', 'close-order').
    - actions: A list of tuples where each tuple contains (min_max, number_of_clicks). 
               'min_max' can be 'increase' or 'decrease'.
               'number_of_clicks' is the number of clicks to simulate for that action.
    - size_volume_step: The step size for volume increments/decrements.

    Raises:
    - ValueError: If 'min_max' is neither 'increase' nor 'decrease'.
    - AssertionError: If the increment or decrement does not match the expected value.
    """
    try:
        if trade_type == "trade":
            # Step 1: Set the units to 'volume'
            swap_units_volume(driver, desired_state="volume")
        
        # Step 2: Short delay to ensure element visibility (if required)
        delay(0.5)
        
        # Step 3: Locate the volume input field
        input_field = find_element_by_testid(driver, data_testid=f"{trade_type}-input-volume")

        # Step 4: Get the initial value of the input field and set it to 0.0 if empty
        initial_value_str = input_field.get_attribute("value")
        initial_value = float(initial_value_str) if initial_value_str.strip() else 0.0
        
        # Step 5: Determine the decimal places based on size_volume_step
        if size_volume_step is not None:
            # Convert to a string to find decimal places
            step_str = f"{size_volume_step:.10f}".rstrip('0').rstrip('.')
            if '.' in step_str:
                decimal_places = len(step_str.split('.')[1])
            else:
                decimal_places = 0
        else:
            decimal_places = 0  # Default, though size_volume_step should be provided
        
        print(f"Specification - Lot Size / Volume Step: {size_volume_step} (Decimal places: {decimal_places})")

        # Step 6: Loop over the actions and perform clicks for each one
        for min_max, number_of_clicks in actions:
            button_min_max = find_element_by_testid(driver, data_testid=f"{trade_type}-input-volume-{min_max}")
            initial_value_before_action = initial_value  # Save initial value before this action

            for i in range(number_of_clicks):
                click_element(button_min_max)
                
                # Get the updated value after the click
                updated_value_str = input_field.get_attribute("value")
                updated_value = float(updated_value_str) if updated_value_str.strip() else 0.0
                print(f"Size - updated value after {min_max} click {i+1}: {updated_value}")

                # Calculate expected value after this click
                if min_max == "increase":
                    expected_value = initial_value + size_volume_step
                else:
                    expected_value = initial_value - size_volume_step
                
                # Round to the step's decimal places
                expected_rounded = round(expected_value, decimal_places)
                
                # Verify the updated value matches the rounded expected value
                assert abs(updated_value - expected_rounded) < 1e-6, (f"After {i+1} {min_max} click(s): Expected {expected_rounded}, got {updated_value}")
                
                initial_value = updated_value  # Update for next iteration

            # Final check after all clicks in this action
            final_value = float(input_field.get_attribute("value"))
            
            # Calculate total expected value for the action
            if min_max == "increase":
                total_expected = initial_value_before_action + (size_volume_step * number_of_clicks)
            else:
                total_expected = initial_value_before_action - (size_volume_step * number_of_clicks)
            
            total_expected_rounded = round(total_expected, decimal_places)
            
            assert abs(final_value - total_expected_rounded) < 1e-6, (
                f"Final value mismatch after {number_of_clicks} {min_max} clicks: "
                f"Expected {total_expected_rounded}, got {final_value}"
            )

            # Logging
            attach_text(str(number_of_clicks), name=f"{min_max.capitalize()} button clicked {number_of_clicks} times")
            attach_text(f"{final_value:.{decimal_places}f}", name=f"Final value: {final_value:.{decimal_places}f}")
        
    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - MIN / MAX BUTTON
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def verify_button_behavior_at_min_max(driver, trade_type, lot_size):
    try:
        
        # Step 1: Locate the (Trade / Close) input field for the current value
        input_field = find_element_by_testid(driver, data_testid=f"{trade_type}-input-volume")

        # Step 2: Retrieve the current value from the input field
        current_value_str = input_field.get_attribute("value")
        current_value = float(current_value_str) if current_value_str.strip() else 0.0
        print(f"Current Value: {current_value}")

        # Step 3: Locate the maximum value element and retrieve its value
        max_value_element = find_element_by_testid(driver, data_testid="close-order-input-volume-max-value")
        max_value_text = max_value_element.text.split()[1]  # Assuming the format "Max: 100.0"
        max_value = float(max_value_text)
        print(f"Max Value: {max_value}")

        # Step 4: Verify behavior when current value is at max value
        max_button = find_element_by_testid(driver, data_testid="close-order-input-volume-static-max")
        if current_value == max_value:
            # Check if the max button is disabled
            parent_div = max_button.find_element(By.XPATH, "./ancestor::div[contains(@class, 'disabled')]")
            is_disabled = "disabled" in parent_div.get_attribute("class")
            assert is_disabled, "Max button should be disabled when at max value."
            print("The Max button is correctly disabled.")

            # Test Min Button when value is at max
            min_button = find_element_by_testid(driver, data_testid="close-order-input-volume-static-min")
            assert min_button.is_enabled(), "Min button should be enabled when current value is at max."
            print(f"The Min button is enabled when current value is at max: {current_value}.")
        else:
            # Verify that the current value is within the expected range
            assert False, f"Current value {current_value} not equal to the maximum value {max_value}."
            
        # Step 5: Set the value to the minimum and verify behavior
        min_button = find_element_by_testid(driver, data_testid="close-order-input-volume-static-min")
        click_element(element=min_button)
        current_value = float(input_field.get_attribute("value"))
        print(f"Current Value after setting to Min: {current_value}")

        # Verify Min Button behavior
        min_button = find_element_by_testid(driver, data_testid="close-order-input-volume-static-min")
        if current_value == lot_size:
            parent_div = min_button.find_element(By.XPATH, "./ancestor::div[contains(@class, 'disabled')]")
            is_disabled = "disabled" in parent_div.get_attribute("class")
            assert is_disabled, "Min button should be disabled when at min value."
            print("The Min button is correctly disabled.")

            # Test Max Button when value is at min
            assert max_button.is_enabled(), "Max button should be enabled when current value is at min."
            print(f"The Max button is enabled when current value is at min: {current_value}")
        else:
            assert False, f"Current value {current_value} is not equal to the minimum lot size {lot_size}."

        delay(1)
        
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

def verify_invalid_size_volume_input(driver, trade_type):
    try:
        # Locate the input field for 'size' or 'volume'
        size_input = find_element_by_testid(driver, data_testid=f"{trade_type}-input-volume")

        # Define test cases and expected results
        test_cases = [
            {"name": "negative_value", "input": "-5", "expected": "5", "description": "Negative values should not be accepted."},
            {"name": "non_numeric", "input": "abc", "expected": "", "description": "Non-numeric values should not be accepted."},
            {"name": "more_than_two_decimals", "input": "123.456", "expected": "123.45", "description": "Values with more than two decimals should be truncated."}
        ]

        for case in test_cases:
            # Clear the input field before entering a new value
            clear_input_field(element=size_input)

            # Populate the input field with the test value
            populate_element_with_wait(driver, element=size_input, text=case["input"])

            # Retrieve the value currently in the input field
            entered_value = size_input.get_attribute("value")

            # Assert based on the expected value
            assert entered_value == case["expected"], f"Failed: {case['description']} Input: '{case['input']}' Expected: '{case['expected']}' Got: '{entered_value}'"

            print(f"Test '{case['name']}' passed: {case['description']}")

    except Exception as e:
        # Handle any exceptions that occur during execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""