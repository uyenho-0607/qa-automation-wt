from constants.helper.driver import delay
from constants.helper.element import click_element, find_element_by_testid, visibility_of_element_by_testid
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - TOGGLE ON / OFF OCT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def toggle_radioButton_OCT(driver, desired_state: str ="unchecked"):
    """
    This function toggles a radio button to the desired state, either 'checked' or 'unchecked'.
    It checks the current state of the button and performs the necessary click if needed.
    
    Arguments:
    - driver (WebDriver): The Selenium WebDriver instance.
    - desired_state (str): The state to toggle the radio button to. Can be 'checked' or 'unchecked'. Default is 'unchecked'.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Define the 'data-testid' values for both states
        radio_states = {
            "unchecked": "toggle-oct",
            "checked": "toggle-oct-checked"
        }

        # Identify the current state of the radio button (checked/unchecked)
        current_state = None
        
        for state, testid in radio_states.items():
            try:
                radiobtn = find_element_by_testid(driver, testid)
                current_state = state
                attach_text(f"Radio button is currently in the '{state}' state.", name="Button Current Status")

                # If the current state matches the desired state, no action is needed
                if state == desired_state:
                    return

                # Perform the toggle to the desired state
                attach_text(f"Toggling to '{desired_state}' as desired.", name="Toggle Button Status")
                click_element(radiobtn)
                
                # If toggling to 'checked', confirm the action in the modal
                if desired_state == "checked":
                    # Wait for the confirmation modal to appear and click it
                    oct_confirm = visibility_of_element_by_testid(driver, data_testid="oct-modal-button-confirm")
                    click_element(oct_confirm)
                    delay(0.5) # Small delay for stability
                return # Exit after toggling to the desired state
            
            except Exception:
                # If the element is not found, continue checking the other state
                continue

        # If no valid state is found
        if current_state is None:
            raise Exception("Unable to determine the current state of the radio button.")
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
