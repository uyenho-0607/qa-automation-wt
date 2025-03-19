import random

from constants.element_ids import DataTestID
from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception
from constants.helper.element_android_app import click_element, find_element_by_testid, find_element_by_xpath, find_list_of_elements_by_xpath, get_label_of_element, is_element_present_by_xpath, find_presence_element_by_testid, spinner_element, find_visible_element_by_xpath, populate_element, find_element_by_xpath_with_wait, wait_for_text_to_be_present_in_element_by_xpath

from common.mobileapp.module_login.login import authenticate_user, handle_login_result, select_account_type, splash_screen
from data_config.generate_dummy_data import generate_random_name_and_email, generate_random_credential, generate_singapore_phone_number
from enums.main import AccountType

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                FORGOT PASSWORD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def app_signup(driver, expect_failure: bool = True, selected_language: str = None):
    try:
        
        # Skip the splash screen
        splash_screen(driver)
        
        # Step 2: Select account type (CRM)
        select_account_type(driver, account_type=AccountType.CRM)
        
        # Step 3: Verify and click the 'Forgot Password' button
        if not is_element_present_by_xpath(driver, DataTestID.APP_SIGN_UP):
            raise AssertionError("Sign Up button not found")
        
        # Locate the forgot Password button
        btn_sign_up = find_element_by_xpath_with_wait(driver, DataTestID.APP_SIGN_UP)
        click_element(element=btn_sign_up)
        
        if wait_for_text_to_be_present_in_element_by_xpath(driver, DataTestID.APP_SIGN_UP, text="Sign up"):

            # Generate a random username
            username, first_name, last_name, email = generate_random_name_and_email()
            
            # Input username
            input_username = find_element_by_xpath(driver, DataTestID.APP_SIGN_UP_USERNAME)
            populate_element(element=input_username, text=username)
            
            # Click to reveal the title dropdown options
            title = find_element_by_xpath(driver, DataTestID.APP_SIGN_UP_TITLE)
            click_element(element=title)
            
            delay(1)
            
            # Select the title dropdown options
            dropdown = find_list_of_elements_by_xpath(driver, DataTestID.APP_SIGN_UP_TITLE_DROPDOWN)
            dropdown_options = random.choice(dropdown)
            click_element(element=dropdown_options)

            # Input first name
            input_first_name = find_visible_element_by_xpath(driver, DataTestID.APP_SIGN_UP_FIRST_NAME)
            populate_element(element=input_first_name, text=first_name)
            
            # Input last name
            input_last_name = find_element_by_xpath(driver, DataTestID.APP_SIGN_UP_LAST_NAME)
            populate_element(element=input_last_name, text=last_name)
            
            # Input email
            input_email = find_element_by_xpath(driver, DataTestID.APP_SIGN_UP_EMAIL)
            populate_element(element=input_email, text=email)
            
            # Generate and input the random password
            password = generate_random_credential()
            input_password = find_element_by_xpath(driver, DataTestID.APP_SIGN_UP_PASSWORD)
            populate_element(element=input_password, text=password)
            
            # Click to reveal the Country of Residence dropdown options
            country_residence = find_element_by_xpath(driver, DataTestID.APP_SIGN_UP_COUNTRY_OF_RESIDENCE)
            click_element(element=country_residence)
            
            # Input to search for country name
            search_country = find_visible_element_by_xpath(driver, DataTestID.APP_SIGN_UP_COUNTRY_OF_RESIDENCE_SEARCH)
            populate_element(element=search_country, text="Singapore")
            
            delay(1)
            
            # Click on the options
            search_country_options = find_element_by_xpath_with_wait(driver, DataTestID.APP_SIGN_UP_COUNTRY_OF_RESIDENCE_OPTIONS)
            click_element(element=search_country_options)
            
            delay(1)
            
            # Generate a random Singapore phone number
            phone_number = generate_singapore_phone_number()
            # Populate the phone number input field with the generated phone number
            input_phone_number = find_element_by_xpath(driver, DataTestID.APP_SIGN_UP_PHONE_NUMBER)
            populate_element(element=input_phone_number, text=phone_number)
            
            """ Checkbox field """
            # Handle the checkbox field (for terms or other agreements)
            checkbox = find_element_by_xpath(driver, DataTestID.APP_SIGN_UP_CHECKBOX)
            click_element(element=checkbox)
                
            # Click the "Next" button to proceed
            btn_next = find_element_by_xpath(driver, DataTestID.APP_SIGN_UP_PROCEED_KYC)
            click_element(element=btn_next)
            
            # Retrieve the banner
            get_signup_banner(driver)
            
            # Perform login action
            authenticate_user(driver, username, password)
            
            handle_login_result(driver, expect_failure, selected_language)
        
    except Exception as e:
        handle_exception(driver, e)
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                EXTRACT THE NEGATIVE SNACKBAR MESSAGE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_signup_banner(driver):
    """
    Extracts the sign up notification message, processes its content, and returns a structured DataFrame with order details.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        
        spinner_element(driver)
        
        delay(1)
        
        label_message_description = find_presence_element_by_testid(driver, data_testid=DataTestID.NOTIFICATION_BOX_DESCRIPTION)
        label_message = get_label_of_element(label_message_description)
        
        if label_message != "You have successfully registered your new account. Please check your email for your account details.":
            raise AssertionError(f"Invalid message description: {label_message}")
            
        # Wait for the message header to be visible
        message_title = find_presence_element_by_testid(driver, data_testid=DataTestID.NOTIFICATION_BOX_TITLE)
        extracted_title = get_label_of_element(message_title)
        
        if extracted_title != "Success":
            raise AssertionError(f"Invalid message title: {extracted_title}")

        btn_close = find_element_by_testid(driver, data_testid=DataTestID.NOTIFICATION_BOX_CLOSE)
        click_element(btn_close)
        
        # Get in-app browser url
        browser = find_visible_element_by_xpath(driver, DataTestID.IN_APP_BROWSER_URL_bar)
        print(browser.text)
        if browser.text in "cpuat.lirunex.com":
            print("Redirect to the correct website")
        
        browser = find_visible_element_by_xpath(driver, DataTestID.IN_APP_BROWSER_CLOSE_BUTTON)
        click_element(element=browser)
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)