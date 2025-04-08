import random

from enums.main import ButtonModuleType
from constants.element_ids import DataTestID

from constants.helper.error_handler import handle_exception
from constants.helper.element_android_app import click_element, find_element_by_testid_with_wait


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / CLOSE - FILL POLICY DROPDOWN TYPE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def fill_policy_type(driver, fill_policy: ButtonModuleType):
    try:
        # Define mapping for dropdown and its options
        fill_policy_map = {
            ButtonModuleType.TRADE: {
                "dropdown": DataTestID.TRADE_DROPDOWN_FILL_POLICY,
                "options": [
                    DataTestID.TRADE_DROPDOWN_FILL_POLICY_FILL_OR_KILL,
                    DataTestID.TRADE_DROPDOWN_FILL_POLICY_IMMEDIATE_OR_CANCEL
                ]
            },
            ButtonModuleType.CLOSE: {
                "dropdown": DataTestID.CLOSE_ORDER_DROPDOWN_FILL_POLICY,
                "options": [
                    DataTestID.CLOSE_ORDER_DROPDOWN_FILL_POLICY_FILL_OR_KILL,
                    DataTestID.CLOSE_ORDER_DROPDOWN_FILL_POLICY_IMMEDIATE_OR_CANCEL
                ]
            }
        }

        # Validate button type and get corresponding data
        if fill_policy not in fill_policy_map:
            raise ValueError(f"Invalid button type: {fill_policy}")
        
        policy_data = fill_policy_map[fill_policy]

        # Click on the Fill Policy dropdown
        dropdown_element = find_element_by_testid_with_wait(driver, data_testid=policy_data["dropdown"])
        click_element(dropdown_element)

        # Select and click a random option
        selected_option = random.choice(policy_data["options"])
        option_element = find_element_by_testid_with_wait(driver, data_testid=selected_option)
        click_element(option_element)

    except Exception as e:
        handle_exception(driver, e)
        
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


