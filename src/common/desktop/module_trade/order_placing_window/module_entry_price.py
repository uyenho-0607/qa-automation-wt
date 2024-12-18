from common.desktop.module_trade.order_placing_window.opw_button_action import label_onePointEqual
from constants.helper.element import clear_input_field, find_element_by_testid, javascript_click
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - ENTRY PRICE FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_entryPrice(driver, trade_type):
    entryPrice_element = find_element_by_testid(driver, data_testid=f"{trade_type}-input-price")
    if trade_type == "edit":
        clear_input_field(entryPrice_element)
    # Return both the element and the value
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
        
        # Locate the min/max button
        button_minMax = find_element_by_testid(driver, data_testid=f"{trade_type}-input-price-{minMax}")
        javascript_click(driver, element=button_minMax)

        # Locate the input field where the price is displayed
        input_field = find_element_by_testid(driver, data_testid=f"{trade_type}-input-price")

        # Get the initial value of the input field, set to 0.0 if empty
        initial_value_str = input_field.get_attribute("value")
        initial_value = float(initial_value_str) if initial_value_str.strip() else 0.0

        # Get the increment (one point equal to a specific value, like 0.01)
        increment = label_onePointEqual(driver, trade_type)

        for i in range(number_of_clicks):
            javascript_click(driver, element=button_minMax)

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
            
            assert abs(final_value - expected_value), f"Final value does not match expected value. Expected: {expected_value:.2f}, Got: {final_value:.2f}"

            attach_text(str(number_of_clicks), name=f"{minMax.capitalize()} button clicked {i+1} times")
            attach_text(f"{final_value}", name=f"Final value: {final_value}")
            
    except Exception as e:
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""