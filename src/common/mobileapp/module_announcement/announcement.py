from selenium.common.exceptions import NoSuchElementException, TimeoutException

from constants.element_ids import DataTestID
from constants.helper.error_handler import handle_exception
from constants.helper.element_android_app import click_element, spinner_element, find_element_by_xpath, find_visible_element_by_testid, find_element_by_testid, get_label_of_element
from enums.main import AnnouncementModal

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ANNOUNCEMENT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def announcement_validation(driver):
    try:
        spinner_element(driver)
        
        announcement = find_element_by_xpath(driver, DataTestID.HOME_ANNOUNCEMENT)
        label_announcement = get_label_of_element(element=announcement)
        print(label_announcement)
        if label_announcement == "#" or label_announcement == " ":
            raise AssertionError("System should not reflect # or blank")
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                MODAL ANNOUNCEMENT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def modal_announcement(driver, button: AnnouncementModal.GOT_IT):
    """
    This function waits for the feature announcement modal to be visible and interacts with it.
    If the modal is not visible, the function skips any further actions.
    
    Arguments:
    - button: The type of button to click ('got-it' or 'try-it-now' or 'media-left', 'media-right'). Defaults to 'got-it'.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Wait for the login process to complete (spinner disappears)
        spinner_element(driver)

        # Wait for the feature announcement modal to be visible
        find_visible_element_by_testid(driver, data_testid=DataTestID.FEATURE_ANNOUNCEMENT_MODAL)

        # If the modal is visible, interact with it (click "Got it")
        handle_modal_announcement(driver, button)
    
    except (TimeoutException, Exception) as e:
        # Skip if modal is not visible (TimeoutException from visibility_of_element_by_testid)
        if isinstance(e, TimeoutException):
            pass  # Skip the modal interaction if TimeoutException occurs
        else:
            # Handle any other exceptions that occur during the execution
            handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                MODAL ANNOUNCEMENT GOT IT / TRY IT NOW BUTTON
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_modal_announcement(driver, button_type: AnnouncementModal):
    """
    This function handles modal announcements by clicking either the "Got It", "Try It Now", or "Media-Arrow" buttons.
    If the "got-it" button is selected, it clicks all "Got It" buttons until none are found.
    If the "try-it-now" button is selected, it clicks that button once.
    If the "media-left" or "media-right" buttons are selected, it clicks those buttons once.

    Arguments:
    - button_type: The type of button to click ('got-it' or 'try-it-now' or 'media-left', 'media-right'). Defaults to 'got-it'.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Determine the data-testid based on the button type
        button_testids = {
            AnnouncementModal.GOT_IT: DataTestID.FEATURE_ANNOUNCEMENT_MODAL_GOT_IT_BUTTON,
            AnnouncementModal.TRY_IT: DataTestID.FEATURE_ANNOUNCEMENT_MODAL_TRY_IT_NOW_BUTTON,
            AnnouncementModal.MEDIA_LEFT: DataTestID.FEATURE_ANNOUNCEMENT_MODAL_MEDIA_LEFT_BUTTON,
            AnnouncementModal.MEDIA_RIGHT: DataTestID.FEATURE_ANNOUNCEMENT_MODAL_MEDIA_RIGHT_BUTTON
        }
        

        button_testid = button_testids.get(button_type)
        if not button_testid:
            raise ValueError(f"Invalid button type: {button_type}")
        
        # Attempt to locate the button
        modal_button = find_element_by_testid(driver, data_testid=button_testid)
        
        if button_type == AnnouncementModal.GOT_IT:
            # Continuously click the "Got It" button until it's no longer found
            while modal_button:
                click_element(element=modal_button)
                try:
                    # Try to locate the "Got It" button again
                    modal_button = find_element_by_testid(driver, data_testid=button_testid)
                except NoSuchElementException:
                    # If no more "Got It" buttons are found, exit the loop
                    break
        else:
            # For "try-it-now", "media-left", and "media-right", click the button once
            click_element(element=modal_button)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""