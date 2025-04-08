from enums.main import ButtonModuleType, SLTPOption
from constants.element_ids import DataTestID

from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element_android_app import click_element, clear_input_field, find_element_by_testid, find_element_by_testid_with_wait, populate_element_with_wait, find_visible_element_by_testid

from common.mobileapp.module_trade.order_placing_window.opw_button_action import get_label_one_point_equal


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - TAKE PROFIT FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Retrieve the Take Profit (Price / Points) field
def handle_take_profit(driver, trade_type: ButtonModuleType, tp_type: SLTPOption):
    
    # Define mapping for dropdown and its options
    button_testids = {
        ButtonModuleType.TRADE: {
            SLTPOption.PRICE: DataTestID.TRADE_INPUT_TAKEPROFIT_PRICE,
            SLTPOption.POINTS: DataTestID.TRADE_INPUT_TAKE_PROFIT_POINTS,
        },
        ButtonModuleType.EDIT: {
            SLTPOption.PRICE: DataTestID.EDIT_INPUT_TAKEPROFIT_PRICE,
            SLTPOption.POINTS: DataTestID.EDIT_INPUT_TAKE_PROFIT_POINTS
        }
    }
    
    take_profit_testid = button_testids[trade_type][tp_type]

    # Locate the Take Profit input field
    takeProfit_element = find_element_by_testid_with_wait(driver, data_testid=take_profit_testid)
    
    # Clear the input field if in edit mode
    if trade_type == ButtonModuleType.EDIT:
        clear_input_field(element=takeProfit_element)
        
    # Return the take-profit element for further actions if required
    return takeProfit_element

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - BUTTON MIN / MAX TAKE PROFIT (+ / - BUTTON)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def btn_minMax_takeProfit(driver, trade_type, type, minMax, number_of_clicks):
    try:
        # Locate and click the min/max button
        button_min_max = find_visible_element_by_testid(driver, data_testid=f"{trade_type}-input-takeprofit-{type}-{minMax}")
        click_element(button_min_max)

        # Locate the input field and determine the initial value and increment
        input_field = find_element_by_testid(driver, data_testid=f"{trade_type}-input-takeprofit-{type}")

        # Determine the initial value based on value_type (either float or int)
        initial_value_str = input_field.get_attribute("value")
        
        if type == "price":
            # Convert input value to float, default to 0.0 if empty
            initial_value = float(initial_value_str) if initial_value_str.strip() else 0.0
            
            # Retrieve the increment value for price
            increment = get_label_one_point_equal(driver, trade_type)
        elif type == "points":
            # Convert input value to int, default to 0 if empty
            initial_value = int(initial_value_str) if initial_value_str.strip() else 0
            
            # Set increment for points to 1
            increment = 1
        else:
            raise ValueError("Invalid value type. Must be 'price' or 'points'.")

        for i in range(number_of_clicks):
            click_element(button_min_max)

            # Get the updated value based on value_type
            updated_value_str = input_field.get_attribute("value")
            updated_value = float(updated_value_str) if type == "price" else int(updated_value_str)

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

            # Attach text logs for the clicks and final value for reporting
            attach_text(str(number_of_clicks), name=f"{minMax.capitalize()} button clicked {i+1} times")
            attach_text(f"{updated_value:.6f}" if type == "price" else str(updated_value), 
                        name=f"Final value: {updated_value:.6f}" if type == "price" else f"Final value: {updated_value}")

        # Final check: ensure total increment or decrement matches the expected value
        final_value = float(input_field.get_attribute("value")) if type == "price" else int(input_field.get_attribute("value"))
        expected_value = initial_value + (increment * number_of_clicks) if minMax == "increase" else initial_value - (increment * number_of_clicks)
        
        # Final check: ensure total increment or decrement matches the expected value
        assert abs(final_value - expected_value), f"Final value does not match expected value. Expected: {expected_value}, Got: {final_value}"

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - INPUT / CLEAR THE TAKE PROFIT FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def manage_takeProfit(driver, trade_type, type, takeProfit_field=None):

    # Remove the trailing ".0" if it exists
    if takeProfit_field.endswith(".0"):
        takeProfit_field = takeProfit_field[:-2]
    
    try:
        # Locate the input field for take profit
        take_profit_input = find_element_by_testid(driver, data_testid=f"{trade_type}-input-takeprofit-{type}")

        # Clear the field if editing
        if trade_type == 'edit':
            clear_input_field(take_profit_input)
            
        # Populate the field with the provided stop loss value
        populate_element_with_wait(driver, element=take_profit_input, text=takeProfit_field)
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
     
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
