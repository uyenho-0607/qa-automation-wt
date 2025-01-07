import re
import random

from faker import Faker
from tabulate import tabulate

from constants.helper.screenshot import attach_text
from constants.helper.driver import delay, get_current_url
from constants.helper.error_handler import handle_exception
from constants.helper.element import spinner_element, clear_input_field, click_element, find_element_by_testid, find_element_by_xpath, find_list_of_elements_by_xpath, populate_element, visibility_of_element_by_xpath, get_label_of_element, wait_for_text_to_be_present_in_element_by_xpath

from common.desktop.module_setting.utils import button_setting
from common.desktop.module_announcement.utils import modal_announcement
from common.desktop.module_trade.order_panel.utils import extract_order_data_details


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
    
    Returns
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
                                                OPEN A DEMO ACCOUNT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def open_demo_account(driver, setting: bool = False, set_close: bool = False, user_email: str = None):
    """
    Opens a demo account by filling in necessary details such as name, email, phone number, deposit, and checkbox.
     - Handles account creation and optionally closes the modal dialog or proceeds with further steps.

    Arguments:
    - setting: Boolean flag to trigger the opening of the demo account from a setting option (default is False).
    - set_close: Boolean flag to close the demo account modal after account creation (default is False).
    - user_email: Optional custom email address to use for the demo account (default is None, meaning a random email will be generated).

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:

        # If the setting flag is True, open the demo account settings via the settings button
        if setting:
            button_setting(driver, setting_option="open-demo-account")
        
        """ Name field """
        # Generate a random name for the demo account if not provided
        random_name, _ = generate_random_name_and_email()
        # Fill in the Name field with the generated name
        name_input = find_element_by_xpath(driver, "(//div[@class='sc-9dltft-2 ifJKAm']/input)[1]")
        clear_input_field(element=name_input) # Clear any pre-filled value
        populate_element(element=name_input, text=random_name)  # Populate the input field with the random name

        """ Email field """        
        # Use the provided email or generate a random one
        email_to_use = user_email if user_email else generate_random_name_and_email()[1]
        
        # Fill in the Email field        
        email_input = find_element_by_xpath(driver, "(//div[@class='sc-9dltft-2 ifJKAm']/input)[2]")
        populate_element(element=email_input, text=email_to_use)  # Populate the input field with the email

        """ Phone Number field """
        # Handle the Phone Number field
        dialCode = find_element_by_xpath(driver, "//div[@class='sc-1ks0xwr-0 fSgSbd']")
        click_element(element=dialCode) # Open the dial code dropdown
        
        # Wait for the dial code modal to appear
        visibility_of_element_by_xpath(driver, "//div[@class='sc-189z816-0 bQWMaw']")
        
        # Search for and select 'Singapore' from the dial code options
        dialCode_search = find_element_by_xpath(driver, "//div[@class='sc-189z816-0 bQWMaw']//input")
        populate_element(element=dialCode_search, text="Singapore")
        
        # Select the Singapore dial code option
        dialCode_dropdown = find_element_by_xpath(driver, "//div[@class='sc-1ks0xwr-2 dcwmHB']/div")
        click_element(element=dialCode_dropdown)
                
        # Generate a random Singapore phone number
        phone_number = generate_singapore_phone_number()
        # Populate the phone number input field with the generated phone number
        phoneNumber_input = find_element_by_xpath(driver, "//div[@class='sc-9dltft-6 iTWziY']//input")
        populate_element(element=phoneNumber_input, text=phone_number)
        
        """ Deposit field """
        # Handle the Deposit field
        deposit = find_element_by_xpath(driver, "(//div[@class='sc-9dltft-6 cMhmWq'])[2]")
        click_element(element=deposit) # Open the deposit dropdown
                
        # Wait for all deposit options to appear
        deposit_options = find_list_of_elements_by_xpath(driver, "//div[@class='sc-1efs9pd-4 inESDi']")

        # Select a random deposit option from the dropdown
        random_deposit_option = random.choice(deposit_options)

        # Click the randomly selected deposit option
        click_element(element=random_deposit_option)
        
        """ Checkbox field """
        # Handle the checkbox field (for terms or other agreements)
        checkbox = find_element_by_xpath(driver, "//div[@class='sc-1byafbj-1 gdFGzr']")
        click_element(element=checkbox)

        # Click the "Next" button to proceed
        next_btn = find_element_by_xpath(driver, "//button[contains(normalize-space(text()), 'Next')]")
        click_element(element=next_btn)

        # Handle the demo account ready screen (either close the modal or proceed to sign-in)
        demo_account_ready_screen(driver, set_close)
        
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

def demo_account_ready_screen(driver, set_close: bool = False):
    """
    Handles the demo account creation confirmation screen. 
     - Extracts demo account details and either signs the user in or closes the modal based on `set_close` flag.

    Arguments:
    - set_close: Boolean flag to determine if the modal should be closed after processing (default is False).

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Define a mapping for header labels to their corresponding fields
        header_mapping = {
            "Login:": "MetaTraderID",
            "Password:": "Password",
            "View Only Password:": "View Only Password",
            "Name:": "Account Name",
            "Leverage:": "Leverage",
            "Deposit:": "Deposit",
        }

        # Wait for any loading spinner to disappear and the demo account modal dialog to appear
        spinner_element(driver)
        visibility_of_element_by_xpath(driver, "//div[@class='sc-ur24yu-1 eqxJBS']")
        
        match = wait_for_text_to_be_present_in_element_by_xpath(driver, f"//div[contains(normalize-space(text()), 'Your Demo Account is Ready!')]", text='Your Demo Account is Ready!')
        if not match:
            assert False, "hey this is not correct"

        # Retrieve header labels from the page and map them to our predefined labels
        header_elements = find_list_of_elements_by_xpath(driver, "//span[@class='sc-zee84o-5 eFtIIM']")
        header_labels = [header_mapping.get(element.text, element.text) for element in header_elements]
        header_labels.append("Currency") # Append Currency label for deposit handling

        # Initialize an empty list to hold the demo account details
        demo_account_details = []

        # Retrieve all the account details values from the page
        demoAccount_elements = find_list_of_elements_by_xpath(driver, "//span[@class='sc-zee84o-5 hPAmu']")

        # Iterate through the elements to extract account details
        for idx, element in enumerate(demoAccount_elements):
            # Get the text of the element
            label = get_label_of_element(element)
            
            # Special handling for leverage (idx == 4) to remove unwanted spaces in the label
            if idx == 4:
                label = re.sub(r'\s*:\s*', ":", label)
                
            # Special handling for deposit (idx == 5) to split the amount and currency
            elif idx == 5:
                match = re.search(r'([0-9,]+)\s([A-Za-z]+)', label)
                if match:
                    demo_account_details.append(match.group(1))  # Amount
                    demo_account_details.append(match.group(2))  # Currency
                    continue
            # Add the label to the list of demo account details
            demo_account_details.append(label)

        # Tabulate and attach the demo account details to a report
        demo_account_info = extract_order_data_details(driver, [demo_account_details], header_labels, section_name="Your Demo Account is Ready!")
        
        # Convert the data into a grid format for easy reading
        overall = tabulate(demo_account_info.set_index('Section').T.fillna('-'), headers='keys', tablefmt='grid', stralign='center')
        attach_text(overall, name="Your Demo Account is Ready!")

        # If set_close is True, close the demo account modal dialog, otherwise proceed with sign-in
        if set_close:
            """Closes the demo account modal dialog."""
            modal_close = find_element_by_xpath(driver, "//div[@class='sc-1dvc755-6 hyBcLN']//*[name()='svg']")
            click_element(modal_close)
        else:
            # Proceed with the sign-in process using the demo account details
            handle_sign_in(driver, demo_account_details)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_sign_in(driver, demo_account_details):
    """
    Handles the sign-in process after demo account creation.

    Arguments:
    - demo_account_details: A tuple containing the demo account username and password.
    """

    # Find and click the 'Sign In' button to navigate to the login page
    sign_in_button = find_element_by_xpath(driver, "//div[@class='sc-1dvc755-5 eugaOX']/button")
    click_element(sign_in_button)
    
    # Wait for a brief moment to ensure the page has time to load
    delay(0.5)
    
    # Get the current URL after clicking the 'Sign In' button
    current_url = get_current_url(driver)
    
    # Ensure that the URL contains 'web/login' (indicating that we are on the login page)
    if "web/login" not in current_url:
        assert False, f"Redirected to {current_url}"

    # Validate the login username by checking if it matches the demo account username
    username_input = find_element_by_testid(driver, data_testid="login-user-id")
    assert username_input.get_attribute("value") == demo_account_details[0], "Username mismatch"

    # Validate the login password by checking if it matches the demo account password
    password_input = find_element_by_testid(driver, data_testid="login-password")
    assert password_input.get_attribute("value") == demo_account_details[1], "Password mismatch"

    # Find and click the 'Submit' button to proceed with the login
    submit_button = find_element_by_testid(driver, data_testid="login-submit")
    click_element(submit_button)

    # Check if an announcement modal is present and handle it
    modal_announcement(driver)
    
    # Validate that the account details are correct after logging in
    validate_account_details(driver, demo_account_details)

   
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def validate_account_details(driver, demo_account_details):
    """
    Validates account details after successful sign-in.

    Arguments:
    - demo_account_details: A list containing the demo account details (username, password, etc.).
    """
    
    # Ensure that the "DEMO" text is displayed to confirm we're on the demo account
    wait_for_text_to_be_present_in_element_by_xpath(driver, "//span[@class='sc-cj7llv-0 sc-1lvl0n3-0 eOJwGU himwOQ']", text="DEMO")

    # Validate the Account Name displayed matches the expected value from demo_account_details
    account_name = get_label_of_element(find_element_by_xpath(driver, "//div[@class='sc-ck4lnb-5 fRgsvl']"))
    assert account_name == demo_account_details[3], "Account name mismatch"

    # Validate the MetaTraderID (Trader ID) displayed matches the expected value from demo_account_details
    trader_id = get_label_of_element(find_element_by_xpath(driver, "//div[@class='sc-ck4lnb-3 fdbvSk']"))
    assert trader_id == demo_account_details[0], "MetaTraderID mismatch"

    # Validate the USD / Leverage information
    usd_leverage = get_label_of_element(find_element_by_xpath(driver, "//div[@class='sc-ck4lnb-4 iPvqUv']"))
    match = re.search(r"(\w+)\s*\|\s*([\d:]+)", usd_leverage)
    assert match.group(1) == demo_account_details[-1], f"Currency mismatch. Expected {demo_account_details[-1]} but found {match.group(1)}"
    assert match.group(2) == demo_account_details[4], f"Leverage mismatch. Expected {demo_account_details[4]} but found {match.group(2)}"

    # Validate the Account Balance displayed matches the expected value from demo_account_details
    account_balance = get_label_of_element(find_element_by_xpath(driver, "(//div[@class='sc-2l74dl-0 iwdqqf'])[1]"))
    # Extract the numerical value of the account balance from the displayed text using regex
    balance_value = re.search(r'\$(\d{1,3}(?:,\d{3})*)', account_balance).group(1)
    assert balance_value == demo_account_details[-2], "Account balance mismatch"

    
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""