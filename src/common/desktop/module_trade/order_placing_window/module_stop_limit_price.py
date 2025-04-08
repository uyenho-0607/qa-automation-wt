from enums.main import ButtonModuleType
from constants.element_ids import DataTestID

from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element import clear_input_field, find_element_by_testid, javascript_click

from common.desktop.module_trade.order_placing_window.opw_button_action import get_label_one_point_equal

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - STOP LIMIT PRICE FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_stop_limit_price(driver, trade_type: ButtonModuleType):
    """
    Handles the interaction with the Stop Limit Price input field in a trading platform,
    specifically for either creating a new order or editing an existing one.
    
    Arguments:
    - trade_type: The type of trade action, either 'edit' for editing an existing order or
                  other trade types for creating a new one.
    
    Returns:
    - stop_limit_price_element: The WebElement corresponding to the Stop Limit Price input field.
    """
    
    
    # Determine the data-testid based on the button type
    button_testids = {
        ButtonModuleType.TRADE: DataTestID.TRADE_INPUT_STOP_LIMIT_PRICE,
        ButtonModuleType.EDIT: DataTestID.EDIT_INPUT_STOP_LIMIT_PRICE,
    }
    
    button_testid = button_testids.get(trade_type)
    
    # Locate the Stop Limit Price input field based on the trade type (either creating or editing)
    stop_limit_price_element = find_element_by_testid(driver, data_testid=button_testid)
    # If the trade type is "edit", clear the existing value in the input field
    if trade_type == ButtonModuleType.EDIT:
        clear_input_field(stop_limit_price_element) # Clear the field before updating the value
    
    # Return the element representing the input field
    return stop_limit_price_element

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - BUTTON MIN / MAX STOP LIMIT PRICE (+ / - BUTTON)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def btn_min_max_stop_limit_price(driver, trade_type: str, minMax: str, number_of_clicks: int):
    """
    Interacts with the Stop Limit Price's min/max button to increment or decrement the price value.
    It clicks the button a specified number of times and validates the price change after each click.
    
    Arguments:
    - trade_type: The type of trade (e.g., "trade", "edit").
    - minMax: Specifies whether to "increase" or "decrease" the value by clicking the min/max button.
    - number_of_clicks: The number of times to click the min/max button for the operation.
    
    Raises:
    - ValueError: If an invalid `minMax` value is provided.
    - AssertionError: If the value does not increment or decrement by the expected amount.
    """
    try:

        # Locate the min/max button (increase or decrease) based on the trade type and minMax action
        button_min_max = find_element_by_testid(driver, data_testid=f"{trade_type}-input-stop-limit-price-{minMax}")
        javascript_click(driver, element=button_min_max)

        # Locate the input field that holds the stop limit price
        input_field = find_element_by_testid(driver, data_testid=f"{trade_type}-input-stop-limit-price")

        # Get the initial value of the input field. If it's empty, default to 0.0.
        initial_value_str = input_field.get_attribute("value")
        initial_value = float(initial_value_str) if initial_value_str.strip() else 0.0

        # Get the increment value (e.g., 0.01) from the label, which represents one step in the price change
        increment = get_label_one_point_equal(driver, trade_type)

        # Loop for the number of clicks specified
        for i in range(number_of_clicks):
            # Click the min/max button and perform the price change action
            javascript_click(driver, element=button_min_max)

            # Get the updated value after the click and set it to 0.0 if empty
            updated_value_str = input_field.get_attribute("value")
            updated_value = float(updated_value_str) if updated_value_str.strip() else 0.0
            print(f"Stop Limit Price - updated value after click {i+1}: {updated_value}")

            # Check if the value has changed by the expected increment amount
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

            # Log the results for the user
            attach_text(str(number_of_clicks), name=f"{minMax.capitalize()} button clicked {i+1} times")
            attach_text(f"{final_value:.2f}", name=f"Final value: {final_value:.2f}")
            
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""