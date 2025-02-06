import random
from constants.helper.driver import delay
from constants.helper.element import click_element, find_element_by_testid, visibility_of_element_by_testid, find_element_by_xpath
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

        # Randomly select a state if 'random' is chosen
        if desired_state == "random":
            desired_state = random.choice(list(radio_states.keys()))
            attach_text(f"Randomly selected state: {desired_state}", name="Random Selection Status")

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


def get_radioStates():
    return {
        "OCT": {
            "unchecked": "//div[@data-testid='toggle-oct']",
            "checked": "//div[@data-testid='toggle-oct-checked']"
        },
        "Margin_Call": {
            "unchecked": "(//div[@class='sc-sdaxep-3 fKaFfa'])[1]//div[@data-testid='toggle-oct']",
            "checked": "(//div[@class='sc-sdaxep-3 fKaFfa'])[1]//div[@data-testid='toggle-oct-checked']"
        },
        "Margin_Stop": {
            "unchecked": "(//div[@class='sc-sdaxep-3 fKaFfa'])[2]//div[@data-testid='toggle-oct']",
            "checked": "(//div[@class='sc-sdaxep-3 fKaFfa'])[2]//div[@data-testid='toggle-oct-checked']"
        },
        "Signal": {
            "unchecked": "(//div[@class='sc-sdaxep-3 fKaFfa'])[3]//div[@data-testid='toggle-oct']",
            "checked": "(//div[@class='sc-sdaxep-3 fKaFfa'])[3]//div[@data-testid='toggle-oct-checked']"
        },
        "Linked_Devices": {
            "unchecked": "(//div[@class='sc-sdaxep-3 fKaFfa'])[4]//div[@data-testid='toggle-oct']",
            "checked": "(//div[@class='sc-sdaxep-3 fKaFfa'])[4]//div[@data-testid='toggle-oct-checked']"
        }
    }
    

def handle_close_popup(driver, category):
    """Handles closing the popup modal if necessary."""
    if category != "OCT":
        close_btn = find_element_by_xpath(driver, "//div[@class='sc-ur24yu-4 jgnDww']//*[name()='svg']")
        click_element(close_btn)
        
        
    
def toggle_radioButton(driver, category: str, desired_state: str):
    """
    Toggles a radio button within a specific category to the desired state ('checked' or 'unchecked').

    Arguments:
    - driver (WebDriver): The Selenium WebDriver instance.
    - category (str): The category of the radio button (e.g., 'OCT', 'Signal').
    - desired_state (str): The state to toggle the radio button to. Can be 'checked' or 'unchecked'. Default is 'unchecked'.

    Returns:
    - str: The final state of the radio button ('checked' or 'unchecked').

    Raises:
    - Exception: If the category is invalid or the radio button state cannot be determined.
    """
    try:
        radio_states = get_radioStates()

        # Validate category
        if category not in radio_states:
            raise ValueError(f"Invalid category '{category}'. Valid options: {list(radio_states.keys())}")

        # Random selection if 'random' is chosen
        if desired_state == "random":
            desired_state = random.choice(list(radio_states[category].keys()))
            attach_text(f"Randomly selected state: {desired_state}", name="Random Selection Status")

        # Identify the current state of the radio button
        current_state = None
        for state, testid in radio_states[category].items():
            try:
                radiobtn = find_element_by_xpath(driver, testid)
                current_state = state
                attach_text(f"Radio button ({category}) is currently in the '{state}' state.", name="Button Current Status")

                # If the current state matches the desired state, no action needed
                if state == desired_state:
                    print(f"Radio button '{category}' is already in the '{desired_state}' state. No action needed.")
                    handle_close_popup(driver, category)
                    return desired_state  # Return the final state

                # Toggle the radio button
                attach_text(f"Toggling '{category}' button to '{desired_state}'", name="Toggle Button Status")
                click_element(radiobtn)
                
                # Only apply confirmation modal if category is 'OCT' and desired state is 'checked'
                if category == "OCT" and desired_state == "checked":
                    oct_confirm = visibility_of_element_by_testid(driver, data_testid="oct-modal-button-confirm")
                    click_element(oct_confirm)
                    delay(0.5)  # Small delay for stability
                    return desired_state  # Return the final state

                handle_close_popup(driver, category)

            except Exception:
                # Continue checking the next state if the element is not found
                continue

        # If no valid state is found
        if current_state is None:
            raise Exception(f"Unable to determine the current state of the '{category}' radio button.")

        return desired_state  # Return the final state after execution

    except Exception as e:
        handle_exception(driver, e)
        return None  # Return None in case of an exception
