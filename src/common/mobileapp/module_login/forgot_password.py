
from enums.main import AccountType, AlertType
from constants.element_ids import DataTestID

from constants.helper.error_handler import handle_exception
from constants.helper.element_android_app import click_element, find_element_by_xpath, is_element_present_by_xpath, populate_element, find_visible_element_by_xpath, find_element_by_xpath_with_wait, wait_for_text_to_be_present_in_element_by_xpath

from common.mobileapp.module_login.login import handle_alert_error, select_account_type, click_splash_screen


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                FORGOT PASSWORD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def handle_help_is_on_the_way(driver):
    """Handles the 'Help is on the way' screen by navigating to Contact Support and returning to login."""
    btn_contact_support = find_element_by_xpath(driver, DataTestID.APP_CONTACT_SUPPORT)
    click_element(element=btn_contact_support)
    
    # Retrieve the in app browser url
    browser_url = find_visible_element_by_xpath(driver, DataTestID.IN_APP_BROWSER_URL_bar)
    print(browser_url.text)
    
    # Close in app browser
    close_in_app_browser(driver)
    
    # Redirect back to login screen
    btn_back_to_login = find_visible_element_by_xpath(driver, DataTestID.APP_BACK_TO_LOGIN_SCREEN)
    click_element(element=btn_back_to_login)


def close_in_app_browser(driver):
    """Closes the in-app browser if open."""
    btn_close_browser = find_visible_element_by_xpath(driver, DataTestID.IN_APP_BROWSER_CLOSE_BUTTON)
    click_element(element=btn_close_browser)



def handle_reset_password_flow(driver, email, accountID, account_type):
    """Handles email/accountID input and submission."""

    # Input Email Address
    input_email = find_element_by_xpath(driver, DataTestID.APP_RESET_PASSWORD_EMAIL_ADDRESS)
    populate_element(element=input_email, text=email)

    # Input account ID if required
    if account_type==AccountType.LIVE and accountID:
        input_accountID = find_element_by_xpath(driver, DataTestID.APP_RESET_PASSWORD_ACCOUNT_ID)
        populate_element(element=input_accountID, text=accountID)
    
    # Click 'Submit' button
    btn_submit = find_element_by_xpath(driver, DataTestID.APP_RESET_PASSWORD_SUBMIT)
    click_element(element=btn_submit)
    
    wait_for_text_to_be_present_in_element_by_xpath(driver, DataTestID.APP_HELP_IS_ON_THE_WAY, "Help is on the way!")
    
    handle_help_is_on_the_way(driver)
    
    

def forgot_password(driver, email: str, accountID: str = None, account_type: AccountType = AccountType.LIVE):
    try:
        click_splash_screen(driver)
        select_account_type(driver, account_type)

        if not is_element_present_by_xpath(driver, DataTestID.APP_FORGOT_PASSWORD):
            assert False, "Forgot Password button not found"
        
        click_element(find_element_by_xpath_with_wait(driver, DataTestID.APP_FORGOT_PASSWORD))

        # Check for Reset Password page
        if wait_for_text_to_be_present_in_element_by_xpath(driver, DataTestID.APP_RESET_PASSWORD, "Reset Password"):
            handle_reset_password_flow(driver, email, accountID, account_type)
            return  # Exit after successful flow

        # Check for in-app browser
        if find_visible_element_by_xpath(driver, DataTestID.IN_APP_BROWSER_URL_bar):
            close_in_app_browser(driver)
            return  # Exit after closing browser

        # Fallback error handling
        handle_alert_error(driver, expectation=AlertType.SUCCESS)

    except Exception as e:
        handle_exception(driver, e)


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""