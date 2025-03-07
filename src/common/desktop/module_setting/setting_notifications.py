
from constants.helper.error_handler import handle_exception
from constants.helper.driver import access_url, get_current_url

from common.desktop.module_notification.noti_system import noti_newDevice
from common.desktop.module_trade.order_placing_window.module_oct import toggle_radioButton
from common.desktop.module_setting.setting_change_pwd import perform_login
from common.desktop.module_setting.setting_general import button_setting


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NOTIFICATION SETTING MODAL - LINKED DEVICES
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def notification_settings_modal(driver, category: str, desired_state: str, login_username: str = None, login_password: str = None, params_wt_url: str = None):
    try:
        
        button_setting(driver, setting_option="notification-setting")
        
        # Toggle ON / OFF the radio button
        state = toggle_radioButton(driver, category, desired_state)

        # Log the user out
        button_setting(driver, setting_option="logout")
    
        # Get the current URL after logout
        current_url = get_current_url(driver)
        
        # Assert that the URL should change to the login page
        if "web/login" in current_url:
            # Perform login with the provided username
            perform_login(driver, login_username, login_password)
        else:
            access_url(driver, url=params_wt_url)
            perform_login(driver, login_username, login_password)
        
        # Locate the new login device message
        noti_newDevice(driver, state)
    
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e) 
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""