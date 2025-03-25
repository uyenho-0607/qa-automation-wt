import re
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from constants.element_ids import DataTestID
from constants.helper.error_handler import handle_exception
from constants.helper.driver import access_url, delay, get_current_url
from constants.helper.element import spinner_element, is_element_present_by_testid, click_element, populate_element, find_element_by_testid, find_list_of_elements_by_testid, trigger_click, find_visible_element_by_testid, get_label_of_element, wait_for_text_to_be_present_in_element_by_testid

from common.desktop.module_login.utils import handle_alert_error
from common.desktop.module_setting.utils import button_setting
from common.desktop.module_setting.setting_change_pwd import perform_login
from common.desktop.module_setting.setting_general import accountInformation

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NOTIFICATION BANNER - SWITCH ACCOUNT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_account_banner(driver):
    try:
        
        spinner_element(driver)
            
        valid_message_headers = ["Account Switched"]

        # Wait for the snackbar message to be visible
        find_visible_element_by_testid(driver, data_testid=DataTestID.NOTIFICATION_BOX.value)
        
        # Wait for the message header to be visible and extract it
        message_header = find_visible_element_by_testid(driver, data_testid=DataTestID.NOTIFICATION_TITLE.value)
        extracted_header = get_label_of_element(message_header)

        # Extract the message description
        label_message_description = find_element_by_testid(driver, data_testid=DataTestID.NOTIFICATION_DESCRIPTION.value)
        label_message = get_label_of_element(label_message_description)

        # Check if the header is valid
        if extracted_header not in valid_message_headers:
            raise AssertionError(f"Invalid message header: {extracted_header}, Message description: {label_message}")
        
        accountID = re.search(r'Account ID:\s*(\d+)', label_message).group(1)
        print("accountID", accountID)
        
        btn_close = find_element_by_testid(driver, data_testid=DataTestID.NOTIFICATION_CLOSE_BUTTON.value)
        trigger_click(driver, element=btn_close)

        # Retrieve the MetaTrader ID
        traderID = find_element_by_testid(driver, data_testid=DataTestID.ACCOUNT_ID.value)
        label_traderID = get_label_of_element(traderID)
        
        assert accountID == label_traderID, f"AccountID does not match. Expected to display {accountID}"
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


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
            testid = DataTestID.TAB_LOGIN_ACCOUNT_TYPE_DEMO.value # Test ID for the demo account tab
        elif account_type == "live":
            setting_option = "switch-to-live" # Button to switch to the live account
            expected_label = "Live Account" # Expected label for live account
            testid = DataTestID.TAB_LOGIN_ACCOUNT_TYPE_LIVE.value # Test ID for the live account tab
        else:
            # Raise an error if the provided account type is invalid
            raise ValueError("Invalid account type. Must be either 'demo' or 'live'.")

        # Click on the appropriate button to switch the account type
        button_setting(driver, setting_option=setting_option)
        
        # Wait for the account selector element to be visible and obtain it
        account_selector = find_visible_element_by_testid(driver, data_testid=testid)
        
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
    account_id_element = find_element_by_testid(driver, data_testid=DataTestID.LINK_SWITCH_CONFIRMATION_MODAL_DESCRIPTION.value)
    retrieved_account_id = get_label_of_element(account_id_element).strip()
    label_account_id = re.search(r'Account ID:\s*(\d+)', retrieved_account_id).group(1)
    return label_account_id


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                LINK ACCOUNT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_success(driver, account_id: str, expect_failure: bool):
    if expect_failure:
        assert False, "Expected failure, but successfully linked account"

    label_account_id = retrieve_accountID(driver)
    assert account_id == label_account_id, "Account ID does not match"
    print("Linked Account ID:", label_account_id)
    
    # Click on the "Close button"
    btn_close = find_element_by_testid(driver, data_testid=DataTestID.LINK_SWITCH_CONFIRMATION_MODAL_CONFIRM.value)
    click_element(btn_close)
    
    delay(1)

    accountInformation(driver)
    
    # Ensure account_id exists in the account list
    account_list = find_list_of_elements_by_testid(driver, data_testid=DataTestID.ACCOUNT_OPTION_DETAIL.value)
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
        live_account = find_element_by_testid(driver, data_testid=DataTestID.ADD_ACCOUNT.value)
        click_element(element=live_account)
        
        # Wait for it to be visible
        wait_for_text_to_be_present_in_element_by_testid(driver, data_testid=DataTestID.LINK_ACCOUNT_MODAL_TITLE.value, text="Link Another Account")
        
        # Find and populate the accountID and password input field
        accountID_input = find_element_by_testid(driver, data_testid=DataTestID.LINK_ACCOUNT_MODAL_ACCOUNT_ID.value)
        populate_element(element=accountID_input, text=account_id)
        
        accountID_input = find_element_by_testid(driver, data_testid=DataTestID.LINK_ACCOUNT_MODAL_PASSWORD.value)
        populate_element(element=accountID_input, text=accountPassword)

        # Confirm and handle result
        btn_confirm = find_element_by_testid(driver, data_testid=DataTestID.LINK_ACCOUNT_MODAL_CONFIRM.value)
        click_element(element=btn_confirm)
        
        if wait_for_text_to_be_present_in_element_by_testid(driver, data_testid=DataTestID.LINK_SWITCH_CONFIRMATION_MODAL_TITLE.value, text="Successfully Linked"):
            handle_success(driver, account_id, expect_failure)
        else:
            handle_alert_error(driver, expect_failure)

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
        


def switch_or_delete_account(driver, option: str, login_password=None, params_wt_url=None, set_confirmBtn: bool = True, expect_failure: bool = False):
    """
    This function allows switching or deleting an account in the WebTrader platform.
    It locates the account list, selects an account (excluding the first one), and performs the specified action ('switch' or 'delete').

    Arguments:
    - option: The action to perform ('switch' or 'delete').
    - login_password: (Optional) The password required for logging back in after deletion.
    - params_wt_url: (Optional) The WebTrader URL for re-login after deletion.

    Returns:
    - None: The function does not return anything. It performs the specified action on the account.

    Raises:
    - ValueError: If an invalid option is provided.
    """

    try:
        # Open the "Account Information" tab
        accountInformation(driver)
        
        # Locate all available accounts (excluding the first one)
        account_list = find_list_of_elements_by_testid(driver, data_testid=DataTestID.ACCOUNT_OPTION_ITEM.value)
        hoverable_accounts = account_list[1:]  # Exclude the first account
        
        # Randomly select an account from the available list
        selected_account = random.choice(hoverable_accounts)
        
        # Extract the account ID from the selected account element
        account_id_from_list = get_label_of_element(selected_account).strip()
        label_accountID = re.search(r'(\d+)(?=\s?\()', account_id_from_list).group(0)
        
        # Hover over the selected account to reveal action buttons
        ActionChains(driver).move_to_element(selected_account).perform()
        
        # Define action properties for switch and delete
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
        
        # Perform the action if the option is valid
        if option in actions:
            action = actions[option]
            
            # Locate and click the corresponding action button (Switch/Delete)
            button = selected_account.find_element(By.XPATH, action["button_xpath"])
            click_element(element=button)
            
            # Wait for the confirmation message to appear
            if wait_for_text_to_be_present_in_element_by_testid(driver, data_testid=DataTestID.LINK_SWITCH_CONFIRMATION_MODAL_TITLE.value, text=action['action_text']):
                # Retrieve the account ID displayed in the confirmation dialog
                label_account_id = retrieve_accountID(driver)
                
                # Ensure the account ID matches the selected one
                assert label_accountID == label_account_id, f"Account ID does not match for {action['action_type']}"
                print(f"{action['action_type']} Account ID:", label_account_id)
                
                # Close the confirmation dialog
                btn_confirm = find_element_by_testid(driver, data_testid=DataTestID.LINK_SWITCH_CONFIRMATION_MODAL_CONFIRM.value)
                click_element(btn_confirm)
                
        else:
            # Raise an assertion error for invalid option inputs
            assert False, f"Invalid option name: '{option}'"
        
        # Handle additional steps based on the selected action
        if option == "switch":
            handle_password_prompt_on_account_switch(driver, set_confirmBtn, expect_failure)
            
        elif option == "delete":
            # Wait for the success message after account deletion
            if wait_for_text_to_be_present_in_element_by_testid(driver, data_testid=DataTestID.LINK_SWITCH_CONFIRMATION_MODAL_TITLE.value, text="Successfully remove account"):
                # Retrieve the account ID after deletion confirmation
                label_account_id = retrieve_accountID(driver)
                assert label_accountID == label_account_id, "Account ID does not match"
                
                # Close the success dialog
                btn_confirm = find_element_by_testid(driver, data_testid=DataTestID.LINK_SWITCH_CONFIRMATION_MODAL_CONFIRM.value)
                click_element(btn_confirm)
                
                # Print success message
                print(f"Successfully deleted {label_accountID} account.")
                
                # Navigate to logout after deletion
                button_setting(driver, setting_option="logout")
                
                # Get the current URL after logout
                current_url = get_current_url(driver)
                
                # If redirected to login page, log in again
                if "web/login" in current_url:
                    perform_login(driver, label_account_id, login_password)
                else:
                    print("checking if it move in")
                    # If not redirected, manually access the target URL and log in
                    access_url(driver, url=params_wt_url)
                    perform_login(driver, label_account_id, login_password)
                
                # Ensure only one account is displayed after re-login
                verify_single_account_displayed(driver)
        
    except Exception as e:
        # Handle exceptions and errors that occur during execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def verify_single_account_displayed(driver):
    """
    Ensures that only one account is displayed after opening the dropdown.

    :param driver: Selenium WebDriver instance.
    :param dropdown_selector: CSS selector for the account dropdown.
    :param account_item_selector: CSS selector for the account list items.
    :return: The name of the displayed account if only one is found, otherwise raises an assertion error.
    """

    # Locate the "Account Information" tab
    accountInformation(driver)
    
    # Ensure account_id exists in the account list
    accounts = find_list_of_elements_by_testid(driver, data_testid=DataTestID.ACCOUNT_OPTION_ITEM.value)

    # Extract only visible accounts
    visible_accounts = [acc.text for acc in accounts if acc.is_displayed()]

    # Ensure only one account is displayed
    assert len(visible_accounts) == 1, f"Expected 1 account, but found {len(visible_accounts)}: {visible_accounts}"

    print(f"Only one account is displayed: {visible_accounts[0]}")
    return visible_accounts[0]

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_password_prompt_on_account_switch(driver, set_confirmBtn: bool = True, expect_failure: bool = False):
    try:

        if wait_for_text_to_be_present_in_element_by_testid(driver, data_testid=DataTestID.LINK_ACCOUNT_MODAL_TITLE.value, text="Please re-enter your password"):
            
            # Locate the input field where the take profit value is displayed
            accountID = find_element_by_testid(driver, data_testid=DataTestID.LINK_ACCOUNT_MODAL_ACCOUNT_ID.value)
            # Determine the initial value and the increment based on the value type (price or points)
            accountID_value = accountID.get_attribute("value")
            print(accountID_value)
            
            password = find_element_by_testid(driver, data_testid=DataTestID.LINK_ACCOUNT_MODAL_PASSWORD.value)
            populate_element(element=password, text="Asd123")
            
            if set_confirmBtn:
                # Confirm and handle result
                btn_confirm = find_element_by_testid(driver, data_testid=DataTestID.LINK_ACCOUNT_MODAL_CONFIRM.value)
                click_element(element=btn_confirm)
                
                # Wait a moment to check for an error or success response
                if is_element_present_by_testid(driver, data_testid=DataTestID.ALERT_ERROR.value):
                    handle_alert_error(driver, expect_failure)
                else:
                    get_account_banner(driver)
            else:
                # Close the action dialog
                btn_close = find_element_by_testid(driver, data_testid=DataTestID.LINK_ACCOUNT_MODAL_CLOSE.value)
                click_element(btn_close)
        else:
            # Get the success message for switch account
            get_account_banner(driver)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""