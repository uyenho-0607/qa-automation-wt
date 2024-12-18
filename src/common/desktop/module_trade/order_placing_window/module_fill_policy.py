import random
import traceback

from constants.helper.element import click_element, click_element_with_wait, find_element_by_testid
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import take_screenshot


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / CLOSE - FILL POLICY DROPDOWN TYPE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def fillPolicy_type(driver, trade_type):
    try:
        
        # Click on the Fill Policy
        fillPolicy_type = find_element_by_testid(driver, data_testid=f"{trade_type}-dropdown-fill-policy")
        click_element_with_wait(driver, element=fillPolicy_type)
        
        # Define the two possible options
        options = [
            f"{trade_type}-dropdown-fill-policy-fill-or-kill",
            f"{trade_type}-dropdown-fill-policy-immediate-or-cancel"
        ]
        
        # Select a random option
        selected_option = random.choice(options)
        
        # Find and click the selected option
        fillPolicy_options = find_element_by_testid(driver, data_testid=selected_option)
        click_element(fillPolicy_options)

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
