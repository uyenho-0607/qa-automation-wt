import re
import random
import pyperclip
import pandas as pd

from faker import Faker
from tabulate import tabulate
from difflib import get_close_matches
 
from constants.helper.screenshot import attach_text
from constants.helper.driver import delay, get_current_url
from constants.helper.error_handler import handle_exception
from constants.helper.element import spinner_element, clear_input_field, click_element, find_element_by_testid, find_element_by_xpath, find_list_of_elements_by_xpath, find_list_of_elements_by_testid, populate_element, trigger_click, visibility_of_element_by_testid, get_label_of_element, wait_for_text_to_be_present_in_element_by_testid

from common.desktop.module_setting.utils import button_setting, capture_alert
from common.desktop.module_announcement.utils import modal_announcement
from common.desktop.module_trade.order_panel.utils import extract_order_data_details
from common.desktop.module_markets.markets import verify_no_orders_in_my_trades


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                RANDOM GENERATE NAME / EMAIL / PHONE NUMBER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def generate_random_name_and_email():
    """
    Generates a random full name and email address using the Faker library.
    
    Returns: 
    - Tuple containing a random full name and email address
    """
    fake = Faker()
    # Generate a random full name
    full_name = fake.name()
    # Generate a random email address using the name
    email = fake.email()
    return full_name, email


def generate_singapore_phone_number():
    """
    Generates a random Singapore phone number (mobile) with a valid prefix (either 8 or 9).
    
    Returns:
    - A random 8-digit Singapore phone number as a string
    """
    # Prefix for Singapore mobile numbers (8 or 9)
    prefix = random.choice(['8', '9'])
    
    # Generate the remaining 7 digits of the phone number
    number = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    
    # Return the full 8-digit phone number
    return prefix + number

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                OPEN DEMO ACCOUNT ERROR MESSAGE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def open_demo_account_error_msg(driver, setting: bool = False):
    try:
        # Open the demo account settings if the setting flag is True
        if setting:
            button_setting(driver, setting_option="open-demo-account")
        else:
            demo_button = find_element_by_testid(driver, data_testid="login-account-signup")
            click_element(element=demo_button)

        # Click the "Next" button to proceed
        btn_next = find_element_by_testid(driver, data_testid="demo-account-creation-modal-confirm")
        click_element(element=btn_next)

        # Retrieve error messages
        error_msgs = find_list_of_elements_by_testid(driver, data_testid="input-field-validation")
        error_msgs_content = [get_label_of_element(msg).strip() for msg in error_msgs]

        # Expected error messages
        expected_msgs = [
            "Name is required",
            "Phone number is required",
            "Deposit is required",
            "Please review and accept the Terms and Conditions"
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

def open_demo_account_screen(driver, new_password=None, confirm_password=None, setting: bool = False, set_close_modal: bool = False, user_email: str = None):
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

        # If the setting flag is True, open the demo account settings via the settings button
        if setting:
            button_setting(driver, setting_option="open-demo-account")
        else:
            demo_button = find_element_by_testid(driver, data_testid="login-account-signup")
            click_element(element=demo_button)
        
        """ Name field """
        # Generate a random name for the demo account if not provided
        random_name, _ = generate_random_name_and_email()
        # Fill in the Name field with the generated name
        name_input = find_element_by_testid(driver, data_testid="demo-account-creation-modal-name")
        clear_input_field(element=name_input) # Clear any pre-filled value
        populate_element(element=name_input, text=random_name)  # Populate the input field with the random name

        """ Email field """
        # Use the provided email or generate a random one
        email_to_use = user_email if user_email else generate_random_name_and_email()[1]
        
        # Fill in the Email field        
        email_input = find_element_by_testid(driver, data_testid="demo-account-creation-modal-email")
        populate_element(element=email_input, text=email_to_use)  # Populate the input field with the email

        """ Phone Number field """
        # Handle the Phone Number field
        dialCode = find_element_by_xpath(driver, "//div[@class='sc-1ks0xwr-0 fSgSbd']")
        # dialCode = find_element_by_testid(driver, data_testid="country-dial-code-dropdown")
        click_element(element=dialCode) # Open the dial code dropdown
        
        # Wait for the dial code modal to appear
        visibility_of_element_by_testid(driver, data_testid="country-dial-code-dropdown")
        
        # Search for and select 'Singapore' from the dial code options
        dialCode_search = find_element_by_testid(driver, data_testid="country-dial-code-search")
        populate_element(element=dialCode_search, text="Singapore")
        
        # Select the Singapore dial code option
        dialCode_dropdown = find_element_by_testid(driver, data_testid="country-dial-code-item")
        click_element(element=dialCode_dropdown)
                
        # Generate a random Singapore phone number
        phone_number = generate_singapore_phone_number()
        # Populate the phone number input field with the generated phone number
        phoneNumber_input = find_element_by_testid(driver, data_testid="demo-account-creation-modal-phone")
        populate_element(element=phoneNumber_input, text=phone_number)
        
        """ Deposit field """
        # Handle the Deposit field
        deposit = find_element_by_xpath(driver, "(//div[@class='sc-9dltft-0 cOIzTG'][4]//div)[2]")
        click_element(element=deposit) # Open the deposit dropdown
                
        # Wait for all deposit options to appear
        deposit_options = find_list_of_elements_by_testid(driver, data_testid="deposit-dropdown-item")
        # Select a random deposit option from the dropdown
        random_deposit_option = random.choice(deposit_options)

        # Click the randomly selected deposit option
        click_element(element=random_deposit_option)
        
        """ Checkbox field """
        # Handle the checkbox field (for terms or other agreements)
        checkbox = find_element_by_xpath(driver, "//div[@data-testid='demo-account-creation-modal-agreement-unchecked']/div")
        click_element(element=checkbox)

        # Click the "Next" button to proceed
        btn_next = find_element_by_testid(driver, data_testid="demo-account-creation-modal-confirm")
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
        btn_copied = find_element_by_xpath(driver, "//span[@class='sc-zee84o-2 ivLbxM']")
        click_element(element=btn_copied)

        # Wait for snackbar message and extract header & description
        visibility_of_element_by_testid(driver, "notification-box")
        message_header = visibility_of_element_by_testid(driver, "notification-title")
        extracted_header = get_label_of_element(element=message_header)
        
        label_message_description = find_element_by_testid(driver, "notification-description")
        label_message = get_label_of_element(element=label_message_description)
        attach_text(label_message, name="Description_Message")
        
        # Validate message header
        if extracted_header != "Success":
            raise AssertionError(f"Invalid message header: {extracted_header}, Message: {label_message}")
        
        # Close the notification
        btn_close = find_element_by_testid(driver, data_testid="notification-close-button")
        trigger_click(driver, element=btn_close)
        
        # Get and validate clipboard content
        clipboard_text = pyperclip.paste().strip()

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
        
        # Retrieve the account details label
        demo_account_details = find_list_of_elements_by_xpath(driver, "//div[@class='sc-zee84o-4 hXfwHX']")
        if demo_account_details:
            formatted_text = []
            for element in demo_account_details:
                text = get_label_of_element(element)
                formatted_text.append(" ".join(text.split("\n")))  # Remove newlines and join words
            final_result = "\n".join(formatted_text)  # Join all elements into a single string
            
        if clipboard_text != final_result:
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
        match = wait_for_text_to_be_present_in_element_by_testid(driver, data_testid="demo-account-completion-modal-title", text="Your Demo Account is Ready!")
        if not match:
            raise AssertionError("Expected to redirect to 'Your Demo Account is Ready!' modal")

        # Retrieve header labels and map them
        header_elements = find_list_of_elements_by_testid(driver, data_testid="demo-completion-label")
        header_labels = [header_mapping.get(element.text, element.text) for element in header_elements]
        header_labels.append("Currency")  # For handling Deposit currency

        # Initialize a dictionary to store demo account details
        demo_account_details = {label: "N/A" for label in header_labels}

        # Retrieve account detail values from the page
        demoAccount_elements = find_list_of_elements_by_testid(driver, data_testid="demo-completion-value")

        # Iterate through account details and populate the dictionary
        for idx, element in enumerate(demoAccount_elements):
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
        demo_account_info = extract_order_data_details(driver, [list(demo_account_details.values())], list(demo_account_details.keys()), section_name="Your Demo Account is Ready!")

        # Convert the data into a grid format for the report
        overall = tabulate(demo_account_info.set_index("Section").T.fillna("-"), headers="keys", tablefmt="grid", stralign="center")
        attach_text(overall, name="Your Demo Account is Ready!")

        # Check the URL before closing the modal
        initial_url = get_current_url(driver)

        # Handle modal dialog based on `set_close` flag
        if set_close:
            get_copied_banner(driver)

            # if text == demo_account_info
            modal_close = find_element_by_xpath(driver, "//div[@class='sc-1dvc755-6 hyBcLN']//*[name()='svg']")
            click_element(modal_close)
            
            # Verify the URL after closing the modal
            final_url = get_current_url(driver)

            if initial_url != final_url:
                raise AssertionError("Page URL changed unexpectedly after closing the modal.")
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

def handle_sign_in(driver, demo_account_details, new_password, confirm_password):
    """
    Handles the sign-in process after demo account creation.

    Arguments:
    - demo_account_details: A dictionary containing the demo account details, including username and password.
    - new_password: The new password to set.
    - confirm_password: Confirmation of the new password.
    """
    try:
        # Find and click the 'Sign In' button to navigate to the login page from the modal dialog
        sign_in_button = find_element_by_xpath(driver, "//div[@class='sc-1dvc755-5 eugaOX']/button")
        click_element(sign_in_button)

        # Wait for a brief moment to ensure the page has time to load
        delay(0.5)

        # Get the current URL after clicking the 'Sign In' button
        current_url = get_current_url(driver)

        # Ensure that the URL contains 'web/login' (indicating that we are on the login page)
        if "web/login" not in current_url:
            raise AssertionError(f"Redirected to {current_url}, expected to be on the login page.")

        # Validate the login username by checking if it matches the demo account username
        username_input = find_element_by_testid(driver, data_testid="login-user-id")
        assert username_input.get_attribute("value") == demo_account_details["LoginID"], "Username mismatch"

        # Validate the login password by checking if it matches the demo account password
        password_input = find_element_by_testid(driver, data_testid="login-password")
        assert password_input.get_attribute("value") == demo_account_details["Password"], "Password mismatch"

        # Find and click the 'Submit' button to proceed with the login
        submit_button = find_element_by_testid(driver, data_testid="login-submit")
        click_element(submit_button)

        delay(2)
        
        # Check if an announcement modal is present and handle it
        modal_announcement(driver)

        # Validate that the account details are correct after logging in
        validate_account_details(driver, demo_account_details)
        
        verify_no_orders_in_my_trades(driver)

        # Handle the password change process if necessary
        handle_changePassword(driver, demo_account_details, new_password, confirm_password)

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
    wait_for_text_to_be_present_in_element_by_testid(driver, data_testid="account-type-tag", text="DEMO")

    # Validate the Account Name displayed matches the expected value from demo_account_details
    account_name = get_label_of_element(find_element_by_testid(driver, data_testid="account-name"))    
    assert account_name == demo_account_details["Account Name"], "Account name mismatch"

    # Validate the LoginID (Trader ID) displayed matches the expected value from demo_account_details
    trader_id = get_label_of_element(find_element_by_testid(driver, data_testid="account-id"))
    assert trader_id == demo_account_details["LoginID"], "LoginID mismatch"

    # Validate the USD / Leverage information
    usd_leverage = get_label_of_element(find_element_by_testid(driver, data_testid="account-detail"))
    match = re.search(r"(\w+)\s*\|\s*([\d:]+)", usd_leverage)
    assert match.group(1) == demo_account_details["Currency"], f"Currency mismatch. Expected {demo_account_details["Currency"]} but found {match.group(1)}"
    assert match.group(2) == demo_account_details["Leverage"], f"Leverage mismatch. Expected {demo_account_details["Leverage"]} but found {match.group(2)}"

    # Validate the Account Balance displayed matches the expected value from demo_account_details
    account_balance = get_label_of_element(find_element_by_xpath(driver, "(//div[@class='sc-11khvbe-3 jKLIbO'])[1]//div[@class='sc-11khvbe-5 doTcw']"))
    # Extract the numerical value of the account balance from the displayed text using regex
    balance_value = re.search(r'\$(\d{1,3}(?:,\d{3})*)', account_balance).group(1)
    assert balance_value == demo_account_details["Deposit"], "Account balance mismatch"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CHANGE NEWLY CREATED DEMO ACCOUNT PASSWORD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_changePassword(driver, demo_account_details, new_password, confirm_password):

    # Step 1: Navigate to the Change Password section
    button_setting(driver, setting_option="change-password")
    
    # Locate and populate the old password input field
    old_password_input = find_element_by_testid(driver, data_testid="change-password-modal-old-password")
    populate_element(element=old_password_input, text=demo_account_details["Password"])

    # Locate and populate the new password input field
    new_password_input = find_element_by_testid(driver, data_testid="change-password-modal-new-password")
    populate_element(element=new_password_input, text=new_password)

    # Locate and populate the confirm password input field
    confirm_password_input = find_element_by_testid(driver, data_testid="change-password-modal-confirm-new-password")
    populate_element(element=confirm_password_input, text=confirm_password)

    # Find the submit button and click it
    submit_button = find_element_by_testid(driver, data_testid="change-password-modal-confirm")
    click_element(element=submit_button)

    alert_message, actual_alert_type = capture_alert(driver)

    # Handle different types of alerts
    if actual_alert_type == "success":
        # Extract the label/message from the alert
        label_message = get_label_of_element(alert_message)
    
        # If the success message indicates a password change, process it
        if "Account password has been updated successfully" in label_message:
            attach_text(label_message, name="Success message found:")
            
            # Log the user out
            button_setting(driver, setting_option="logout")
            
        else:
            # If the success message doesn't match, handle it as an unexpected message
            assert False, f"Unexpected success message: {label_message}"
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""