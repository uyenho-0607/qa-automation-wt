from constants.helper.driver import delay
from constants.helper.element import click_element, find_element_by_testid, spinner_element, visibility_of_element_by_testid
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - TOGGLE ON / OFF OCT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
        
def toggle_radioButton_OCT(driver, desired_state="unchecked"):
    try:
        
        spinner_element(driver)
        
        # Define both possible 'data-testid' values for the radio button states
        radio_states = {
            "unchecked": "toggle-oct",
            "checked": "toggle-oct-checked"
        }

        # Identify the current state of the radio button (checked/unchecked)
        current_state = None
        for state, testid in radio_states.items():
            try:
                
                oct_button = visibility_of_element_by_testid(driver, testid)
                current_state = state
                attach_text(f"Radio button is currently in the '{state}' state.", name="Button Current Status")

                # If the current state matches the desired state, no action is needed
                if state == desired_state:
                    return

                # Perform the toggle to the desired state
                attach_text(f"Toggling to '{desired_state}' as desired.", name="Toggle Button Status")
                click_element(oct_button)

                # Confirm the action if needed
                if desired_state == "checked":
                    oct_confirm = visibility_of_element_by_testid(driver, data_testid="oct-modal-button-confirm")
                    click_element(oct_confirm)
                return
            
            except Exception:
                # If the element is not found, continue checking the other state
                continue

        # If no valid state is found
        if current_state is None:
            raise Exception("Unable to determine the current state of the radio button.")

        delay(0.5)
    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""