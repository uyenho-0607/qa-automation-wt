import random
from constants.helper.driver import delay
from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, find_visible_element_by_testid, find_element_by_xpath

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE - TOGGLE ON / OFF OCT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_radioStates():
    return {
        "OCT": {
            "unchecked": "//*[@data-testid='toggle-oct']",
            "checked": "//*[@data-testid='toggle-oct-checked']"
        },
        "Margin_Call": {
            "unchecked": "(//div[@class='sc-sdaxep-3 fKaFfa'])[1]//div[@data-testid='toggle-oct']",
            # "checked": "(//div[@class='sc-sdaxep-3 fKaFfa'])[1]//div[@data-testid='toggle-oct-checked']"
            "checked": "(//*[@data-testid='notification-settings-toggle-checked'])[1]"
        },
        "Margin_Stop": {
            # "unchecked": "(//div[@class='sc-sdaxep-3 fKaFfa'])[2]//div[@data-testid='toggle-oct']",
            # "checked": "(//div[@class='sc-sdaxep-3 fKaFfa'])[2]//div[@data-testid='toggle-oct-checked']"
            "unchecked": "//div[@data-testid='notification-settings-toggle-']",
            "checked": "(//*[@data-testid='notification-settings-toggle-checked'])[2]"
        },
        "Signal": {
            # "unchecked": "(//div[@class='sc-sdaxep-3 fKaFfa'])[3]//div[@data-testid='toggle-oct']",
            # "checked": "(//div[@class='sc-sdaxep-3 fKaFfa'])[3]//div[@data-testid='toggle-oct-checked']"
            "unchecked": "//div[@data-testid='notification-settings-toggle-']",
            "checked": "(//*[@data-testid='notification-settings-toggle-checked'])[3]"
        },
        "Linked_Devices": {
            # "unchecked": "(//div[@class='sc-sdaxep-3 fKaFfa'])[4]//div[@data-testid='toggle-oct']",
            # "checked": "(//div[@class='sc-sdaxep-3 fKaFfa'])[4]//div[@data-testid='toggle-oct-checked']"
            "unchecked": "//div[@data-testid='notification-settings-toggle-']",
            "checked": "(//*[@data-testid='notification-settings-toggle-checked'])[1]"
        }
    }
    

def handle_close_popup(driver, category):
    """Handles closing the popup modal if necessary."""
    if category != "OCT":
        btn_close = find_element_by_xpath(driver, "//div[@class='sc-ur24yu-4 jgnDww']//*[name()='svg']")
        click_element(btn_close)
        
        
    
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
                attach_text(f"Radio button ({category}) is currently in the '{state}' state. No action needed.", name="Button Current Status")

                # If the current state matches the desired state, no action needed
                if state == desired_state:
                    handle_close_popup(driver, category)
                    return desired_state  # Return the final state

                # Toggle the radio button
                attach_text(f"Toggling '{category}' button to '{desired_state}'", name="Toggle Button Status")
                click_element(radiobtn)
                
                # Only apply confirmation modal if category is 'OCT' and desired state is 'checked'
                if category == "OCT" and desired_state == "checked":
                    oct_confirm = find_visible_element_by_testid(driver, data_testid="oct-modal-button-confirm")
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


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""