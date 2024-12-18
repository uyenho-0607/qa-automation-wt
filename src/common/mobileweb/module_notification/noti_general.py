from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, click_element_with_wait, find_element_by_testid


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NOTIFICATION BELL
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def notification_bell(driver):
    try:
        
        # Click on the notification bell
        noti_bell = find_element_by_testid(driver, data_testid="notification-selector")
        click_element_with_wait(driver, element=noti_bell)

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
   

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NOTIFICATION TYPE (TO SELECT THE ORDER / SYSTEM / INFORMATION BUTTON)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def notification_type(driver, notiType):
    try:

        # Find all elements matching the attribute selector
        notifcation_type = find_element_by_testid(driver, data_testid=f"tab-notification-type-{notiType}")
        click_element(notifcation_type)

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""