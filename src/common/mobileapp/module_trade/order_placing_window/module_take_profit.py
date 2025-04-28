from enums.main import ButtonModuleType, SLTPOption
from constants.element_ids import DataTestID

from constants.helper.element_android_app import clear_input_field, find_element_by_testid_with_wait



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - TAKE PROFIT FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Retrieve the Take Profit (Price / Points) field
def handle_take_profit(driver, trade_type: ButtonModuleType, tp_type: SLTPOption):
    
    # Define mapping for dropdown and its options
    button_testids = {
        ButtonModuleType.TRADE: {
            SLTPOption.PRICE: DataTestID.TRADE_INPUT_TAKEPROFIT_PRICE,
            SLTPOption.POINTS: DataTestID.TRADE_INPUT_TAKE_PROFIT_POINTS,
        },
        ButtonModuleType.EDIT: {
            SLTPOption.PRICE: DataTestID.EDIT_INPUT_TAKEPROFIT_PRICE,
            SLTPOption.POINTS: DataTestID.EDIT_INPUT_TAKE_PROFIT_POINTS
        }
    }
    
    take_profit_testid = button_testids[trade_type][tp_type]

    # Locate the Take Profit input field
    take_profit_element = find_element_by_testid_with_wait(driver, data_testid=take_profit_testid)
    
    # Clear the input field if in edit mode
    if trade_type == ButtonModuleType.EDIT:
        clear_input_field(element=take_profit_element)
        
    # Return the take-profit element for further actions if required
    return take_profit_element

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""