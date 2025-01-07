from constants.helper.error_handler import handle_exception
from constants.helper.element import find_list_of_elements_by_testid, click_element


from common.desktop.module_notification.noti_general import notification_bell, notification_type

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NOTIFICATION BELL
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def noti_newDevice(driver):
    try:
        
        notification_bell(driver)
        
        notification_type(driver)
        
        noti_messages = find_list_of_elements_by_testid(driver, data_testid="notification-list-result-item")

        for message in noti_messages:
            # Check if the order ID is present in the notification message
            if "New Login Detected" in message.text:
                print("message", message.text)
            
                # Click on the matching notification message for further actions
                click_element(message)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""