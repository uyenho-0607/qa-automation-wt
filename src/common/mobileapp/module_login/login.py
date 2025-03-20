import random

from constants.element_ids import DataTestID
from enums.main import AccountType, CredentialType, LoginResultState, Server

from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text
from data_config.encrypt_decrypt import decrypt_and_print
from constants.helper.element_android_app import clear_input_field, click_element, click_element_with_wait, get_label_of_element, populate_element, find_presence_element_by_testid, spinner_element, find_visible_element_by_testid, is_element_present_by_testid, find_element_by_testid_with_wait, wait_for_text_to_be_present_in_element_by_xpath
from data_config.file_handler import get_credentials


from common.mobileapp.module_announcement.announcement import modal_announcement
from common.mobileapp.module_login.language import select_and_verify_language, select_english_language


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SPLASH SCREEN
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def click_splash_screen(driver):
    find_presence_element_by_testid(driver, data_testid=DataTestID.ADS_SKIP_BUTTON)
    splash_screen = find_element_by_testid_with_wait(driver, data_testid=DataTestID.ADS_SKIP_BUTTON)
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
        input_search = find_visible_element_by_testid(driver, data_testid=DataTestID.SYMBOL_SEARCH_SELECTOR)
        return input_search.is_displayed()
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
    userinput_name = find_element_by_testid_with_wait(driver, data_testid=DataTestID.LOGIN_USER_ID)
    clear_input_field(element=userinput_name)
    populate_element(element=userinput_name, text=login_username)

    # Enter the username and password into the login form
    password_input = find_element_by_testid_with_wait(driver, data_testid=DataTestID.LOGIN_PASSWORD)
    clear_input_field(element=password_input)
    populate_element(element=password_input, text=login_password)

    # Click the login submit button
    submit_button = find_element_by_testid_with_wait(driver, data_testid=DataTestID.LOGIN_SUBMIT)
    click_element_with_wait(driver, element=submit_button)


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ACCOUNT TYPE SELECTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
def select_account_type(driver, account_type: AccountType = AccountType.LIVE):
    """
    Selects the desired account type (CRM, Live, Demo) during login.

    Args:
    - driver: WebDriver instance.
    - account_type (AccountType): Enum representing the account type.

    Raises:
    - ValueError: If an invalid account type is provided.
    """

    button_testids = {
        AccountType.CRM: DataTestID.TAB_LOGIN_ACCOUNT_TYPE_CRM,
        AccountType.LIVE: DataTestID.TAB_LOGIN_ACCOUNT_TYPE_LIVE,
        AccountType.DEMO: DataTestID.TAB_LOGIN_ACCOUNT_TYPE_DEMO
    }

    button_testid = button_testids.get(account_type)
    if not button_testid:
        raise ValueError(f"[ERROR] Invalid account type: {account_type}")

    acct_type_selector = find_element_by_testid_with_wait(driver, data_testid=button_testid)
    click_element_with_wait(driver, element=acct_type_selector)

    print(f"[INFO] Selected account type: {account_type}")


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                WT LOGIN PAGE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def wt_user_login(driver, server: Server, testcase_id: str = None, selected_language: str = None, 
                  expectation: LoginResultState = LoginResultState.SUCCESS, 
                  credential_type: CredentialType = CredentialType.DEFAULT) -> None:
    
    # Load credentials from the JSON file
    data = get_credentials(server)
    
    # Check if the server exists in the data
    if server not in data:
        raise ValueError(f"Server '{server}' not found in credentials data.")

    # Retrieve the specific server data for the given client and "MemberSite"
    server_data = data[server]["MemberSite"]

    if expectation == LoginResultState.FAILURE:
        if not testcase_id:
            raise ValueError("testcaseID must be provided for invalid_credential.")
        
        credential_type = CredentialType.INVALID_CREDENTIAL

    # Retrieve the credentials
    credentials_list = server_data.get(credential_type, [])
    
    if not credentials_list:
        raise ValueError(f"No {credential_type} data available for server '{server}'")
    
    if testcase_id:
        valid_testcases = [testcase for testcase in credentials_list if testcase["testcase_id"] == testcase_id]
        if not valid_testcases:
            raise ValueError(f"Testcase ID '{testcase_id}' not found in {credential_type} for server '{server}'")
        testcase = valid_testcases[0]
    else:
        testcase = random.choice(credentials_list)
    
    # Retrieve and decrypt credentials
    login_username = testcase["username"]
    login_password = decrypt_and_print(testcase["password"])
    
    # Perform login
    authenticate_user(driver, login_username, login_password)

    # Handle the result
    handle_login_result(driver, expectation, selected_language)

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


def handle_login_result(driver, expectation: LoginResultState, selected_language: str = None):
    """
    Handles the login result based on the expectation.
    """
    
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
    
    # Wait for spinner element not display
    spinner_element(driver)
    
    # Retrieve the expected text
    verification_text = language_specific_text.get(selected_language, "Trade")
    
    # Check if the test is present
    if wait_for_text_to_be_present_in_element_by_xpath(driver, DataTestID.APP_SIDE_BAR_OPTION_TRADE, text=verification_text):
        print("Successfully Logged In")
        
        # If login succeeded but failure was expected, log the unexpected success and fail the test
        if expectation == LoginResultState.FAILURE:
            attach_text("Expected failure, but login succeeded. Test failed.", name="Unexpected Success")
            assert False, "Expected failure, but login succeeded."
        
        # If login is successful and no failure was expected, process the modal announcement (if applicable)
        modal_announcement(driver)
        return
        
    else:
        # If "Trade" was not found, the login failed. Handle the error scenario.
        handle_alert_error(driver, expectation)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                RETRIEVE THE ERROR MESSAGE CONTENT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def handle_alert_error(driver, expectation: LoginResultState):
    """
    Handles expected or unexpected login failures.
    """
    spinner_element(driver)
    
    # Retrieve the error message notification
    error_message_notification = find_presence_element_by_testid(driver, data_testid=DataTestID.NOTIFICATION_BOX_DESCRIPTION)
    
    # Extract the text (label) of the error message from the notification element.
    error_message = get_label_of_element(element=error_message_notification)
    
    # Attach the extracted error message to the logs for reporting purposes.
    attach_text(error_message, name="Error Message:")
    
    expected_errors = [
        "Invalid Login", "Invalid credentials, please try again", 
        "Account already linked", "FXCRM Invalid Login"
    ]

    if expectation == LoginResultState.FAILURE:
        if error_message in expected_errors:
            attach_text("Expected failure condition met.", name="Expected Failure")
            assert True
        else:
            # If an unexpected error message is encountered during the expected failure case, fail the test
            assert False, f"Unexpected error message: {error_message}"
    else:
        # If login failed unexpectedly (failure was not expected), fail the test
        assert False, f"Unexpected login failure: {error_message}"
    
    # Click on the Confirm button
    btn_ok = find_element_by_testid_with_wait(driver, data_testid=DataTestID.NOTIFICATION_BOX_CLOSE)
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
def login_wt(driver, server: Server, testcase_id: str = None, 
             account_type: AccountType = AccountType.LIVE,
             set_language: bool = False, set_username: bool = True, 
             expectation: LoginResultState = LoginResultState.SUCCESS, 
             credential_type: CredentialType = CredentialType.DEFAULT) -> tuple[str, str] | None:
    
    """
    This function performs the complete login process to the WebTrader platform (WT).
    It launches the platform, selects the account type (Crm/Live/Demo), and logs into the member's site 
    using the provided credentials. It handles both successful and failure scenarios as specified.

    Arguments:
    - driver: WebDriver instance.
    - server (str): The server for login (e.g., 'MT4', 'MT5').
    - testcase_id (str, optional): The test case ID for fetching credentials.
    - account_type (AccountType, optional): Type of account. Defaults to LIVE.
    - set_language (bool, optional): If True, sets and verifies language selection.
    - set_username (bool, optional): If True, performs login with username and password.
    - expectation (LoginExpectation, optional): Expected login outcome. Defaults to SUCCESS.
    - credential_type (CredentialType, optional): Type of credentials to use.

    Returns:
    - tuple[str, str]: (username, password) if login is performed.
    - None: If already logged in or login is skipped.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    
    try:
        
        # Skip the splash screen
        click_splash_screen(driver)
        
        # Check if user is already logged in by looking for an element that is only present in login screen
        if check_symbol_element_present(driver):
            print("[INFO] User is already logged in, skipping login steps.")
            return

        # Step 2: Select the desired account type (either CRM / Live or Demo) for login.
        select_account_type(driver, account_type)
        
        # Select and verify language if required
        selected_language = None
        if set_language:
            selected_language = select_and_verify_language(driver)
            print(f"[INFO] Selected language: {selected_language}")
        else:
            select_english_language(driver)
            
        # Step 3: Perform the login action using the `wt_user_login` function. 
        # This handles credential retrieval, entry into the login form, and the actual login process.
        if set_username:
            username, password = wt_user_login(driver, server, testcase_id, selected_language, expectation, credential_type)
            return username, password

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""