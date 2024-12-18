from constants.helper.element import click_element, clear_input_field, find_element_by_testid, populate_element_with_wait
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text

from common.mobileweb.module_trade.order_placing_window.opw_button_action import label_onePointEqual


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
            attach_text(str(number_of_clicks), name=f"{minMax.capitalize()} button clicked {i+1} times")
            attach_text(f"{final_value:.2f}", name=f"Final value: {final_value:.2f}")
            
    except Exception as e:
        handle_exception(driver, e)

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
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
