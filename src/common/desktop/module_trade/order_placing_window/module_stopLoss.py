from common.desktop.module_trade.order_placing_window.opw_button_action import label_onePointEqual
from constants.helper.element import click_element, clear_input_field, find_element_by_testid, javascript_click
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - STOP LOSS FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_stopLoss(driver, trade_type, sl_type):
    stopLoss_element = find_element_by_testid(driver, data_testid=f"{trade_type}-input-stoploss-{sl_type}")
    if trade_type == "edit":
        clear_input_field(stopLoss_element)
    return stopLoss_element

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - BUTTON MIN / MAX STOP LOSS (+ / - BUTTON)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def btn_minMax_stopLoss(driver, trade_type, type, minMax, number_of_clicks):
    try:
        button_minMax = find_element_by_testid(driver, data_testid=f"{trade_type}-input-stoploss-{type}-{minMax}")
        click_element(button_minMax)

        input_field = find_element_by_testid(driver, data_testid=f"{trade_type}-input-stoploss-{type}")

        # Determine the initial value based on value_type (either float or int)
        initial_value_str = input_field.get_attribute("value")
        if type == "price":
            initial_value = float(initial_value_str) if initial_value_str.strip() else 0.0
            increment = label_onePointEqual(driver, trade_type)
        elif type == "points":
            initial_value = int(initial_value_str) if initial_value_str.strip() else 0
            increment = 1
        else:
            raise ValueError("Invalid value type. Must be 'price' or 'points'.")

        for i in range(number_of_clicks):
            javascript_click(driver, element=button_minMax)

            # Get the updated value based on value_type
            updated_value_str = input_field.get_attribute("value")
            updated_value = float(updated_value_str) if type == "price" else int(updated_value_str)
            print(f"Stop Loss - updated value after click {i+1}: {updated_value}")

            # Check if increment/decrement is as expected
            if minMax == "increase":
                difference = updated_value - initial_value
            elif minMax == "decrease":
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

            attach_text(str(number_of_clicks), name=f"{minMax.capitalize()} button clicked {i+1} times")
            attach_text(f"{updated_value:.6f}" if type == "price" else str(updated_value), 
                        name=f"Final value: {updated_value:.6f}" if type == "price" else f"Final value: {updated_value}")
            
        # Final check: ensure total increment or decrement matches the expected value
        final_value = float(input_field.get_attribute("value")) if type == "price" else int(input_field.get_attribute("value"))
        expected_value = initial_value + (increment * number_of_clicks) if minMax == "increase" else initial_value - (increment * number_of_clicks)
        
        assert abs(final_value - expected_value), f"Final value does not match expected value. Expected: {expected_value}, Got: {final_value}"

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def btn_minMax_stopLoss777(driver, trade_type, type, minMax, number_of_clicks):
    try:
        button_minMax = find_element_by_testid(driver, data_testid=f"{trade_type}-input-stoploss-{type}-{minMax}")
        click_element(button_minMax)

        input_field = find_element_by_testid(driver, data_testid=f"{trade_type}-input-stoploss-{type}")

        # Determine the initial value based on value_type (either float or int)
        initial_value_str = input_field.get_attribute("value")
        if type == "price":
            initial_value = float(initial_value_str) if initial_value_str.strip() else 0.0
            increment = label_onePointEqual(driver, trade_type)
        elif type == "points":
            initial_value = int(initial_value_str) if initial_value_str.strip() else 0
            increment = 1
        else:
            raise ValueError("Invalid value type. Must be 'price' or 'points'.")

        for i in range(number_of_clicks):
            javascript_click(driver, element=button_minMax)

            # Track the current price (for price type only)
            current_price_str = find_element_by_testid(driver, data_testid=f"{trade_type}-input-price").get_attribute("value")
            current_price = float(current_price_str) if current_price_str.strip() else 0.0
            
            # Get the updated stop loss value
            updated_value_str = input_field.get_attribute("value")
            updated_value = float(updated_value_str) if type == "price" else int(updated_value_str)
            print(f"Updated value after click {i+1}: {updated_value} (Current price: {current_price})")

            # Calculate the difference between the updated stop loss value and the current price
            if minMax == "increase":
                difference = updated_value - initial_value
            elif minMax == "decrease":
                difference = initial_value - updated_value
            else:
                raise ValueError("Invalid value for minMax. Must be 'increase' or 'decrease'.")

            # Ensure that the stop loss is incremented/decremented correctly based on the actual price movement
            if type == "price":
                # Check that the stop loss change aligns with the price jump
                expected_difference = (current_price - initial_value) if minMax == "increase" else (initial_value - current_price)
                assert abs(difference - expected_difference) < 1e-6, f"Value did not change by {expected_difference} after click {i+1}. Difference: {difference:.6f} (Current price: {current_price})"
            else:  # for "points"
                assert abs(difference - increment) == 0, f"Value did not change by {increment} after click {i+1}. Difference: {difference}"

            # Update initial_value for next iteration
            initial_value = updated_value

            attach_text(str(number_of_clicks), name=f"{minMax.capitalize()} button clicked {i+1} times")
            attach_text(f"{updated_value:.6f}" if type == "price" else str(updated_value), 
                        name=f"Final value: {updated_value:.6f}" if type == "price" else f"Final value: {updated_value}")

        # Final check: ensure total increment or decrement matches the expected value
        final_value = float(input_field.get_attribute("value")) if type == "price" else int(input_field.get_attribute("value"))
        expected_value = initial_value + (increment * number_of_clicks) if minMax == "increase" else initial_value - (increment * number_of_clicks)

        assert abs(final_value - expected_value), f"Final value does not match expected value. Expected: {expected_value}, Got: {final_value}"

    except Exception as e:
        handle_exception(driver, e)
