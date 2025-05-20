from constants.element_ids import DataTestID

from constants.helper.driver import delay
from constants.helper.element_android_app import clear_input_field, find_element_by_testid_with_wait

from enums.main import ButtonModuleType


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - LOCATE THE ENTRY PRICE FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_entry_price(driver, trade_type: ButtonModuleType):
    
    delay(0.5)
    
    # Define both possible 'data-testid' values for the radio button states
    trade_type_mappings = {
        ButtonModuleType.TRADE: DataTestID.TRADE_INPUT_PRICE,
        ButtonModuleType.EDIT: DataTestID.EDIT_INPUT_PRICE
    }
    
    entry_price = trade_type_mappings.get(trade_type)    
    
    # Find the entry price input field based on the trade type (e.g., 'trade' or 'edit')
    entry_price_element = find_element_by_testid_with_wait(driver, data_testid=entry_price)
    
    # If the trade type is 'edit', clear the input field before proceeding
    if trade_type == ButtonModuleType.EDIT:
        clear_input_field(element=entry_price_element)
        
    # Return the entry price element for further use
    return entry_price_element
    
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""