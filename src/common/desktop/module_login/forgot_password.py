from constants.element_ids import DataTestID
from enums.main import Server, Platform, AccountType, EnvironmentType

from constants.helper.error_handler import handle_exception
from constants.helper.driver import get_current_url, switch_to_new_window
from constants.helper.element import click_element, find_element_by_xpath, is_element_present_by_xpath, javascript_click, populate_element, find_visible_element_by_xpath, wait_for_text_to_be_present_in_element_by_xpath, get_label_of_element

from common.desktop.module_login.utils import select_account_type, launch_wt

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                FORGOT PASSWORD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def handle_help_is_on_the_way(driver):
    """Handles the 'Help is on the way' screen by navigating to Contact Support and returning to login."""
    btn_contact_support = find_element_by_xpath(driver, DataTestID.CONTACT_SUPPORT)
    click_element(element=btn_contact_support)

    # Switch to the new window
    switch_to_new_window(driver)
    
    # Step 9: Capture and print the current URL
    print(get_current_url(driver))



def handle_reset_password_flow(driver, email, accountID, account_type):
    """Handles email/accountID input and submission."""

    # Input Email Address
    input_email = find_element_by_xpath(driver, DataTestID.RESET_PASSWORD_EMAIL_ADDRESS)
    populate_element(element=input_email, text=email)

    # Input account ID if required
    if account_type==AccountType.LIVE and accountID:
        input_accountID = find_element_by_xpath(driver, DataTestID.RESET_PASSWORD_ACCOUNT_ID)
        populate_element(element=input_accountID, text=accountID)
    
    # Click 'Submit' button
    btn_submit = find_element_by_xpath(driver, DataTestID.RESET_PASSWORD_SUBMIT)
    click_element(element=btn_submit)
    
    if wait_for_text_to_be_present_in_element_by_xpath(driver, DataTestID.HELP_IS_ON_THE_WAY, "Help is on the way!"):
        handle_help_is_on_the_way(driver)
        return
    
    error_message = find_element_by_xpath(driver, DataTestID.FORGOT_PASSWORD_ERROR_MESSAGE)
    assert False, get_label_of_element(element=error_message)
    
    

def forgot_password(driver, server: Server, device_type: Platform = Platform.DESKTOP, env_type: EnvironmentType = EnvironmentType.SIT,
                    email: str = None, accountID: str = None, account_type: AccountType = AccountType.LIVE):
    try:

        # Step 1: Launch WebTrader platform
        launch_wt(driver, server, device_type, env_type)
        
        # Step 2: Select account type (CRM/Live/Demo)
        select_account_type(driver, account_type)

        if not is_element_present_by_xpath(driver, DataTestID.FORGOT_PASSWORD):
            assert False, "Forgot Password button not found"
        
        # Locate the forgot Password button
        btn_forgot_password = find_visible_element_by_xpath(driver, DataTestID.FORGOT_PASSWORD)
        javascript_click(driver, element=btn_forgot_password)

        # Check for Reset Password page
        if wait_for_text_to_be_present_in_element_by_xpath(driver, DataTestID.RESET_PASSWORD, text="Reset Password"):
            handle_reset_password_flow(driver, email, accountID, account_type)
            return  # Exit after successful flow

        # Check for in-app browser
        switch_to_new_window(driver)
        if get_current_url(driver):
            print(get_current_url(driver))
            return  # Exit after closing browser

    except Exception as e:
        handle_exception(driver, e)


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""