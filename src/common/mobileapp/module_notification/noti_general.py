from constants.element_ids import DataTestID
from constants.helper.error_handler import handle_exception
from constants.helper.element_android_app import click_element, click_element_with_wait, find_element_by_testid_with_wait
from enums.main import NotificationTitle


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NOTIFICATION BELL
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def notification_bell(driver):
    try:
        
        # Click on the notification bell
        noti_bell = find_element_by_testid_with_wait(driver, data_testid=DataTestID.NOTIFICATION_SELECTOR)
        click_element_with_wait(driver, element=noti_bell)

    except Exception as e:
        # Handle any exceptions that occur during the execution
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

def notification_type(driver, notiType: NotificationTitle):
    try:
            
        # Define both possible 'data-testid' values for the radio button states
        button_notification = {
            NotificationTitle.ORDER: DataTestID.TAB_NOTIFICATION_TYPE_ORDER,
            NotificationTitle.SYSTEM: DataTestID.TAB_NOTIFICATION_TYPE_SYSTEM,
            NotificationTitle.INFORMATION: DataTestID.TAB_NOTIFICATION_TYPE_INFORMATION
        }
        
        button_testid = button_notification.get(notiType)
        if not button_testid:
            raise ValueError(f"Invalid button type: {notiType}")
        
        
        # Find all elements matching the attribute selector
        notifcation_type = find_element_by_testid_with_wait(driver, data_testid=button_testid)
        click_element(notifcation_type)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""