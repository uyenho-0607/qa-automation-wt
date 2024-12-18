import random
import traceback


from constants.helper.driver import access_url, delay, wait_for_url
from constants.helper.screenshot import take_screenshot, attach_text
from constants.helper.element import click_element, click_element_with_wait, find_element_by_testid, find_list_of_elements_by_testid, get_label_of_element, javascript_click, populate_element_with_wait, spinner_element, visibility_of_element_by_testid, visibility_of_element_by_xpath, wait_for_text_to_be_present_in_element_by_xpath
from constants.helper.error_handler import handle_exception

from data_config.encrypt_decrypt import decrypt_and_print
from data_config.fileHandler import get_URLs, get_credentials, get_success_urls

from common.desktop.module_announcement.utils import modal_announcement



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                LAUNCH WT WEBSITE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# platform: The platform type (MT4, MT5, RootAdmin).
# client_name: The client name (Lirunex / Transactcloudmt5)
# device_type: The environment type (Desktop, Mobile, Backoffice).
# env_type: The specific sub-environment (SIT, Release_SIT, UAT).

def launch_wt(driver, platform: str, client_name: str, device_type: str, env_type: str) -> None:

    urls = get_URLs()

    # Handle MT4 and MT5 structures with dynamic sub_key
    if platform not in urls or client_name not in urls[platform] or device_type not in urls[platform][client_name] or env_type not in urls[platform][client_name][device_type]:
        raise ValueError(f"Unsupported environment type: {platform} - {client_name} - {device_type} - {env_type}")
    
    params_wt_url = urls[platform][client_name][device_type][env_type]

    # Access the URL with optimized loading techniques
    access_url(driver, params_wt_url)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                WT LOGIN PAGE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def wt_user_login(driver, platform: str, client_name: str, device_type: str, env_type: str, testcaseID: str = None, expect_failure: bool = False, use_crm_cred: bool = False) -> None:

    # Load credentials from the JSON file
    data = get_credentials()

    # Check if the platform exists in the data
    if platform in data:
        platform_data = data[platform].get(client_name, {}).get("MemberSite", {})

        # If expect_failure is True, use Invalid_Credential and require testcaseID
        if expect_failure:
            if testcaseID is None:
                raise ValueError("testcaseID must be provided for Invalid_Credential.")
            
            credential_type = "Invalid_Credential"
            valid_testcases = [testcase for testcase in platform_data.get(credential_type, [])
                                if testcase["TestcaseID"] == testcaseID]
            if not valid_testcases:
                raise ValueError(f"Testcase ID '{testcaseID}' not found in {credential_type} for platform '{platform}'")
            testcase = valid_testcases[0]
        else:
            # If expect_failure is False, decide between CRM_Credential or Credential without testcaseID
            credential_type = "CRM_Credential" if use_crm_cred else "Credential"
            
            if not platform_data.get(credential_type):
                raise ValueError(f"No {credential_type} data available for platform '{platform}'")
            
            # Randomly pick a testcase from the selected credential list
            testcase = random.choice(platform_data[credential_type])
        
        # Retrieve the username and password from the selected testcase
        login_username_encrypted = testcase["Username"]
        login_password_encrypted = testcase["Password"]

        # Decrypt the credentials
        login_username = decrypt_and_print(login_username_encrypted)
        login_password = decrypt_and_print(login_password_encrypted)

        # Assuming these functions exist in your automation framework
        username_input = find_element_by_testid(driver, data_testid="login-user-id")
        populate_element_with_wait(driver, element=username_input, text=login_username)

        password_input = find_element_by_testid(driver, data_testid="login-password")
        populate_element_with_wait(driver, element=password_input, text=login_password)

        submit_button = find_element_by_testid(driver, data_testid="login-submit")
        click_element(submit_button)

        # handle_login_result(driver, platform, client_name, device_type, env_type, expect_failure)
        handle_login_result(driver, expect_failure)
        
    else:
        raise ValueError(f"Platform '{platform}' not found in credential data")

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                RETRIEVE THE ERROR MESSAGE CONTENT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_login_error(driver):
    # Handle the expected failure scenario
    error_message_notification = visibility_of_element_by_testid(driver, data_testid="alert-error")
    error_message = get_label_of_element(error_message_notification)
    attach_text(error_message, name="Error message found: ")
    return error_message

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                HANDLE LOGIN RESULT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# def handle_login_result(driver, platform, client_name, device_type, env_type, expect_failure=False):
def handle_login_result(driver, expect_failure=False):

    # Get the specific success URL from the JSON file based on platform, device type, and environment
    # success_url = get_success_urls(platform, env_type, client_name, device_type)
    
    # # Wait for the URL to change to the expected URL
    # matched_url = wait_for_url(driver, [success_url])
    spinner_element(driver)

    # Check for balance element to confirm successful login
    match = wait_for_text_to_be_present_in_element_by_xpath(driver, "//div[normalize-space(text())='Account Balance']", text="Account Balance")
    
    if match:
    # if matched_url:
        # If 'expect_failure' is True but login succeeded, fail the test
        if expect_failure:
            attach_text("Expected failure, but login succeeded without any error. Test failed as expected failure condition was not met.", name="Unexpected Success")
            assert False, "Expected failure, but login succeeded without error."
        
        modal_announcement(driver)
        assert True  # Pass the test as login succeeded as expected
        return  # Exit after processing the login request
    
    else:
        # If the URL does not match, handle the error
        error_message = handle_login_error(driver)
        
        if expect_failure:
            # Check for expected failure messages
            if error_message in ["Invalid Login", "Invalid credentials, please try again"]:
                attach_text("Expected failure condition met.", name="Expected Failure")
                assert True  # Pass the test as failure was expected and encountered
            else:
                # Fail the test if an unexpected error message was received
                assert False, f"Expected failure, but received unexpected message: {error_message}"
        else:
            # Fail the test as an unexpected error occurred when we were not expecting a failure
            assert False, f"Unexpected error message: {error_message}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ACCOUNT TYPE SELECTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def select_account_type(driver, account_type):
    
    acct_type_selector = visibility_of_element_by_testid(driver, data_testid=f"tab-login-account-type-{account_type}")
    javascript_click(driver, element=acct_type_selector)
    # return acct_type_selector

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                LOGIN STEP
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Login to WebTrader Website Release_SIT
def login_wt(driver, account_type, platform: str, client_name: str, testcaseID: str = None,  device_type: str = "Desktop", env_type: str = "Release_SIT", expect_failure: bool = False, use_crm_cred: bool = False) -> None:
    try:
            
        # launch_wt(driver, platform, device_type, env_type)
        launch_wt(driver, platform, client_name, device_type, env_type)

        select_account_type(driver, account_type)
        
        wt_user_login(driver, platform, client_name, device_type, env_type, testcaseID, expect_failure, use_crm_cred)
                
    except Exception as e:
        handle_exception(driver, e)


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                LANGUAGE SELECTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Login - Language dropdown selection
def language_change(driver, language_str: str = 'Japanese'):
    try:
        language_dropdown = find_element_by_testid(driver, data_testid="language-dropdown")
        
        click_element_with_wait(driver, element=language_dropdown)

        language_options = find_list_of_elements_by_testid(driver, data_testid="language-option")
        
        for option in language_options:
            if option.get_attribute('innerHTML') == language_str:
                click_element_with_wait(driver, element=option)
                break
            
    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "language_change - Exception Screenshot")
        # Log the full exception message and stacktrace
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""