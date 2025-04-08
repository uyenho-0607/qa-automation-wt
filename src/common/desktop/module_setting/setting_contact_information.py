from enums.main import Setting

from constants.helper.error_handler import handle_exception
from constants.helper.element import find_element_by_xpath, click_element, invisibility_of_element_by_testid

from common.desktop.module_setting.setting_general import button_setting


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NOTIFICATION SETTING MODAL - LINKED DEVICES
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def contact_information(driver):
    try:
        
        button_setting(driver, setting_option=Setting.CONTACT_INFORMATION)
        
        # Close the modal dialog
        btn_close = find_element_by_xpath(driver, "//div[@class='sc-ur24yu-4 jgnDww']//*[name()='svg']")
        click_element(element=btn_close)
        
        invisibility_of_element_by_testid(driver, "//div[normalize-space(text())='Contact Information']")

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e) 
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""