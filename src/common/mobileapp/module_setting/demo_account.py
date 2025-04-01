
import random
import re

from tabulate import tabulate
from difflib import get_close_matches

from enums.main import Menu, Setting
from constants.element_ids import DataTestID
from constants.helper.driver import delay
from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element_android_app import clear_input_field, click_element, find_element_by_testid, find_element_by_xpath, find_list_of_elements_by_xpath, get_label_of_element, populate_element, find_presence_element_by_testid, spinner_element, find_visible_element_by_testid, find_visible_element_by_xpath, find_element_by_testid_with_wait, find_element_by_xpath_with_wait, wait_for_text_to_be_present_in_element_by_xpath

from common.mobileapp.module_sub_menu.sub_menu import menu_button
from common.mobileapp.module_setting.utils import button_setting
from common.mobileapp.module_announcement.announcement import modal_announcement
from common.mobileapp.module_trade.order_panel.op_general import extract_order_data_details
from data_config.generate_dummy_data import generate_random_name_and_email, generate_singapore_phone_number, generate_random_credential


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                OPEN DEMO ACCOUNT ERROR MESSAGE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def open_demo_account_error_msg(driver, setting: bool = False):
    
    try:
        # Open the demo account settings if the setting flag is True
        if setting:
            button_setting(driver, setting_option=Setting.OPEN_DEMO_ACCOUNT)
        else:
            demo_button = find_element_by_xpath_with_wait(driver, DataTestID.APP_OPEN_DEMO_ACCOUNT)
            click_element(element=demo_button)
            
        # Click the "Next" button to proceed
        btn_next = find_element_by_xpath_with_wait(driver, DataTestID.APP_DEMO_ACCOUNT_CREATION_AGREE_CONTINUE)
        click_element(element=btn_next)

        # Retrieve error messages
        error_msgs = find_list_of_elements_by_xpath(driver, DataTestID.APP_DEMO_ACCOUNT_ERROR_CHECK)
        error_msgs_content = [get_label_of_element(msg).strip() for msg in error_msgs]

        # Expected error messages
        expected_msgs = [
            "Name is required",
            "Email is required",
            "Dial code is required",
            "Phone number is required"
        ]

        # Check and log each error message
        for expected_msg in expected_msgs:
            matching_msgs = [msg for msg in error_msgs_content if msg == expected_msg]
            if matching_msgs:
                print(f"Correct Error Message Retrieved: {expected_msg}")
            else:
                # Find close matches for debugging purposes
                close_matches = get_close_matches(expected_msg, error_msgs_content)
                if close_matches:
                    print(f"Expected: '{expected_msg}', but retrieved similar message(s): {close_matches}")
                else:
                    retrieved_msgs = ', '.join(error_msgs_content) if error_msgs_content else "No messages retrieved"
                    assert False, f"Expected: '{expected_msg}', but no matching messages. Retrieved: {retrieved_msgs}"

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                OPEN A DEMO ACCOUNT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def open_demo_account_screen(driver, new_password=None, confirm_password=None, setting: bool = False, set_close_modal: bool = False):
    """
    Opens a demo account by filling in necessary details such as name, email, phone number, deposit, and checkbox.
     - Handles account creation and optionally closes the modal dialog or proceeds with further steps.

    Arguments:
    - setting: Boolean flag to trigger the opening of the demo account from a setting option (default is False).
    - set_close_modal: Boolean flag to close the demo account modal after account creation (default is False).
    - user_email: Optional custom email address to use for the demo account (default is None, meaning a random email will be generated).

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:

        # Open the demo account settings if the setting flag is True
        if setting:
            button_setting(driver, setting_option=Setting.OPEN_DEMO_ACCOUNT)
        else:
            demo_button = find_element_by_xpath_with_wait(driver, DataTestID.APP_OPEN_DEMO_ACCOUNT)
            click_element(element=demo_button)
        
        """ Name field """
        # Generate a random name for the demo account if not provided
        _, first_name, _, email = generate_random_name_and_email()
        # Fill in the Name field with the generated name
        input_name = find_visible_element_by_xpath(driver, DataTestID.APP_DEMO_ACCOUNT_CREATION_MODAL_NAME)
        clear_input_field(element=input_name) # Clear any pre-filled value
        populate_element(element=input_name, text=first_name)  # Populate the input field with the random name

        """ Email field """
        # Fill in the Email field        
        input_email = find_visible_element_by_xpath(driver, DataTestID.APP_DEMO_ACCOUNT_CREATION_MODAL_EMAIL)
        populate_element(element=input_email, text=email)  # Populate the input field with the email

        """ Phone Number field """
        # Handle the Phone Number field
        dial_code = find_visible_element_by_xpath(driver, DataTestID.APP_DEMO_ACCOUNT_CREATION_MODAL_COUNTRY_DIAL_CODE)
        click_element(element=dial_code) # Open the dial code dropdown
                
        # Search for and select 'Singapore' from the dial code options
        dial_code_search = find_visible_element_by_xpath(driver, DataTestID.APP_DEMO_ACCOUNT_CREATION_MODAL_COUNTRY_DIAL_CODE_SEARCH)
        populate_element(element=dial_code_search, text="Singapore")

        delay(1)

        # Select the Singapore dial code option
        dial_code_dropdown = find_element_by_xpath_with_wait(driver, DataTestID.APP_DEMO_ACCOUNT_CREATION_MODAL_COUNTRY_DIAL_CODE_ITEM)
        click_element(element=dial_code_dropdown)
                
        # Generate a random Singapore phone number
        phone_number = generate_singapore_phone_number()
        # Populate the phone number input field with the generated phone number
        input_phone_number = find_visible_element_by_xpath(driver, DataTestID.APP_DEMO_ACCOUNT_CREATION_PHONE_NUMBER)
        populate_element(element=input_phone_number, text=phone_number)
        
        """ Deposit field """
        # Handle the Deposit field
        deposit = find_visible_element_by_xpath(driver, DataTestID.APP_DEMO_ACCOUNT_CREATION_DEPOSIT_AMT)
        click_element(element=deposit) # Open the deposit dropdown

        delay(1)

        # Wait for all deposit options to appear
        deposit_options = find_list_of_elements_by_xpath(driver, DataTestID.APP_DEMO_ACCOUNT_CREATION_DEPOSIT_AMT_OPTIONS)
        # Select a random deposit option from the dropdown
        random_deposit_option = random.choice(deposit_options)
        
        # Click the randomly selected deposit option
        click_element(element=random_deposit_option)

        # Click the "Next" button to proceed
        btn_next = find_element_by_xpath_with_wait(driver, DataTestID.APP_DEMO_ACCOUNT_CREATION_AGREE_CONTINUE)
        click_element(element=btn_next)

        # Handle the demo account ready screen (either close the modal or proceed to sign-in)
        demo_account_ready_screen(driver, new_password, confirm_password, set_close_modal)
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""




"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                COPIED PASTE FUNCTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_copied_banner(driver):
    """
    Extracts the snackbar trade notification message, processes its content,
    and returns a structured DataFrame with order details.

    Returns:
    - pd.DataFrame: A DataFrame containing the extracted trade details from the snackbar banner.
    
    Raises:
    - AssertionError: If an invalid message header is found or clipboard content does not match the expected format.
    """
    try:
        # Click the "Copy" button
        btn_copied = find_element_by_xpath(driver, DataTestID.APP_DEMO_ACCOUNT_COMPLETION_COPIED)
        click_element(element=btn_copied)
        
        # Wait for snackbar message and extract header & description
        find_visible_element_by_testid(driver, data_testid=DataTestID.NOTIFICATION_BOX)
        
        # Retrieve the message
        label_message_description = find_element_by_testid(driver, data_testid=DataTestID.NOTIFICATION_BOX_DESCRIPTION)
        label_message = get_label_of_element(element=label_message_description)
        attach_text(label_message, name="Description_Message")
        
        # Close the notification
        btn_close = find_element_by_testid(driver, data_testid=DataTestID.NOTIFICATION_BOX_CLOSE)
        click_element(btn_close)
        
        # Get and validate clipboard content
        clipboard_text = driver.get_clipboard_text()

        pattern = (
            r"^Login:\s\d+\n"
            r"Password:\s[^\n]+\n"
            r"(?:View Only Password:\s[^\n]+\n)?"
            r"Name:\s.+\n"
            r"Leverage:\s\d+\s:\s\d+\n"
            r"Deposit:\s[\d,]+\sUSD$"
        )
        
        # Validate copied text
        if re.search(pattern, clipboard_text, re.MULTILINE):
            attach_text(clipboard_text, name="✅ Copied account creation details")
        else:
            raise AssertionError("❌ Copy function failed or incorrect format.")
                
    except Exception as e:
        handle_exception(driver, e)
     
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                DEMO ACCOUNT READY SCREEN
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def demo_account_ready_screen(driver, new_password=None, confirm_password=None, set_close: bool = False):
    """
    Handles the demo account creation confirmation screen. 
     - Extracts demo account details and either signs the user in or closes the modal based on `set_close` flag.

    Arguments:
    - driver: The Selenium WebDriver instance.
    - set_close: Boolean flag to determine if the modal should be closed after processing (default is False).

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Define a mapping for header labels to their corresponding fields
        header_mapping = {
            "Login:": "LoginID",
            "Password:": "Password",
            "View Only Password:": "View Only Password",
            "Name:": "Account Name",
            "Leverage:": "Leverage",
            "Deposit:": "Deposit",
        }

        # Wait for the modal dialog to appear
        spinner_element(driver)

        # Verify the presence of the "Your Demo Account is Ready!" message
        match = wait_for_text_to_be_present_in_element_by_xpath(driver, DataTestID.APP_DEMO_ACCOUNT_COMPLETION_TITLE, text="Your demo account has been opened successfully.")
        if not match:
            raise AssertionError("Expected to redirect to 'Your Demo Account is Ready!' modal")
        
        delay(2)
        
        # Retrieve header labels and map them
        header_elements = find_list_of_elements_by_xpath(driver, DataTestID.APP_DEMO_ACCOUNT_COMPLETION_LABEL)
        header_labels = [header_mapping.get(element.text, element.text) for element in header_elements]
        header_labels.append("Currency")  # For handling Deposit currency

        # Initialize a dictionary to store demo account details
        demo_account_details = {label: "N/A" for label in header_labels}

        # Retrieve account detail values from the page
        demo_account_elements = find_list_of_elements_by_xpath(driver, DataTestID.APP_DEMO_ACCOUNT_COMPLETION_VALUE)
        # Iterate through account details and populate the dictionary
        for idx, element in enumerate(demo_account_elements ):
            label = get_label_of_element(element).strip()

            # Handle Leverage (e.g., "1 : 5" to "1:5")
            if re.match(r'\d+\s:\s\d+', label): # Matches "X : Y" pattern
                label = label.replace(" ", "")  # Remove spaces, resulting in "X:Y"
                demo_account_details["Leverage"] = label

            match = re.search(r"([0-9,]+)\s([A-Za-z]+)", label)
            if match:
                demo_account_details["Deposit"] = match.group(1)
                demo_account_details["Currency"] = match.group(2)
            else:
                # Assign values to mapped labels dynamically
                demo_account_details[header_labels[idx]] = label

        # Tabulate and attach the demo account details to the report
        demo_account_info = extract_order_data_details(driver, list(demo_account_details.values()), list(demo_account_details.keys()), section_name="Your Demo Account is Ready!")
        print(demo_account_details)
        
        # Convert the data into a grid format for the report
        overall = tabulate(demo_account_info.set_index("Section").T.fillna("-"), headers="keys", tablefmt="grid", stralign="center")
        attach_text(overall, name="Your Demo Account is Ready!")

        # Check the URL before closing the modal
        wait_for_text_to_be_present_in_element_by_xpath(driver, DataTestID.APP_DEMO_ACCOUNT_COMPLETION_TITLE, text="Your demo account has been opened successfully.")

        # Handle modal dialog based on `set_close` flag
        if set_close:
            get_copied_banner(driver)
        else:
            handle_sign_in(driver, demo_account_details, new_password, confirm_password)

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                HANDLE SIGN IN VERIFICATION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_sign_in(driver, demo_account_details):
    """
    Handles the sign-in process after demo account creation.

    Arguments:
    - demo_account_details: A dictionary containing the demo account details, including username and password.
    - new_password: The new password to set.
    - confirm_password: Confirmation of the new password.
    """
    try:
        # Find and click the 'Sign In' button to navigate to the login page from the modal dialog
        sign_in_button = find_element_by_xpath(driver, DataTestID.APP_DEMO_ACCOUNT_COMPLETION_SIGN_IN)
        click_element(sign_in_button)

        # Wait for a brief moment to ensure the page has time to load
        delay(0.5)
        
        assert find_visible_element_by_xpath(driver, DataTestID.APP_LOGIN_LOGO)

        # Validate the login username by checking if it matches the demo account username
        userinput_name = find_element_by_testid(driver, data_testid=DataTestID.LOGIN_USER_ID)
        assert userinput_name.get_attribute("text") == demo_account_details["Login"], "Username mismatch"
        
        password_unmasked = find_element_by_xpath(driver, DataTestID.APP_LOGIN_PASSWORD_UNMASKED)
        click_element(element=password_unmasked)
        
        # Validate the login password by checking if it matches the demo account password
        password_input = find_element_by_testid(driver, data_testid=DataTestID.LOGIN_PASSWORD)
        assert password_input.get_attribute("text") == demo_account_details["Password"], "Password mismatch"

        # Find and click the 'Submit' button to proceed with the login
        submit_button = find_element_by_testid(driver, data_testid=DataTestID.LOGIN_SUBMIT)
        click_element(submit_button)

        delay(2)
        
        # Check if an announcement modal is present and handle it
        modal_announcement(driver)

        # Validate that the account details are correct after logging in
        validate_account_details(driver, demo_account_details)

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                VALIDATE ACCOUNT DETAILS UPON LOGIN
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def validate_account_details(driver, demo_account_details):
    """
    Validates account details after successful sign-in.

    Arguments:
    - demo_account_details: A list containing the demo account details (username, password, etc.) from the demo account ready screen
    """
    
    # Ensure that the "DEMO" text is displayed to confirm we're on the demo account
    wait_for_text_to_be_present_in_element_by_xpath(driver, DataTestID.APP_ACCOUNT_TYPE_TAG, text="DEMO")

    # Validate the Account Balance displayed matches the expected value from demo_account_details
    account_balance = get_label_of_element(find_element_by_xpath(driver, DataTestID.APP_ACCOUNT_BALANCE))
    # Extract the numerical value of the account balance from the displayed text using regex
    balance_value = re.search(r'\$(\d{1,3}(?:,\d{3})*)', account_balance).group(1)
    assert balance_value == demo_account_details["Deposit"], "Account balance mismatch"
    
    # Redirect to asset page
    menu_button(driver, menu=Menu.ASSETS)

    # Validate the Account Name displayed matches the expected value from demo_account_details
    account_name = get_label_of_element(find_visible_element_by_xpath(driver, DataTestID.APP_ACCOUNT_NAME))
    assert account_name == demo_account_details["Name"], f"Account name mismatch, {account_name}"

    # Validate the LoginID (Trader ID) displayed matches the expected value from demo_account_details
    trader_id = get_label_of_element(find_element_by_xpath(driver, DataTestID.APP_ACCOUNT_ID))
    assert trader_id == demo_account_details["Login"], "LoginID mismatch"

    # Validate the USD / Leverage information
    usd_leverage = get_label_of_element(find_element_by_xpath(driver, DataTestID.APP_ACCOUNT_DETAIL))
    match = re.search(r"(\w+)\s*\|\s*([\d:]+)", usd_leverage)
    assert match.group(1) == demo_account_details["Currency"], f"Currency mismatch. Expected {demo_account_details["Currency"]} but found {match.group(1)}"
    assert match.group(2) == demo_account_details["Leverage"], f"Leverage mismatch. Expected {demo_account_details["Leverage"]} but found {match.group(2)}"


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CHANGE NEWLY CREATED DEMO ACCOUNT PASSWORD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_changePassword(driver, demo_account_details):

    # Step 1: Navigate to the Change Password section
    button_setting(driver, setting_option=Setting.CHANGE_PASSWORD)
    
    credential = generate_random_credential(length=12)
    
    # Locate and populate the old password input field
    old_password_input = find_visible_element_by_xpath(driver, DataTestID.APP_CHANGE_PASSWORD_MODAL_OLD_PASSWORD)
    populate_element(element=old_password_input, text=demo_account_details["Password"])

    # Locate and populate the new password input field
    new_password_input = find_element_by_xpath(driver, DataTestID.APP_CHANGE_PASSWORD_MODAL_NEW_PASSWORD)
    populate_element(element=new_password_input, text=credential)

    # Locate and populate the confirm password input field
    confirm_password_input = find_element_by_xpath(driver, DataTestID.APP_CHANGE_PASSWORD_MODAL_CONFIRM_NEW_PASSWORD)
    populate_element(element=confirm_password_input, text=credential)

    # Find the submit button and click it
    submit_button = find_element_by_xpath(driver, DataTestID.APP_CHANGE_PASSWORD_MODAL_CONFIRM)
    click_element(element=submit_button)
    
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
        button_setting(driver, setting_option=Setting.LOGOUT)
        
    else:
        # If the success message doesn't match, handle it as an unexpected message
        assert False, f"Unexpected success message: {label_message}"
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""