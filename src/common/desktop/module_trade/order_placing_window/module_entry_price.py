from enums.main import ButtonModuleType
from constants.element_ids import DataTestID

from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element import clear_input_field, find_element_by_testid, javascript_click

from common.desktop.module_trade.order_placing_window.opw_button_action import get_label_one_point_equal


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - ENTRY PRICE FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_entry_price(driver, trade_type: ButtonModuleType):
    """
    This function handles the entry price input for a trade form. Depending on the trade type, 
    it either retrieves the price input field or clears it (for "edit" trades).

    Arguments:
    - trade_type: The type of trade (e.g., "trade", "edit").

    Returns:
    - entry_price_element (WebElement): The Selenium WebElement representing the entry price input field.
    """
        
    # Determine the data-testid based on the button type
    button_testids = {
        ButtonModuleType.TRADE: DataTestID.TRADE_INPUT_PRICE,
        ButtonModuleType.EDIT: DataTestID.EDIT_INPUT_PRICE,
    }
    
    button_testid = button_testids.get(trade_type)

    # Locate the entry price input field using its test ID attribute
    entry_price_element = find_element_by_testid(driver, data_testid=button_testid)
    
    # Clear the input field if in edit mode
    if trade_type == ButtonModuleType.EDIT:
        clear_input_field(element=entry_price_element)
        
    # Return the element for further actions if required
    return entry_price_element
    
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - BUTTON MIN / MAX ENTRY PRICE (+ / - BUTTON)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def btn_min_max_price(driver, trade_type, min_max, number_of_clicks):
    """
    This function interacts with a 'min' or 'max' button (depending on the trade type and action) 
    to adjust the price. It performs the specified number of clicks and verifies that the price changes
    according to the expected increment or decrement.

    Arguments:
    - trade_type (str): The type of trade (e.g., "create", "edit").
    - min_max (str): Determines whether to increase or decrease the price. Expected values: "increase" or "decrease".
    - number_of_clicks (int): The number of times the button should be clicked to adjust the price.

    Raises:
    - ValueError: If the `min_max` value is not "increase" or "decrease".
    - AssertionError: If the increment or decrement does not match the expected value.
    """
    try:
        
        # Locate the min/max button based on the trade type and action ('increase' or 'decrease')
        button_min_max = find_element_by_testid(driver, data_testid=f"{trade_type}-input-price-{min_max}")
        # Simulate a click on the button using JavaScript
        javascript_click(driver, element=button_min_max)

        # Locate the input field where the price is displayed
        input_field = find_element_by_testid(driver, data_testid=f"{trade_type}-input-price")

        # Get the initial value of the price input field, default to 0.0 if empty
        initial_value_str = input_field.get_attribute("value")
        initial_value = float(initial_value_str) if initial_value_str.strip() else 0.0

        # Get the price increment value (one point equal to a specific value, like 0.01)
        increment = get_label_one_point_equal(driver, trade_type)

        # Loop through the specified number of clicks
        for i in range(number_of_clicks):
            # Click the button to increase or decrease the price
            javascript_click(driver, element=button_min_max)

            # Get the updated value after the click and set it to 0.0 if empty
            updated_value_str = input_field.get_attribute("value")
            updated_value = float(updated_value_str) if updated_value_str.strip() else 0.0
            
            # Verify that the increment or decrement is correct
            if min_max == "increase":
                # Check if the value increased by the expected increment
                difference = updated_value - initial_value
                assert abs(difference - increment) < 1e-6, f"Value did not increment by {increment} after click {i+1}. Difference: {difference:.6f}"
            elif min_max == "decrease":
                # Check if the value increased by the expected increment
                difference = initial_value - updated_value
                assert abs(difference - increment) < 1e-6, f"Value did not decrement by {increment} after click {i+1}. Difference: {difference:.6f}"
            else:
                # Raise an error if an invalid value for 'min_max' is provided
                raise ValueError("Invalid value for min_max. Must be 'increase' or 'decrease'.")

            # Update initial_value for the next iteration to the current updated value
            initial_value = updated_value

            # Final check: ensure the total increment or decrement matches the expected value
            final_value = float(input_field.get_attribute("value"))
            expected_value = initial_value + (increment * number_of_clicks) if min_max == "increase" else initial_value - (increment * number_of_clicks)
            
            # Assert if the final value doesn't match the expected value
            assert abs(final_value - expected_value), f"Final value does not match expected value. Expected: {expected_value:.2f}, Got: {final_value:.2f}"

            # Log the results for the user
            attach_text(str(number_of_clicks), name=f"{min_max.capitalize()} button clicked {i+1} times")
            attach_text(f"{final_value}", name=f"Final value: {final_value}")
            
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""