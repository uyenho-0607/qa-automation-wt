from constants.element_ids import DataTestID
from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.driver import access_url, get_current_url
from constants.helper.element import click_element, find_element_by_testid, spinner_element, find_visible_element_by_testid, get_label_of_element, populate_element, wait_for_text_to_be_present_in_element_by_xpath

from common.desktop.module_setting.utils import button_setting
from common.desktop.module_announcement.utils import modal_announcement
from common.desktop.module_login.utils import select_account_type


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                POPULATE PASSWORD FIELDS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def populate_password_fields(driver, old_password, new_password, confirm_password):
    """
    Fills in the old, new, and confirm password fields in the password change form.

    Arguments:
    - old_password: The current password of the user.
    - new_password: The new password that the user wants to set.
    - confirm_password: The confirmation of the new password entered by the user.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    # Locate and populate the old password input field
    old_password_input = find_element_by_testid(driver, data_testid=DataTestID.CHANGE_PASSWORD_MODAL_OLD_PASSWORD.value)
    populate_element(element=old_password_input, text=old_password)

    # Locate and populate the new password input field
    new_password_input = find_element_by_testid(driver, data_testid=DataTestID.CHANGE_PASSWORD_MODAL_NEW_PASSWORD.value)
    populate_element(element=new_password_input, text=new_password)

    # Locate and populate the confirm password input field
    confirm_password_input = find_element_by_testid(driver, data_testid=DataTestID.CHANGE_PASSWORD_MODAL_CONFIRM_NEW_PASSWORD.value)
    populate_element(element=confirm_password_input, text=confirm_password)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SUBMIT AND HANDLE ALERT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def submit_and_handle_alert(driver, expected_alert_type, login_username, login_password, params_wt_url=None):
    """
    Submits a form and handles the alert that appears afterward.
    
    Arguments:
    - expected_alert_type: The expected type of alert, such as "success" or "error".
    - login_username: The username to be used for further actions in case of a success alert.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    # Find the submit button and click it
    submit_button = find_element_by_testid(driver, data_testid=DataTestID.CHANGE_PASSWORD_MODAL_CONFIRM.value)
    click_element(element=submit_button)
    
    # Try to capture the alert message and type
    alert_message, actual_alert_type = capture_alert(driver)

    if alert_message:
        # Extract the label/message from the alert
        label_message = get_label_of_element(element=alert_message)
        print(f"Label message: {label_message}")

        # Check if the actual alert type matches the expected one
        if actual_alert_type != expected_alert_type:
            assert False, f"Test failed: Expected alert type '{expected_alert_type}' but got '{actual_alert_type}' with message: {label_message}"

        # Handle different types of alerts
        if actual_alert_type == "success":
            handle_success(driver, label_message, login_username, login_password, params_wt_url)
        elif actual_alert_type == "error":
            handle_error(driver, label_message)

    else:
        # If no alert message is found, log and fail the test
        attach_text("No alert found.", name="Alert check")
        assert False, "No alert message displayed after form submission."

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CAPTURE ALERT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def capture_alert(driver):
    """
    Captures the first visible alert message (success or error) based on predefined test IDs.

    Returns:
    - Tuple (alert_message, alert_type) where:
        - alert_message: The WebElement representing the alert message.
        - alert_type: A string indicating the type of alert ("success", "error", or "no_alert").
        
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    alert_types = [("alert-success", "success"), ("alert-error", "error")]

    for data_testid, alert_type in alert_types:
        try:
            alert_message = find_visible_element_by_testid(driver, data_testid=data_testid)
            return alert_message, alert_type
        except Exception as e:
            # print(f"Error while capturing {alert_type} alert: {e}")
            continue  # Proceed to next alert type if the current one fails

    # If no alert is found, return None with type 'no_alert'
    return None, "no_alert"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                HANDLE SUCCESS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_success(driver, label_message, login_username, login_password, params_wt_url=None,):
    """
    Handles the success alert after an action such as a password change and performs subsequent actions.

    Arguments:
    - label_message: The message from the alert.
    - login_username: The username used for login after the action.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    
    # If the success message indicates a password change, process it
    if "Account password has been updated successfully" in label_message:
        attach_text(label_message, name="Success message found: ")
        
        # Log the user out
        button_setting(driver, setting_option="logout")
        
        # Get the current URL after logout
        current_url = get_current_url(driver)
        
        # Assert that the URL should change to the login page
        if "web/login" in current_url:
            # Perform login with the provided username
            perform_login(driver, login_username, login_password)
        else:
            access_url(driver, url=params_wt_url)
            perform_login(driver, login_username, login_password)

    else:
        # If the success message doesn't match, handle it as an unexpected message
        assert False, f"Unexpected success message: {label_message}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                               PERFORM LOGIN
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def perform_login(driver, login_username, login_password):
    """
    Perform the login process after password change and validate success.

    Arguments:
    - login_username: The username to be used for further actions in case of a success alert.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    
    select_account_type(driver, account_type="live")
    
    # Find and populate the username input field
    userinput_name = find_element_by_testid(driver, data_testid=DataTestID.LOGIN_USER_ID.value)
    populate_element(element=userinput_name, text=login_username)

    # Find and populate the password input field
    password_input = find_element_by_testid(driver, data_testid=DataTestID.LOGIN_PASSWORD.value)
    populate_element(element=password_input, text=login_password)

    # Submit the login form
    submit_button = find_element_by_testid(driver, data_testid=DataTestID.LOGIN_SUBMIT.value)
    click_element(submit_button)
    
    # Wait until the login process completes (spinner disappears)
    spinner_element(driver)

    # Optionally handle modal announcement or further actions
    modal_announcement(driver)
    
    # Wait for the account balance element to be visible, ensuring successful login
    wait_for_text_to_be_present_in_element_by_xpath(driver, "//div[normalize-space(text())='Account Balance']", text="Account Balance")
    
    # Attach a success message or log the result
    attach_text("Login Successfully", name="Login")
    
    assert True

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                HANDLE ERROR
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_error(driver, label_message):
    """
    Handle error messages that may appear during a process (e.g., password change).

    Arguments:
    - label_message: The message from the alert.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """

    # Define common error messages and their corresponding log labels
    error_messages = {
        "Invalid current password": "Error message found: Invalid current password",
        "Password format is incorrect.": "Error message found: Password format is incorrect",
        "New password does not match confirm password": "Error message found: New password mismatch",
        "New password cannot be the same as previous 5 old password": "Error message found: New password is too similar"
    }

    # Check if the label_message contains any of the predefined error messages
    for error_text, error_label in error_messages.items():
        # If a match is found, attach the label message and stop further checks
        if error_text in label_message:
            attach_text(label_message, name=error_label) # Attach the error message for reporting
            break  # Stop after finding the first matching error message

    # Close the modal dialog
    btn_close = find_element_by_testid(driver, data_testid=DataTestID.CHANGE_PASSWORD_MODAL_CLOSE.value)
    click_element(element=btn_close)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CHANGE PASSWORD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def change_password(driver, old_password, new_password, confirm_password, alert_type="error", login_username=None, login_password=None, params_wt_url=None):
    """
    Changes the user's password on the platform.

    Arguments:
    - old_password: The current password of the user.
    - new_password: The new password to be set.
    - confirm_password: The confirmation of the new password.
    - alert_type: The expected type of alert after submission (default is "error").
    - login_username: The username to be used for further actions in case of a success alert (optional).

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """

    try:
        
        # Step 1: Navigate to the Change Password section
        button_setting(driver, setting_option="change-password")

        # Validate input parameters
        if not all([old_password, new_password, confirm_password]):
            raise ValueError("All password fields must be provided.")
        
        # Step 2: Populate password fields
        populate_password_fields(driver, old_password, new_password, confirm_password)

        # Step 3: Submit the form and capture alert
        submit_and_handle_alert(driver, alert_type, login_username, login_password, params_wt_url)
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""