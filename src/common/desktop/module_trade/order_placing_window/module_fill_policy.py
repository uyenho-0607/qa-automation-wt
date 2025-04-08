import random

from enums.main import ButtonModuleType
from constants.element_ids import DataTestID

from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, find_element_by_testid


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / CLOSE - FILL POLICY DROPDOWN TYPE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def fill_policy_type(driver, trade_type: ButtonModuleType):
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
        if trade_type not in fill_policy_map:
            raise ValueError(f"Invalid button type: {trade_type}")
        
        policy_data = fill_policy_map[trade_type]

        # Click on the Fill Policy dropdown
        dropdown_element = find_element_by_testid(driver, data_testid=policy_data["dropdown"])
        click_element(element=dropdown_element)

        # Select and click a random option
        selected_option = random.choice(policy_data["options"])
        option_element = find_element_by_testid(driver, data_testid=selected_option)
        click_element(element=option_element)

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""