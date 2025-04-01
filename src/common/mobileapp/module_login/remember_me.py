



from constants.element_ids import DataTestID
from enums.main import AccountType, CredentialType, AlertType, Setting

from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element_android_app import click_element, find_element_by_xpath, get_label_of_element, find_presence_element_by_testid, find_element_by_testid_with_wait, find_element_by_xpath_with_wait, is_element_present_by_xpath

from data_config.generate_dummy_data import generate_random_credential
from common.mobileapp.module_setting.utils import button_setting, change_password
from common.mobileapp.module_login.utils import select_account_type, click_splash_screen, wt_user_login
from common.mobileapp.module_login.language import select_english_language



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                VERIFY LOGIN FIELDS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def verify_login_fields(driver, expected_username, expected_password):
    userinput_name = find_element_by_testid_with_wait(driver, data_testid=DataTestID.LOGIN_USER_ID)
    assert userinput_name.get_attribute("text") == expected_username, "Username mismatch"

    password_unmasked = find_element_by_xpath(driver, DataTestID.APP_LOGIN_PASSWORD_UNMASKED)
    click_element(element=password_unmasked)

    password_input = find_element_by_testid_with_wait(driver, data_testid=DataTestID.LOGIN_PASSWORD)
    assert password_input.get_attribute("text") == expected_password, "Password mismatch"


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                OPEN DEMO ACCOUNT ERROR MESSAGE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



def toggle_remember_me_checkbox(driver, server: str, testcase_id: str = None, 
                                account_type: AccountType = AccountType.LIVE, 
                                expectation: AlertType = AlertType.SUCCESS,
                                credential_type: CredentialType = CredentialType.TOGGLE_REMEMBER_ME,
                                kick_user: bool = True):
    
    try:
        # Skip the splash screen
        click_splash_screen(driver)
        
        # Step 2: Select account type (CRM / Live)
        select_account_type(driver, account_type)
        
        # Step 3: Locate the language dropdown
        select_english_language(driver)
                
        # Verify the current checkbox status
        is_checked = is_element_present_by_xpath(driver, DataTestID.APP_RMB_ME_CHECKBOX)
        
        # Verify the current status
        if is_checked != True:
        # if is_checked is not True or is_checked is not False:
            # Declare the checkbox xpath
            checkbox_xpath = (DataTestID.APP_RMB_ME_CHECKBOX if is_checked else DataTestID.APP_RMB_ME_UNCHECKBOX)
            
            # Click on the checkbox
            checkbox = find_element_by_xpath_with_wait(driver, checkbox_xpath)
            click_element(element=checkbox)
                
        # Continue with login process
        username, password = wt_user_login(driver, server, testcase_id, expectation, credential_type)
        print(username, password)
        
        # Log the user out
        if kick_user:
            # Click on the logout button
            button_setting(driver, setting_option=Setting.LOGOUT)
            
            verify_login_fields(driver, expected_username=username, expected_password=password)
        
        else:
            # Click on change password button
            button_setting(driver, setting_option=Setting.CHANGE_PASSWORD)
            
            credential = generate_random_credential(length=12)
            
            # Change account password
            change_password(driver, old_password=password, new_password=credential, confirm_password=credential)
            
            # Retrieve the error message notification
            success_message_notification = find_presence_element_by_testid(driver, data_testid=DataTestID.NOTIFICATION_BOX_DESCRIPTION)
            
            # Extract the text (label) of the error message from the notification element.
            label_message = get_label_of_element(element=success_message_notification)
            
            # If the success message indicates a password change, process it
            if "Account password has been updated successfully" in label_message:
                attach_text(label_message, name="Success message found:")
                
                # Click on the Confirm button
                btn_ok = find_element_by_testid_with_wait(driver, data_testid=DataTestID.NOTIFICATION_BOX_CLOSE)
                click_element(element=btn_ok)
                
                # Log the user out
                button_setting(driver, setting_option=Setting.LOGOUT, menu=False)
                
                verify_login_fields(driver, expected_username=username, expected_password=credential)
                
            else:
                # If the success message doesn't match, handle it as an unexpected message
                assert False, f"Unexpected success message: {label_message}"

        return username, password
    
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""