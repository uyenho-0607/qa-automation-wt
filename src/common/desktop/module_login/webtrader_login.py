import random

from constants.element_ids import DataTestID
from enums.main import Server, Platform, ClientName, AccountType, CredentialType, EnvironmentType, LoginResultState

from constants.helper.driver import access_url
from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, is_element_present_by_testid, find_element_by_testid, get_label_of_element, javascript_click, populate_element, find_visible_element_by_testid, spinner_element, wait_for_text_to_be_present_in_element_by_xpath

from data_config.encrypt_decrypt import decrypt_and_print
from data_config.file_handler import get_URLs, get_credentials
from common.desktop.module_announcement.utils import modal_announcement
from common.desktop.module_login.language import select_and_verify_language, select_english_language


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                LAUNCH WT WEBSITE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def launch_wt(driver, server: Server, device_type: Platform, env_type: EnvironmentType) -> None:
    """
    This function launches the web trader server (WT) for a given server, client, device type, and environment type.
    It retrieves the appropriate URL from a structured dictionary, validates the existence of the necessary keys, 
    and accesses the URL using the provided Selenium WebDriver instance.
    
    Arguments:
    - driver: The Selenium WebDriver instance used for browser automation.
    - server: The server type (e.g., 'MT4', 'MT5').
    - device_type: The type of device (e.g., 'Desktop', 'Mobile').
    - env_type: The environment type (e.g., 'SIT', 'Release_SIT', 'Release_SIT').
    
    Returns:
    - None: The function does not return anything. It navigates to the appropriate URL.
    
    Raises:
    - ValueError: If any of tthen he parameters do not match a valid URL structure.
    """
    urls = get_URLs(server)

    # Handle MT4 and MT5 structures with dynamic sub_key
    if server not in urls or device_type not in urls[server] or env_type not in urls[server][device_type]:
        raise ValueError(f"Unsupported environment type: {server} - {device_type} - {env_type}")

    params_wt_url = urls[server][device_type][env_type]

    # Access the URL with optimized loading techniques
    access_url(driver, params_wt_url)
    
    return params_wt_url
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def authenticate_user(driver, login_username, login_password):
    
    # Enter the username and password into the login form
    userinput_name = find_element_by_testid(driver, data_testid=DataTestID.LOGIN_USER_ID)
    populate_element(element=userinput_name, text=login_username)

    # Enter the username and password into the login form
    password_input = find_element_by_testid(driver, data_testid=DataTestID.LOGIN_PASSWORD)
    populate_element(element=password_input, text=login_password)

    # Click the login submit button
    submit_button = find_element_by_testid(driver, data_testid=DataTestID.LOGIN_SUBMIT)
    click_element(submit_button)


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ACCOUNT TYPE SELECTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def select_account_type(driver, account_type: AccountType = AccountType.LIVE):
    """
    This function selects the specified account type (e.g., 'demo', 'live') by clicking the corresponding tab 
    on the login page. The account type tab is identified using its test ID.

    Arguments:
    - account_type: The type of account to select, typically 'crm', 'live', 'demo'.
    
    Returns:
    - None: This function performs the action of selecting the account type tab.
    """
            
    button_testids = {
        AccountType.CRM: DataTestID.TAB_LOGIN_ACCOUNT_TYPE_CRM,
        AccountType.LIVE: DataTestID.TAB_LOGIN_ACCOUNT_TYPE_LIVE,
        AccountType.DEMO: DataTestID.TAB_LOGIN_ACCOUNT_TYPE_DEMO
    }
    
    button_testid = button_testids.get(account_type)
    if not button_testid:
        raise ValueError(f"Invalid button type: {account_type}")

    # Locate the account type selector element by its test ID.
    acct_type_selector = find_visible_element_by_testid(driver, data_testid=button_testid)
    
    # Perform a JavaScript click action on the located account type element.
    javascript_click(driver, element=acct_type_selector)

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
    """
    This function automates the login process for a web trader platform (WT) using credentials from a JSON file.
    The function handles both valid and invalid login scenarios and supports choosing between CRM or regular credentials.

    Arguments:
    - driver: The Selenium WebDriver instance used for browser automation.
    - server: The server (e.g., "MT4", "MT5") for which the login is performed.
    - testcaseID: The ID of the test case (if specific credentials are needed for invalid credentials).
    - expect_failure: A boolean flag to indicate whether a failed login scenario is expected.
    - use_crm_cred: A boolean flag to decide whether to use CRM credentials or standard credentials.

    Returns:
    - login_username: The decrypted username used for the login.

    Raises:
    - ValueError: If invalid inputs or missing values are encountered (e.g., server not found, missing testcaseID).
    """

    # Load credentials from the JSON file
    data = get_credentials(server)

    # Check if the server exists in the data
    if server not in data:
        raise ValueError(f"Server '{server}' not found in credentials data.")

    # Retrieve the specific server data for the given client and "MemberSite"
    # server_data = data[server].get(client_name, {}).get("MemberSite", {})
    server_data = data[server]["MemberSite"]
    
    # If expect failure, use Invalid_Credential and require testcaseID
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
        
    # Retrieve the username and password from the selected testcase
    login_username = testcase["username"]
    login_password = decrypt_and_print(testcase["password"])  # Decrypt the credentials
    
    # Perform login
    authenticate_user(driver, login_username, login_password)
    
    # Handle the result of the login (success or failure)
    handle_login_result(driver, expectation, selected_language)

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

def handle_login_result(driver, expectation: LoginResultState, selected_language: str = None):
    """
    Handles the login result by verifying the presence of the expected text based on the selected language.
    """

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
    spinner_element(driver)

    # Determine the text to wait for based on the selected language
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
        # If account balance was not found, the login failed. Handle the error scenario.
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
    This function handles the expected login error scenario by checking for the error notification 
    and extracting the error message. It then attaches the error message for logging or reporting purposes.

    Returns:
    - error_message: The error message text extracted from the login failure notification.
    """
    
    if is_element_present_by_testid(driver, data_testid=DataTestID.ALERT_ERROR):
        # Locate the error message notification element by its test ID.
        error_message_notification = find_visible_element_by_testid(driver, data_testid=DataTestID.ALERT_ERROR)
        
        # Extract the text (label) of the error message from the notification element.
        error_message = get_label_of_element(element=error_message_notification)
        
        # Attach the extracted error message to the logs for reporting purposes.
        attach_text(error_message, name="Error message:")
        
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
def login_wt(driver, server: Server, device_type: Platform = Platform.DESKTOP, env_type: EnvironmentType = EnvironmentType.UAT,
             account_type: AccountType = AccountType.LIVE,
             testcase_id: str = None, set_language: bool = False, set_username: bool = True, 
             expectation: LoginResultState = LoginResultState.SUCCESS, 
             credential_type: CredentialType = CredentialType.DEFAULT) -> tuple[str, str] | None:
    """
    This function performs the complete login process to the WebTrader platform (WT).
    It launches the platform, selects the account type (Crm/Live/Demo), and logs into the member's site 
    using the provided credentials. It handles both successful and failure scenarios as specified.

    Arguments:
    - account_type: The type of account to select (e.g., 'crm', 'live', 'demo').
    - server: The server to use for login (e.g., 'MT4', 'MT5').
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
        params_wt_url = launch_wt(driver, server, device_type, env_type)

        # Step 2: Select the desired account type (either CRM / Live or Demo) for login.
        select_account_type(driver, account_type)
        
        # Select and verify language if required
        selected_language = None
        if set_language:
            selected_language = select_and_verify_language(driver)
            print("selected language", selected_language)
        else:
            select_english_language(driver)
            
        # Step 3: Perform the login action using the `wt_user_login` function. 
        # This handles credential retrieval, entry into the login form, and the actual login process.
        if set_username:
            username, password = wt_user_login(driver, server, testcase_id, selected_language, expectation, credential_type)
            return params_wt_url, username, password
    
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""