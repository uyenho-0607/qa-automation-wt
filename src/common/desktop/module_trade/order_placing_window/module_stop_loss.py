from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, clear_input_field, find_element_by_testid, javascript_click

from common.desktop.module_trade.order_placing_window.opw_button_action import label_onePointEqual
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - STOP LOSS FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_stop_loss(driver, trade_type, sl_type):
    """
    Handles the interaction with the Stop Loss input field in a trading platform.
    This function locates the Stop Loss input field, clears it if the trade is being edited,
    and returns the input element for further interaction.
    
    Arguments:
    - trade_type: The type of trade (e.g., 'trade', 'edit').
    - sl_type: The type of stop loss (e.g., 'price', 'points') that determines which specific input field to locate.
    
    Returns:
    - stop_loss_element: The WebElement corresponding to the Stop Loss input field.
    """
    
    # Locate the Stop Loss input field based on the trade type and stop loss type (sl_type)
    stop_loss_element = find_element_by_testid(driver, data_testid=f"{trade_type}-input-stoploss-{sl_type}")
    
    # If the trade type is "edit", clear the existing value in the input field
    if trade_type == "edit":
        clear_input_field(stop_loss_element) # Clear the field before updating the value
    
    # Return the element representing the input field
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

def btn_min_max_stop_loss(driver, trade_type, type, min_max, number_of_clicks):
    """
    Handles interaction with the Stop Loss min/max button (increase/decrease) for either price or points.
    This function clicks the min/max button a specified number of times, verifies the change in value,
    and ensures the value increments or decrements correctly based on the expected value type (price or points).
    
    Arguments:
    - trade_type: The type of trade (e.g., 'trade', 'edit').
    - type: The type of value being modified ('price' or 'points').
    - minMax: The action to perform, either 'increase' or 'decrease'.
    - number_of_clicks: The number of times to click the min/max button.
    
    Raises:
    - ValueError: If an invalid `type` or `minMax` is provided.
    - AssertionError: If the value does not change as expected after each click.
    """
    try:
        # Locate the min/max button based on trade type, stop loss type, and the action (increase/decrease)
        button_minMax = find_element_by_testid(driver, data_testid=f"{trade_type}-input-stoploss-{type}-{min_max}")
        click_element(button_minMax)

        # Locate the input field where the stop loss value is displayed
        input_field = find_element_by_testid(driver, data_testid=f"{trade_type}-input-stoploss-{type}")

        # Determine the initial value and the increment based on the value type (price or points)
        initial_value_str = input_field.get_attribute("value")
        if type == "price":
            initial_value = float(initial_value_str) if initial_value_str.strip() else 0.0
            increment = label_onePointEqual(driver, trade_type) # Get the increment for price
        elif type == "points":
            initial_value = int(initial_value_str) if initial_value_str.strip() else 0
            increment = 1  # For points, increment is always 1
        else:
            raise ValueError("Invalid value type. Must be 'price' or 'points'.")
        
         # Loop to click the button a specified number of times
        for i in range(number_of_clicks):
            javascript_click(driver, element=button_minMax)

            # Get the updated value based on value_type
            updated_value_str = input_field.get_attribute("value")
            updated_value = float(updated_value_str) if type == "price" else int(updated_value_str)
            print(f"Stop Loss - updated value after click {i+1}: {updated_value}")

            # Check if increment/decrement is as expected
            if min_max == "increase":
                difference = updated_value - initial_value
            elif min_max == "decrease":
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

        # Final check: ensure total increment or decrement matches the expected value
        final_value = float(input_field.get_attribute("value")) if type == "price" else int(input_field.get_attribute("value"))
        expected_value = initial_value + (increment * number_of_clicks) if min_max == "increase" else initial_value - (increment * number_of_clicks)
        
        # Assert if the final value doesn't match the expected value
        assert abs(final_value - expected_value), f"Final value does not match expected value. Expected: {expected_value}, Got: {final_value}"

        # Log the results for the user
        attach_text(str(number_of_clicks), name=f"{min_max.capitalize()} button clicked {i+1} times")
        attach_text(f"{updated_value:.6f}" if type == "price" else str(updated_value), 
                    name=f"Final value: {updated_value:.6f}" if type == "price" else f"Final value: {updated_value}")
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""