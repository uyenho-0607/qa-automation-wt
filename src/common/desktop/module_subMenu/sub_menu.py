from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element_with_wait, visibility_of_element_by_testid


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                MENU SELECTION (TRADE / MARKET / ASSET / SIGNAL / CALENDAR / NEWS)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# menu button (Trade / Market / Asset / Signal / Calendar / News
def menu_button(driver, menu):
    try:
       
        menu_selection = visibility_of_element_by_testid(driver, data_testid=f"side-bar-option-{menu}")
        click_element_with_wait(driver, element=menu_selection)
        
    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""