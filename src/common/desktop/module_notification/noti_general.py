from constants.helper.error_handler import handle_exception
from constants.helper.element import javascript_click, find_element_by_testid


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NOTIFICATION BELL
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def notification_bell(driver):
    """
    This function waits for the notification bell to be visible and then clicks it 
    using JavaScript, ensuring the interaction works even if the element is not interactable
    via traditional Selenium actions.    
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    
    try:
        # Wait for the notification bell element to be visible before interacting
        noti_bell = find_element_by_testid(driver, data_testid="notification-selector")
        
        # Use JavaScript to click the notification bell
        javascript_click(driver, element=noti_bell)

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

def notification_type(driver, notiType):
    """
    This function locates the tab corresponding based on the given notification type
    and clicks on it to change the view to the respective notification type.
    
    Arguments:
    - notiType: The notification type to select (e.g., 'order', 'system', 'information').

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    
    try:
        # Wait for the notification type element to be present
        notifcation_type = find_element_by_testid(driver, data_testid=f"tab-notification-type-{notiType}")
        
        # Use JavaScript to click the notification tab
        javascript_click(driver, element=notifcation_type)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
   
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""