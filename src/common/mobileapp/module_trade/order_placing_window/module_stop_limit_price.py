from enums.main import ButtonModuleType
from constants.element_ids import DataTestID

from constants.helper.driver import delay
from constants.helper.element_android_app import clear_input_field, find_element_by_testid_with_wait


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - STOP LIMIT PRICE FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def handle_stop_limit_price(driver, trade_type: ButtonModuleType):
    
    delay(0.5)
    
    # Define both possible 'data-testid' values for the radio button states
    trade_type_mappings = {
        ButtonModuleType.TRADE: DataTestID.TRADE_INPUT_STOP_LIMIT_PRICE,
        ButtonModuleType.EDIT: DataTestID.EDIT_INPUT_STOP_LIMIT_PRICE
    }
    
    button_testid = trade_type_mappings.get(trade_type)
    
    # Find the entry price input field based on the trade type (e.g., 'trade' or 'edit')
    stop_limit_price_element = find_element_by_testid_with_wait(driver, data_testid=button_testid)
    
    # If the trade type is 'edit', clear the input field before proceeding
    if trade_type == ButtonModuleType.EDIT:
        clear_input_field(element=stop_limit_price_element)
        
    # Return the entry price element for further use
    return stop_limit_price_element



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""