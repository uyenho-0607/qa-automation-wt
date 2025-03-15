import random
import re
import subprocess

from constants.element_ids import DataTestID
from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text
from data_config.encrypt_decrypt import decrypt_and_print
from constants.helper.element_android_app import clear_input_field, click_element, click_element_with_wait, find_element_by_testid, find_element_by_xpath, find_list_of_elements_by_testid, get_label_of_element, is_element_present_by_xpath, populate_element, presence_of_element_located_by_testid, spinner_element, visibility_of_element_by_testid, is_element_present_by_testid, visibility_of_element_by_xpath, wait_for_element_clickable_testid, wait_for_element_clickable_xpath, wait_for_text_to_be_present_in_element_by_testid, wait_for_text_to_be_present_in_element_by_xpath
from data_config.file_handler import get_credentials


from common.mobileapp.module_announcement.announcement import modal_announcement



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SPLASH SCREEN
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def splash_screen(driver):
    if is_element_present_by_testid(driver, data_testid=DataTestID.ADS_SKIP_BUTTON.value):
        splash_screen = wait_for_element_clickable_testid(driver, data_testid=DataTestID.ADS_SKIP_BUTTON.value)
        click_element(splash_screen)
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                VERIFY IF SYMBOL SEARCH IS PRESENT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def check_symbol_element_present(driver):
    """Check if the user is already logged in by searching for an element that only appears after login """
    try:
        search_input = visibility_of_element_by_testid(driver, data_testid=DataTestID.SYMBOL_SEARCH_SELECTOR.value)
        return search_input.is_displayed()
    except:
        return False

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ACCOUNT TYPE SELECTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def authenticate_user(driver, login_username, login_password):
    
    # Enter the username and password into the login form
    userinput_name = wait_for_element_clickable_testid(driver, data_testid=DataTestID.LOGIN_USER_ID.value)
    clear_input_field(element=userinput_name)
    populate_element(element=userinput_name, text=login_username)

    # Enter the username and password into the login form
    password_input = wait_for_element_clickable_testid(driver, data_testid=DataTestID.LOGIN_PASSWORD.value)
    clear_input_field(element=password_input)
    populate_element(element=password_input, text=login_password)

    # Click the login submit button
    submit_button = wait_for_element_clickable_testid(driver, data_testid=DataTestID.LOGIN_SUBMIT.value)
    click_element_with_wait(driver, element=submit_button)


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ACCOUNT TYPE SELECTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def select_account_type(driver, account_type: str):
    button_testids = {
        "crm": DataTestID.TAB_LOGIN_ACCOUNT_TYPE_CRM.value,
        "live": DataTestID.TAB_LOGIN_ACCOUNT_TYPE_LIVE.value,
        "demo": DataTestID.TAB_LOGIN_ACCOUNT_TYPE_DEMO.value
    }
    
    button_testid = button_testids.get(account_type)
    if not button_testid:
        raise ValueError(f"Invalid button type: {account_type}")
    
    # Locate the account type selector element by its test ID.
    acct_type_selector = wait_for_element_clickable_testid(driver, data_testid=button_testid)
    # Perform a JavaScript click action on the located account type element.
    click_element_with_wait(driver, element=acct_type_selector)

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
    
    # Enter the username / password
    authenticate_user(driver, login_username, login_password)

    # Handle the result of the login (success or failure)
    handle_login_result(driver, expect_failure, selected_language)

    # Return the decrypted username used for login
    return login_username, login_password

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
    spinner_element(driver)
    
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
    if wait_for_text_to_be_present_in_element_by_xpath(driver, DataTestID.APP_SIDE_BAR_OPTION_TRADE.value, text=verification_text):
        print("Successfully Login")
    # If the account balance is found, the login is successful
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

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                RETRIEVE THE ERROR MESSAGE CONTENT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_alert_error(driver, expect_failure: bool = None):
    """
    This function handles the expected login error scenario by checking for the error notification 
    and extracting the error message. It then attaches the error message for logging or reporting purposes.

    Returns:
    - error_message: The error message text extracted from the login failure notification.
    """
    
    spinner_element(driver)
    
    # Retrieve the error message notification
    error_message_notification = presence_of_element_located_by_testid(driver, data_testid=DataTestID.NOTIFICATION_BOX_DESCRIPTION.value)
    
    # Extract the text (label) of the error message from the notification element.
    error_message = get_label_of_element(element=error_message_notification)
    # Attach the extracted error message to the logs for reporting purposes.
    attach_text(error_message, name="Error message found:")
    
    # Handle the expected failure case
    if expect_failure:
        # If an expected failure message is found, log it and pass the test
        if error_message in ["Invalid Login", "Invalid credentials, please try again", "Account already linked", "FXCRM Invalid Login"]:
            attach_text("Expected failure condition met.", name="Expected Failure")
            assert True  # Pass the test as failure was expected and encountered
        else:
            # If an unexpected error message is encountered during the expected failure case, fail the test
            assert False, f"Expected failure, but received unexpected message: {error_message}"
    else:
        # If login failed unexpectedly (failure was not expected), fail the test
        assert False, f"Unexpected error message: {error_message}"
    
    # Click on the Confirm button
    btn_ok = wait_for_element_clickable_testid(driver, data_testid=DataTestID.NOTIFICATION_BOX_CLOSE.value)
    click_element(element=btn_ok)

    # Return the error message for further processing or validation.
    return error_message
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
def login_wt(driver, server: str, client_name: str, testcaseID: str = None, account_type: str = "live", expect_failure: bool = False, use_read_only_access: bool = False, use_investor_cred: bool = False, use_crm_cred: bool = False, set_language: bool = False, set_username: bool = True) -> None:
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
        
        # Skip the splash screen
        splash_screen(driver)
        
        # Check if user is already logged in by looking for an element that is only present in login screen
        if check_symbol_element_present(driver):
            print("User is already logged in, skipping login steps.")
            return

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
            return username, password
    
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
        language_dropdown = visibility_of_element_by_testid(driver, data_testid=DataTestID.LANGUAGE_DROPDOWN.value)

        # Step 2: Get all available language options
        click_element(element=language_dropdown)
        languages_options = find_list_of_elements_by_testid(driver, data_testid=DataTestID.LANGUAGE_OPTION_APP.value)

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
            submit_button = find_element_by_testid(driver, data_testid=DataTestID.LOGIN_SUBMIT.value)
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
                click_element(element=language_dropdown)
                languages_options = find_list_of_elements_by_testid(driver, data_testid=DataTestID.LANGUAGE_OPTION_APP.value)

        # Return the last successfully verified language
        return selected_language
    
    except Exception as e:
        handle_exception(driver, e)
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                FORGOT PASSWORD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
        
def forgot_password(driver, email: str, accountID: str = None, account_type: str = "live"):
    try:
        
        # Skip the splash screen
        splash_screen(driver)
        
        # Step 2: Select account type (CRM/Live/Demo)
        select_account_type(driver, account_type)
        
        # Step 3: Verify and click the 'Forgot Password' button
        if not is_element_present_by_xpath(driver, DataTestID.APP_FORGOT_PASSWORD.value):
            raise AssertionError("Forgot Password button not found")
        
        # Locate the forgot Password button
        btn_forgot_password = wait_for_element_clickable_xpath(driver, DataTestID.APP_FORGOT_PASSWORD.value)
        click_element(element=btn_forgot_password)

        # Step 4: Wait for 'Reset Password' page
        wait_for_text_to_be_present_in_element_by_xpath(driver, DataTestID.APP_RESET_PASSWORD.value, text="Reset Password")
        
        # Step 5: Input email
        input_email = find_element_by_xpath(driver, DataTestID.APP_RESET_PASSWORD_EMAIL_ADDRESS.value)
        populate_element(element=input_email, text=email)
        
        # Step 6: Input account ID if required
        if account_type == "live" and accountID:
            input_accountID = find_element_by_xpath(driver, DataTestID.APP_RESET_PASSWORD_ACCOUNT_ID.value)
            populate_element(element=input_accountID, text=accountID)
        
        # Step 7: Click 'Submit' button
        click_element(element=find_element_by_xpath(driver, DataTestID.APP_RESET_PASSWORD_SUBMIT.value))
        
        # Step 8: Verify success message and navigate to Contact Support
        if wait_for_text_to_be_present_in_element_by_xpath(driver, DataTestID.APP_HELP_IS_ON_THE_WAY.value, text="Help is on the way!"):
            btn_contact_support = find_element_by_xpath(driver, DataTestID.APP_CONTACT_SUPPORT.value)
            click_element(element=btn_contact_support)
            
            # Get in-app browser url
            browser = visibility_of_element_by_xpath(driver, DataTestID.IN_APP_BROWSER_URL_bar.value)
            print(browser.text)
            
            # Click to close in-app browser
            browser = visibility_of_element_by_xpath(driver, DataTestID.IN_APP_BROWSER_CLOSE_BUTTON.value)
            click_element(element=browser)
            
            # Redirect back to login screen
            btn_back_to_login = visibility_of_element_by_xpath(driver, DataTestID.APP_BACK_TO_LOGIN_SCREEN.value)
            click_element(element=btn_back_to_login)
            
        else:
            # check for error occurs
            handle_alert_error(driver)

    except Exception as e:
        handle_exception(driver, e)
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def get_url_from_logcat():
    logcat_process = subprocess.Popen(["adb", "logcat", "-d"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logcat_output, _ = logcat_process.communicate()

    # Decode safely, ignoring errors
    logcat_text = logcat_output.decode("utf-8", errors="ignore")  # FIXED

    # Search for a URL in the log output
    url_pattern = re.compile(r"https?://[^\s]+")
    match = url_pattern.search(logcat_text)

    if match:
        return match.group(0)
    return None