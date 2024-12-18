from constants.helper.element import click_element, find_element_by_xpath
from constants.helper.error_handler import handle_exception



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SETTING DROPDOWN OPTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_setting(driver):
    try:
        
        # setting = find_element_by_testid(driver, data_testid="setting-button")
        setting = find_element_by_xpath(driver, "(//div[@class='css-1rynq56 r-lrvibr r-1loqt21'])[2]")
        click_element(setting)
        
        # dropdown_option = find_element_by_testid(driver, data_testid=f"setting-option-{setting_option}")
        # click_element(dropdown_option)
        
        dropdown_option = find_element_by_xpath(driver, "//div[@class='css-1rynq56 r-15bfait r-1bns8cd r-majxgm']")
        click_element(dropdown_option)

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

