import random
import logging


from constants.helper.driver import access_url, delay, get_current_url, switch_to_new_window, url_changes
from constants.helper.screenshot import attach_text
from constants.helper.element import click_element, click_element_with_wait, is_element_present_by_xpath, find_element_by_xpath, find_element_by_testid, find_list_of_elements_by_testid, get_label_of_element, javascript_click, populate_element, spinner_element, visibility_of_element_by_xpath, visibility_of_element_by_testid, wait_for_text_to_be_present_in_element_by_testid, wait_for_text_to_be_present_in_element_by_xpath
from constants.helper.error_handler import handle_exception

from data_config.encrypt_decrypt import decrypt_and_print
from data_config.fileHandler import get_URLs, get_credentials

from common.desktop.module_announcement.utils import modal_announcement


# Configure logging
# Log everything at DEBUG level and above
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                LAUNCH WT WEBSITE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def launch_wt(driver, server: str, client_name: str, device_type: str, env_type: str) -> None:
    """
    This function launches the web trader server (WT) for a given server, client, device type, and environment type.
    It retrieves the appropriate URL from a structured dictionary, validates the existence of the necessary keys, 
    and accesses the URL using the provided Selenium WebDriver instance.
    
    Arguments:
    - driver: The Selenium WebDriver instance used for browser automation.
    - server: The server type (e.g., 'MT4', 'MT5').
    - client_name: The name of the client to load the server for (e.g., 'Lirunex', 'Transactcloudmt5').
    - device_type: The type of device (e.g., 'Desktop', 'Mobile').
    - env_type: The environment type (e.g., 'SIT', 'Release_SIT', 'Release_SIT').
    
    Returns:
    - None: The function does not return anything. It navigates to the appropriate URL.
    
    Raises:
    - ValueError: If any of the parameters do not match a valid URL structure.
    """
    urls = get_URLs()

    # Handle MT4 and MT5 structures with dynamic sub_key
    if server not in urls or client_name not in urls[server] or device_type not in urls[server][client_name] or env_type not in urls[server][client_name][device_type]:
        raise ValueError(f"Unsupported environment type: {server} - {client_name} - {device_type} - {env_type}")
    
    params_wt_url = urls[server][client_name][device_type][env_type]
    
    # Access the URL with optimized loading techniques
    access_url(driver, params_wt_url)
    
    return params_wt_url
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                WT LOGIN PAGE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def wt_user_login(driver, server: str, client_name: str, testcaseID: str = None, selected_language: str = None, expect_failure: bool = False, use_read_only_access: bool = False, use_investor_cred: bool = False, use_crm_cred: bool = False) -> None:
    """
    This function automates the login process for a web trader platform (WT) using credentials from a JSON file.
    The function handles both valid and invalid login scenarios and supports choosing between CRM or regular credentials.

    Arguments:
    - driver: The Selenium WebDriver instance used for browser automation.
    - server: The server (e.g., "MT4", "MT5") for which the login is performed.
    - client_name: The client name (e.g., "Lirunex")to be used for the login.
    - testcaseID: The ID of the test case (if specific credentials are needed for invalid credentials).
    - expect_failure: A boolean flag to indicate whether a failed login scenario is expected.
    - use_crm_cred: A boolean flag to decide whether to use CRM credentials or standard credentials.

    Returns:
    - login_username: The decrypted username used for the login.

    Raises:
    - ValueError: If invalid inputs or missing values are encountered (e.g., server not found, missing testcaseID).
    """

    # Load credentials from the JSON file
    data = get_credentials()

    # Check if the server exists in the data
    if server in data:
        # Retrieve the specific server data for the given client and "MemberSite"
        server_data = data[server].get(client_name, {}).get("MemberSite", {})

        # If expect_failure is True, use Invalid_Credential and require testcaseID
        if expect_failure:
            if testcaseID is None:
                raise ValueError("testcaseID must be provided for Invalid_Credential.")
        
            # Select the "Invalid_Credential" type and search for the matching testcaseID
            credential_type = "Invalid_Credential"
            valid_testcases = [testcase for testcase in server_data.get(credential_type, [])
                                if testcase["TestcaseID"] == testcaseID]
            if not valid_testcases:
                raise ValueError(f"Testcase ID '{testcaseID}' not found in {credential_type} for server '{server}'")
            testcase = valid_testcases[0]
        else:
            # If expect_failure is False, decide between CRM_Credential, Credential, or Read_Only_Access
            if use_read_only_access:
                # If Read_Only_Access is requested, select from that category
                credential_type = "Read_Only_Access"
            elif use_investor_cred:
                credential_type = "Investor_Account"
            elif use_crm_cred:
                # Otherwise, use CRM_Credential if specified
                credential_type = "CRM_Credential"
            else:
                # Default to Credential
                credential_type = "Credential"

            # If a testcaseID is provided, attempt to find the specific testcase
            if testcaseID:
                valid_testcases = [testcase for testcase in server_data.get(credential_type, [])
                                    if testcase["TestcaseID"] == testcaseID]
                if not valid_testcases:
                    raise ValueError(f"Testcase ID '{testcaseID}' not found in {credential_type} for server '{server}'")
                testcase = valid_testcases[0]
            else:
                # If no testcaseID is provided, randomly select a testcase from available credentials
                if not server_data.get(credential_type):
                    raise ValueError(f"No {credential_type} data available for server '{server}'")
                
                testcase = random.choice(server_data[credential_type])
        
        # Retrieve the username and password from the selected testcase
        login_username = testcase["Username"]
        login_password_encrypted = testcase["Password"]

        # Decrypt the credentials
        login_password = decrypt_and_print(login_password_encrypted)

        # Enter the username and password into the login form
        username_input = find_element_by_testid(driver, data_testid="login-user-id")
        populate_element(element=username_input, text=login_username)

        # Enter the username and password into the login form
        password_input = find_element_by_testid(driver, data_testid="login-password")
        populate_element(element=password_input, text=login_password)

        # Click the login submit button
        submit_button = find_element_by_testid(driver, data_testid="login-submit")
        click_element(submit_button)

        # Handle the result of the login (success or failure)
        handle_login_result(driver, expect_failure, selected_language)

        # Return the decrypted username used for login
        return login_username, login_password
    else:
        # Raise an error if the server is not found in the credential data
        raise ValueError(f"Server '{server}' not found in credential data")

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                HANDLE LOGIN RESULT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_login_result(driver, expect_failure: bool = False, selected_language: str = None):
    """
    Handles the login result by verifying the presence of the expected text based on the selected language.
    """
    try:
        
        # Language-specific verification map
        language_specific_text = {
            "English": "Trade",
            "简体中文": "交易",
            "繁体中文": "交易",
            "ภาษาไทย": "เทรด",
            "Tiếng Việt": "Giao dịch",
            "Melayu": "Perdagangan",
            "Bahasa Indonesia": "Berdagang",
            "Japanese": "取引",
            "Korean": "거래"
        }
        
        # Wait till the spinner icon no longer display
        # spinner_element(driver)
    
        # Determine the text to wait for based on the selected language
        verification_text = language_specific_text.get(selected_language, "Trade")

        # Wait until the text is present in the specified element
        match = wait_for_text_to_be_present_in_element_by_testid(driver, data_testid="side-bar-option-trade", text=verification_text)

        # If the account balance is found, the login is successful
        if match:
            # If login succeeded but failure was expected, log the unexpected success and fail the test
            if expect_failure:
                attach_text("Expected failure, but login succeeded without any error. Test failed as expected failure condition was not met.", name="Unexpected Success")
                assert False, "Expected failure, but login succeeded without error."
            
            # If login is successful and no failure was expected, process the modal announcement (if applicable)
            modal_announcement(driver)
            assert True  # Pass the test as login succeeded as expected
        else:
            # If account balance was not found, the login failed. Handle the error scenario.
            handle_alert_error(driver, expect_failure)

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                RETRIEVE THE ERROR MESSAGE CONTENT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_alert_error(driver, expect_failure: bool):
    """
    This function handles the expected login error scenario by checking for the error notification 
    and extracting the error message. It then attaches the error message for logging or reporting purposes.

    Returns:
    - error_message: The error message text extracted from the login failure notification.
    """
    # Locate the error message notification element by its test ID.
    error_message_notification = visibility_of_element_by_testid(driver, data_testid="alert-error")
    # Extract the text (label) of the error message from the notification element.
    error_message = get_label_of_element(element=error_message_notification)
    # Attach the extracted error message to the logs for reporting purposes.
    attach_text(error_message, name="Error message found:")
    
    # Handle the expected failure case
    if expect_failure:
        # If an expected failure message is found, log it and pass the test
        if error_message in ["Invalid Login", "Invalid credentials, please try again", "Account already linked"]:
            attach_text("Expected failure condition met.", name="Expected Failure")
            assert True  # Pass the test as failure was expected and encountered
        else:
            # If an unexpected error message is encountered during the expected failure case, fail the test
            assert False, f"Expected failure, but received unexpected message: {error_message}"
    else:
        # If login failed unexpectedly (failure was not expected), fail the test
        assert False, f"Unexpected error message: {error_message}"
    
    # Return the error message for further processing or validation.
    return error_message

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ACCOUNT TYPE SELECTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def select_account_type(driver, account_type: str):
    """
    This function selects the specified account type (e.g., 'demo', 'live') by clicking the corresponding tab 
    on the login page. The account type tab is identified using its test ID.

    Arguments:
    - account_type: The type of account to select, typically 'crm', 'live', 'demo'.
    
    Returns:
    - None: This function performs the action of selecting the account type tab.
    """

    # Locate the account type selector element by its test ID.
    acct_type_selector = visibility_of_element_by_testid(driver, data_testid=f"tab-login-account-type-{account_type}")

    # Perform a JavaScript click action on the located account type element.
    javascript_click(driver, element=acct_type_selector)

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
def login_wt(driver, server: str, client_name: str, testcaseID: str = None, account_type: str = "live", device_type: str = "Desktop", env_type: str = "SIT", expect_failure: bool = False, use_read_only_access: bool = False, use_investor_cred: bool = False, use_crm_cred: bool = False, set_language: bool = False, set_username: bool = True) -> None:
    """
    This function performs the complete login process to the WebTrader platform (WT).
    It launches the platform, selects the account type (Crm/Live/Demo), and logs into the member's site 
    using the provided credentials. It handles both successful and failure scenarios as specified.

    Arguments:
    - account_type: The type of account to select (e.g., 'crm', 'live', 'demo').
    - server: The server to use for login (e.g., 'MT4', 'MT5').
    - client_name: The name of the client associated with the login.
    - testcaseID: The test case ID to identify the specific credentials (if any).
    - device_type: The type of device (defaults to 'Desktop').
    - env_type: The environment type (defaults to 'Release_SIT').
    - expect_failure: Flag to indicate if login failure is expected.
    - use_crm_cred: Flag to indicate if CRM credentials should be used.

    Returns:
    - username: The username used for the login, returned after successful login.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    
    try:
        
        # Step 1: Launch and navigate to the WebTrader platform URL based on the provided parameters.
        params_wt_url = launch_wt(driver, server, client_name, device_type, env_type)

        # Step 2: Select the desired account type (either Crm / Live or Demo) for login.
        select_account_type(driver, account_type)
        
        # Select and verify language if required
        selected_language = None
        if set_language:
            selected_language = select_and_verify_language(driver)
            print("selected language", selected_language)
            
        # Step 3: Perform the login action using the `wt_user_login` function. 
        # This handles credential retrieval, entry into the login form, and the actual login process.
        if set_username:
            username, password = wt_user_login(driver, server, client_name, testcaseID, selected_language, expect_failure, use_read_only_access, use_investor_cred, use_crm_cred)
            return params_wt_url, username, password
    
    except Exception as e:
        # Handle any exceptions that occur during the execution
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

def select_and_verify_language(driver):
    """
    Randomly selects three different languages from the dropdown,
    verifies if the change is reflected on the login button, and repeats for each language.

    Args:
        driver (webdriver): Selenium WebDriver instance.
    """
    try:
        
        # Language map for verification values
        language_map = {
            "English": "Sign in",
            "简体中文": "登录",
            "繁体中文": "登錄",
            "ภาษาไทย": "เปิดบัญชีซื้อขายจริง",
            "Tiếng Việt": "Đăng nhập",
            "Melayu": "Log masuk",
            "Bahasa Indonesia": "Masuk",
            "Japanese": "ログイン",
            "Korean": "로그인"
        }

        # Step 1: Locate the language dropdown
        language_dropdown = visibility_of_element_by_testid(driver, data_testid="language-dropdown")

        # Step 2: Get all available language options
        click_element_with_wait(driver, element=language_dropdown)
        languages_options = find_list_of_elements_by_testid(driver, data_testid="language-option")

        # Keep track of selected languages to avoid repetition
        selected_languages = []

        # Step 3: Select and verify languages
        for i in range(3):  # Repeat for 3 different random languages
            # Filter out languages already selected
            remaining_languages = [lang for lang in languages_options if lang.text not in selected_languages]

            if not remaining_languages:
                print("No more languages left to select.")
                break

            random_language = random.choice(remaining_languages)
            selected_language = random_language.text
            print(f"Selected language: {selected_language}")

            # Step 4: Click on the selected language
            click_element(element=random_language)
            
            delay(0.5)

            # Step 5: Verify if the change is reflected
            submit_button = find_element_by_testid(driver, data_testid="login-submit")
            button_text = submit_button.text.strip()

            # Get the expected value from the language map
            expected_text = language_map.get(selected_language)

            # Compare the button text with the expected text
            if button_text == expected_text:
                print(f"Language '{selected_language}' verified successfully.")
            else:
                assert False, f"Verification failed for language '{selected_language}', Expected: '{expected_text}', Found: '{button_text}''"

            # Add the selected language to the list to avoid re-selection
            selected_languages.append(selected_language)
            
            # Only click dropdown again if it's **not the last iteration**
            if i < 2:  # Since range(3) means last index is 2
                click_element_with_wait(driver, element=language_dropdown)
                languages_options = find_list_of_elements_by_testid(driver, data_testid="language-option")

        # Return the last successfully verified language
        return selected_language
    
    except Exception as e:
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
        
def forgot_password(driver, server: str, client_name: str, account_type: str, email: str, accountID: str = None, device_type: str = "Desktop", env_type: str = "SIT"):
    try:
        # Step 1: Launch WebTrader platform
        launch_wt(driver, server, client_name, device_type, env_type)
        
        # Step 2: Select account type (CRM/Live/Demo)
        select_account_type(driver, account_type)
        
        # Step 3: Verify and click the 'Forgot Password' button
        if not is_element_present_by_xpath(driver, "//*[normalize-space(text())='Forgot Password?']"):
            raise AssertionError("Forgot Password button not found")
        
        # Locate the forgot Password button
        btn_forgot_password = visibility_of_element_by_xpath(driver, "//*[normalize-space(text())='Forgot Password?']")

        # Perform a JavaScript click action on the located account type element.
        javascript_click(driver, element=btn_forgot_password)
                
        # Step 4: Wait for 'Reset Password' page
        wait_for_text_to_be_present_in_element_by_xpath(driver, "//*[normalize-space(text())='Reset Password']", text="Reset Password")
        
        # Step 5: Input email
        input_email = find_element_by_xpath(driver, "//input[@placeholder='user@gmail.com']")
        populate_element(element=input_email, text=email)
        
        # Step 6: Input account ID if required
        if account_type == "live" and accountID:
            input_accountID = find_element_by_xpath(driver, "//input[@placeholder='Enter your account ID']")
            populate_element(element=input_accountID, text=accountID)
        
        # Step 7: Click 'Submit' button
        click_element(element=find_element_by_xpath(driver, "//*[normalize-space(text())='Submit']"))
        
        
        if wait_for_text_to_be_present_in_element_by_xpath(driver, "//*[normalize-space(text())='FXCRM Invalid Login']", text="FXCRM Invalid Login"):
            error_msg = find_element_by_xpath(driver, "//*[normalize-space(text())='FXCRM Invalid Login']")
            raise AssertionError("Error message promoted", error_msg.text)
        
        # Step 8: Verify success message and navigate to Contact Support
        elif wait_for_text_to_be_present_in_element_by_xpath(driver, "//*[normalize-space(text())='Help is on the way!']", text="Help is on the way!"):
            btn_contact_support = find_element_by_xpath(driver, "//*[normalize-space(text())='Contact Support']")
            click_element(element=btn_contact_support)
            
            # Switch to the new window
            switch_to_new_window(driver)
            
            # Step 9: Capture and print the current URL
            print(get_current_url(driver))
    
    except Exception as e:
        handle_exception(driver, e)