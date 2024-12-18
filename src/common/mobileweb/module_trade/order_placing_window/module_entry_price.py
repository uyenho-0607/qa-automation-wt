from constants.helper.element import click_element, clear_input_field, find_element_by_testid, populate_element_with_wait, javascript_click, visibility_of_element_by_testid
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text

from common.mobileweb.module_trade.order_placing_window.opw_button_action import label_onePointEqual


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - LOCATE THE ENTRY PRICE FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_entryPrice(driver, trade_type):
    # Find the entry price input field based on the trade type (e.g., 'edit', 'new')
    entryPrice_element = visibility_of_element_by_testid(driver, data_testid=f"{trade_type}-input-price")
    
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
        button_minMax = visibility_of_element_by_testid(driver, data_testid=f"{trade_type}-input-price-{minMax}")
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
            attach_text(str(number_of_clicks), name=f"{minMax.capitalize()} button clicked {i+1} times")
            attach_text(f"{final_value}", name=f"Final value: {final_value}")
            
    except Exception as e:
        handle_exception(driver, e)
        
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
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""