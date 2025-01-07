import random

from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text
from constants.helper.element import click_element, click_element_with_wait, find_element_by_testid


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / CLOSE - FILL POLICY DROPDOWN TYPE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def fillPolicy_type(driver, trade_type):
    """
    This function selects a fill policy type from the dropdown. It clicks the dropdown,
    chooses one of the available options randomly, and then selects it.

    Arguments:
    - trade_type: The type of trade (e.g., "trade", "edit") to help locate the specific elements.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        
        # Locate and click the fill policy dropdown
        fillPolicy_type = find_element_by_testid(driver, data_testid=f"{trade_type}-dropdown-fill-policy")
        click_element_with_wait(driver, element=fillPolicy_type)
        
        # Define the possible fill policy options
        options = [
            f"{trade_type}-dropdown-fill-policy-fill-or-kill",
            f"{trade_type}-dropdown-fill-policy-immediate-or-cancel"
        ]
        
        # Select a random option from the available options
        selected_option = random.choice(options)
        
        # Locate and click the selected option
        fillPolicy_options = find_element_by_testid(driver, data_testid=selected_option)
        click_element(fillPolicy_options)
        
       # Log the selected fill policy for reference
        attach_text(f"Selected Fill Policy: {selected_option}", name="Fill Policy Selection")

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
