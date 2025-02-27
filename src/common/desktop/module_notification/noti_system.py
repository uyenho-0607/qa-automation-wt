from constants.helper.error_handler import handle_exception
from constants.helper.element import find_element_by_xpath, get_label_of_element, spinner_element

from common.desktop.module_notification.noti_general import notification_bell, notification_type

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NOTIFICATION BELL
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def noti_newDevice(driver, state: str):
    try:
        
        notification_bell(driver)
        
        spinner_element(driver)
        
        notification_type(driver, notiType="system")
        
        spinner_element(driver)
        
        noti_messages = find_element_by_xpath(driver, "(//div[@class='sc-pq1npr-2 dRMTuG'])[1]")
        title = get_label_of_element(element=noti_messages)
        
        
        time = find_element_by_xpath(driver, "(//div[@class='sc-pq1npr-4 gyAjxX'])[1]")
        label_time = get_label_of_element(element=time)
        
        if state == "checked":
            # Check that "New Login Detected" and "a few seconds ago" is found
            if "New Login Detected" in title and "a few seconds ago" in label_time:
                print("message", title)
            else:
                assert False, f"Expected to display '{title}'"
                
        elif state == "unchecked":
            # Check that "New Login Detected" and "a few seconds ago" is found
            if "New Login Detected" not in title and "a few seconds ago" not in label_time:
                print(f"'{title}' not display")
            else:
                assert False, f"Not expecting '{title}' to be seen"
            
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

""""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""