



from constants.element_ids import DataTestID
from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element_android_app import click_element, find_element_by_xpath, get_label_of_element, presence_of_element_located_by_testid, wait_for_element_clickable_testid, wait_for_element_clickable_xpath, is_element_present_by_xpath

from data_config.generate_fake_identity import generate_random_credential
from common.mobileapp.module_setting.utils import button_setting, change_password
from common.mobileapp.module_login.login import select_account_type, splash_screen, wt_user_login



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                VERIFY LOGIN FIELDS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def verify_login_fields(driver, expected_username, expected_password):
    userinput_name = wait_for_element_clickable_testid(driver, data_testid=DataTestID.LOGIN_USER_ID.value)
    assert userinput_name.get_attribute("text") == expected_username, "Username mismatch"

    password_unmasked = find_element_by_xpath(driver, DataTestID.APP_LOGIN_PASSWORD_UNMASKED.value)
    click_element(element=password_unmasked)

    password_input = wait_for_element_clickable_testid(driver, data_testid=DataTestID.LOGIN_PASSWORD.value)
    assert password_input.get_attribute("text") == expected_password, "Password mismatch"


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                OPEN DEMO ACCOUNT ERROR MESSAGE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
def toggle_remember_me_checkbox(driver, server: str, client_name: str, testcaseID: str = None, account_type: str = "live", expect_failure: bool = False, use_read_only_access: bool = False, use_investor_cred: bool = False, use_crm_cred: bool = False, check: bool = True, kick_user: bool = True):
    
    try:
        # Skip the splash screen
        splash_screen(driver)
        
        # Step 2: Select account type (CRM / Live)
        select_account_type(driver, account_type)
        
        # Verify the current checkbox status
        is_checked = is_element_present_by_xpath(driver, DataTestID.APP_RMB_ME_CHECKBOX.value)
        print("Checkbox value:", is_checked)
        
        # Verify the current status
        if is_checked != check:
            # Declare the checkbox xpath
            checkbox_xpath = (DataTestID.APP_RMB_ME_CHECKBOX.value if is_checked else DataTestID.APP_RMB_ME_UNCHECKBOX.value)
            
            # Click on the checkbox
            checkbox = wait_for_element_clickable_xpath(driver, checkbox_xpath)
            click_element(element=checkbox)
            print("Checkbox toggled")
        
        # Continue with login process
        username, password = wt_user_login(driver, server, client_name, testcaseID, expect_failure, use_read_only_access, use_investor_cred, use_crm_cred)
        print(username, password)

        # Log the user out
        if kick_user:
            
            button_setting(driver, setting_option="logout")
            
            verify_login_fields(driver, expected_username=username, expected_password=password)
        
        else:
            
            button_setting(driver, setting_option="change-password")
            
            credential = generate_random_credential(length=12)
            print("Generated credential:", credential)
            
            # Change account password
            change_password(driver, old_password=password, new_password=credential, confirm_password=credential)
            
            # Retrieve the error message notification
            success_message_notification = presence_of_element_located_by_testid(driver, data_testid=DataTestID.NOTIFICATION_BOX_DESCRIPTION.value)
            
            # Extract the text (label) of the error message from the notification element.
            label_message = get_label_of_element(element=success_message_notification)
            
            # If the success message indicates a password change, process it
            if "Account password has been updated successfully" in label_message:
                attach_text(label_message, name="Success message found:")
                
                # Click on the Confirm button
                btn_ok = wait_for_element_clickable_testid(driver, data_testid=DataTestID.NOTIFICATION_BOX_CLOSE.value)
                click_element(element=btn_ok)
                
                # Log the user out
                button_setting(driver, setting_option="logout", menu=False)
                
                verify_login_fields(driver, expected_username=username, expected_password=credential)
                
            else:
                # If the success message doesn't match, handle it as an unexpected message
                assert False, f"Unexpected success message: {label_message}"
    
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def verify_incorrect_credential(driver, server: str, client_name: str, testcaseID: str = None, account_type: str = "live", expect_failure: bool = False, use_read_only_access: bool = False, use_investor_cred: bool = False, use_crm_cred: bool = False, check: bool = True, kick_user: bool = True):

    try:
        
        # Skip the splash screen
        splash_screen(driver)
        
        # Step 2: Select account type (CRM / Live)
        select_account_type(driver, account_type)
        
        # Verify the current checkbox status
        is_checked = is_element_present_by_xpath(driver, DataTestID.APP_RMB_ME_CHECKBOX.value)
        print("Checkbox value:", is_checked)
        
        # Verify the current status
        if is_checked != check:
            # Declare the checkbox xpath
            checkbox_xpath = (DataTestID.APP_RMB_ME_CHECKBOX.value if is_checked else DataTestID.APP_RMB_ME_UNCHECKBOX.value)
            
            # Click on the checkbox
            checkbox = wait_for_element_clickable_xpath(driver, checkbox_xpath)
            click_element(element=checkbox)
            print("Checkbox toggled")
        
        # Continue with login process
        username, password = wt_user_login(driver, server, client_name, testcaseID, expect_failure, use_read_only_access, use_investor_cred, use_crm_cred)
        print(username, password)

        # userinput_name = wait_for_element_clickable_testid(driver, data_testid=DataTestID.LOGIN_USER_ID.value)
        # assert userinput_name.get_attribute("text") == expected_username, "Username mismatch"

        # password_unmasked = find_element_by_xpath(driver, DataTestID.APP_LOGIN_PASSWORD_UNMASKED.value)
        # click_element(element=password_unmasked)

        # password_input = wait_for_element_clickable_testid(driver, data_testid=DataTestID.LOGIN_PASSWORD.value)
        # assert password_input.get_attribute("text") == expected_password, "Password mismatch"

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)