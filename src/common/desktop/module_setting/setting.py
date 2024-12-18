from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, find_element_by_testid


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SETTING DROPDOWN OPTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_setting(driver, setting_option):
    try:
        
        setting = find_element_by_testid(driver, data_testid="setting-button")
        click_element(setting)
        
        dropdown_option = find_element_by_testid(driver, data_testid=f"setting-option-{setting_option}")
        click_element(dropdown_option)

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""