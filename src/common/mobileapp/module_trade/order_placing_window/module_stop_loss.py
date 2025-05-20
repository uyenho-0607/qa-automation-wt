from enums.main import ButtonModuleType, SLTPOption
from constants.element_ids import DataTestID

from constants.helper.element_android_app import clear_input_field, find_element_by_testid_with_wait

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - STOP LOSS FIELD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Retrieve the Stop Loss (Price / Points) field
def handle_stop_loss(driver, trade_type: ButtonModuleType, sl_type: SLTPOption):
    
    # Define mapping for dropdown and its options
    button_testids = {
        ButtonModuleType.TRADE: {
            SLTPOption.PRICE: DataTestID.TRADE_INPUT_STOPLOSS_PRICE,
            SLTPOption.POINTS: DataTestID.TRADE_INPUT_STOP_LOSS_POINTS,
        },
        ButtonModuleType.EDIT: {
            SLTPOption.PRICE: DataTestID.EDIT_INPUT_STOPLOSS_PRICE,
            SLTPOption.POINTS: DataTestID.EDIT_INPUT_STOP_LOSS_POINTS
        }
    }

    stop_loss_testid = button_testids[trade_type][sl_type]

    # Locate the Take Profit input field
    stop_loss_element = find_element_by_testid_with_wait(driver, data_testid=stop_loss_testid)
    
    # Clear the input field if in edit mode
    if trade_type == ButtonModuleType.EDIT:
        clear_input_field(element=stop_loss_element)
        
    # Return the stop loss element for further actions if required
    return stop_loss_element


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""