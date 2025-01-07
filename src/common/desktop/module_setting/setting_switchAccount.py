import re
import random

from constants.helper.driver import delay, url_changes

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from constants.helper.error_handler import handle_exception
from constants.helper.element import javascript_click, click_element, populate_element, find_element_by_testid, find_element_by_xpath, find_list_of_elements_by_xpath, visibility_of_element_by_xpath, visibility_of_element_by_testid, get_label_of_element, wait_for_text_to_be_present_in_element_by_xpath

from common.desktop.module_login.utils import handle_login_error
from common.desktop.module_setting.utils import button_setting


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SWITCH TO LIVE / DEMO
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def switch_account_type(driver, account_type):
    """
    To switch between account types (Demo or Live) based on the provided account_type.

    Arguments:
    - account_type: The account type to switch to. Can be either 'demo' or 'live'.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Determine the setting option based on the provided account type ('demo' or 'live')
        if account_type == "demo":
            setting_option = "switch-to-demo" # Button to switch to the demo account
            expected_label = "Demo Account" # Expected label for demo account
            testid = "tab-login-account-type-demo" # Test ID for the demo account tab
        elif account_type == "live":
            setting_option = "switch-to-live" # Button to switch to the live account
            expected_label = "Live Account" # Expected label for live account
            testid = "tab-login-account-type-live" # Test ID for the live account tab
        else:
            # Raise an error if the provided account type is invalid
            raise ValueError("Invalid account type. Must be either 'demo' or 'live'.")

        # Click on the appropriate button to switch the account type
        button_setting(driver, setting_option=setting_option)
        
        # Wait for the account selector element to be visible and obtain it
        account_selector = visibility_of_element_by_testid(driver, data_testid=testid)
        
        # Extract the label or text of the currently selected account option
        selected_option = get_label_of_element(account_selector)
        
        # Assert that the selected account type matches the expected account label
        assert selected_option == expected_label, f"Expected '{expected_label}' to be selected, but found {selected_option}"

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def retrieve_accountID(driver):
    # Retrieve the account ID
    account_id_element = find_element_by_xpath(driver, "//div[@class='sc-ul53rt-5 bKNvWt']")
    retrieved_account_id = get_label_of_element(account_id_element).strip()
    label_account_id = re.search(r'Account ID:\s*(\d+)', retrieved_account_id).group(1)
    print("retrieve ", label_account_id)
    return label_account_id


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                LINK ACCOUNT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def accountInformation(driver):
    # To open the account linkage profile
    accountInfo = find_element_by_xpath(driver, "//div[@class='sc-ck4lnb-1 eqDuXz']")
    javascript_click(driver, element=accountInfo)
    

def handle_success(driver, account_id: str, expect_failure: bool):
    if expect_failure:
        assert False, "Expected failure, but successfully linked account"

    label_account_id = retrieve_accountID(driver)
    assert account_id == label_account_id, "Account ID does not match"
    print("Linked Account ID:", label_account_id)

    close_btn = find_element_by_xpath(driver, "//div[@class='sc-ul53rt-8 jViQlt']/button")
    click_element(close_btn)
    
    delay(1.5)

    accountInformation(driver)
        
    # Ensure account_id exists in the account list
    account_list = find_list_of_elements_by_xpath(driver, "//div[@class='sc-dm5c7m-2 bDlRDM']//div[@class='sc-3lrinj-4 jAWhNv']")
    
    account_ids = []
    for account in account_list:
        account_id_from_list = get_label_of_element(account).strip()
                
        # Remove "(x:y)" pattern from each string in the list
        result_list = re.sub(r"\s*\(\d+:\d+\)", "", account_id_from_list)
        account_ids.append(result_list)

    assert account_id in account_ids, f"Account ID {account_id} not found in the account list"


def link_account(driver, account_id: str, accountPassword: str, expect_failure: bool = False):
    try:
        
        # Locate the "Account Information" tab
        accountInformation(driver)

        # Locate and click the "Live Account" tab
        live_account = find_element_by_xpath(driver, "//span[contains(normalize-space(text()), 'Live Account')]")
        click_element(element=live_account)
        
        # Wait for it to be visible
        visibility_of_element_by_xpath(driver, "//div[@class='sc-ur24yu-1 eqxJBS']")

        # Find and populate the accountID and password input field
        accountID_input = find_element_by_xpath(driver, "//input[@class='sc-13osccp-0 cjlePd small sc-1ad9a8y-0 gZTbnE']")
        populate_element(element=accountID_input, text=account_id)
        
        accountID_input = find_element_by_xpath(driver, "//input[@type='password']")
        populate_element(element=accountID_input, text=accountPassword)

        # Confirm and handle result
        btn_save = find_element_by_xpath(driver, "//button[contains(normalize-space(text()), 'Confirm')]")
        click_element(element=btn_save)
        
        match = wait_for_text_to_be_present_in_element_by_xpath(driver, "//div[contains(normalize-space(text()), 'Successfully Linked')]", text="Successfully Linked")
        if match:
            handle_success(driver, account_id, expect_failure)
        else:
            handle_login_error(driver, expect_failure)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SWITCH OR DELETE ACCOUNT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def switch_or_delete_account(driver, option):
    try:
        # Locate the "Account Information" tab
        accountInformation(driver)

        # Ensure account_id exists in the account list
        account_list = find_list_of_elements_by_xpath(driver, "//div[@class='sc-dm5c7m-2 bDlRDM']/div")

        # Exclude the first account from the list
        hoverable_accounts = account_list[1:]
        
        # Randomly pick an account from the list excluding the first one
        selected_account = random.choice(hoverable_accounts)

        # Get the account ID from the selected account element
        account_id_from_list = get_label_of_element(selected_account).strip()

        # To extract the accountID (e.g. 188188888) from the list
        label_accountID = re.search(r'(\d+)(?=\s?\()', account_id_from_list).group(0)

        # Hover over the selected account
        ActionChains(driver).move_to_element(selected_account).perform()
        
        actions = {
            "switch": {
                "button_xpath": ".//div[@class='sc-3lrinj-0 iCMNHY hover-buttons']/img[1]",
                "action_text": "Switch Account?",
                "action_type": "Switch"
            },
            "delete": {
                "button_xpath": ".//div[@class='sc-3lrinj-0 iCMNHY hover-buttons']/img[2]",
                "action_text": "Remove Account?",
                "action_type": "Delete"
            }
        }
        
        if option in actions:
            action = actions[option]

            button = selected_account.find_element(By.XPATH, action["button_xpath"])
            # Click the button
            click_element(element=button)
            
            # Wait for the action confirmation message
            match = wait_for_text_to_be_present_in_element_by_xpath(driver, f"//div[contains(normalize-space(text()), '{action['action_text']}')]", text=action['action_text'])
            if match:
                label_account_id = retrieve_accountID(driver)
                assert label_accountID == label_account_id, f"Account ID does not match for {action['action_type']}"
                print(f"Linked Account ID ({action['action_type']}):", label_account_id)

                # Close the action dialog
                close_btn = find_element_by_xpath(driver, "//div[@class='sc-ul53rt-8 jViQlt']/button")
                click_element(close_btn)
            
                # Print the success message
                print(f"Hovered and found {option} button for an account.", label_accountID)
        else:
            assert False, f"Invalid option name: '{option}'"
        
        if option == "switch":
            get_account_banner(driver)
        elif option == "delete":
            match = wait_for_text_to_be_present_in_element_by_xpath(driver, f"//div[contains(normalize-space(text()), 'Successfully remove account')]", text="Successfully remove account")
            if match:
                # Retrieve the account ID
                label_account_id = retrieve_accountID(driver)
                assert label_accountID == label_account_id, f"Account ID does not match"

                # Close the action dialog
                close_btn = find_element_by_xpath(driver, "//div[@class='sc-ul53rt-8 jViQlt']/button")
                click_element(close_btn)
            
                # Print the success message
                print(f"Successfully deleted {label_accountID} account.")
        else:
            raise ValueError(f"Invalid option: {option} provided")

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NOTIFICATION BANNER - SWITCH ACCOUNT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_account_banner(driver):
    try:
            
        valid_message_headers = [
            "Account Switched"
        ]

        # Wait for the snackbar message to be visible
        visibility_of_element_by_testid(driver, data_testid="notification-box")
        
        # Wait for the message header to be visible and extract it
        message_header = visibility_of_element_by_testid(driver, data_testid="notification-title")
        extracted_header = get_label_of_element(message_header)

        # Extract the message description
        label_message_description = find_element_by_testid(driver, data_testid="notification-description")
        label_message = get_label_of_element(label_message_description)

        # Check if the header is valid
        if extracted_header not in valid_message_headers:
            raise AssertionError(f"Invalid message header: {extracted_header}, Message description: {label_message}")
        
        re.search(r'Account ID:\s*(\d+)', label_message).group(1)
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""