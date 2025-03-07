
from constants.helper.error_handler import handle_exception
from constants.helper.element import wait_for_text_to_be_present_in_element_by_xpath, find_element_by_xpath, click_element, invisibility_of_element_by_xpath

from common.desktop.module_setting.setting_general import button_setting


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NOTIFICATION SETTING MODAL - LINKED DEVICES
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def contact_information(driver):
    try:
        
        button_setting(driver, setting_option="contact-information")
        
        # Close the modal dialog
        btn_close = find_element_by_xpath(driver, "//div[@class='sc-ur24yu-4 jgnDww']//*[name()='svg']")
        click_element(element=btn_close)
        
        invisibility_of_element_by_xpath(driver, "//div[normalize-space(text())='Contact Information']")

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e) 
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""