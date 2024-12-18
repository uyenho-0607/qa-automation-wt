import traceback

from constants.helper.screenshot import take_screenshot
from constants.helper.element import click_element, visibility_of_element_by_testid, find_element_by_testid
from constants.helper.error_handler import handle_exception
from selenium.common.exceptions import NoSuchElementException


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                MODAL ANNOUNCEMENT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def modal_announcement(driver):
    try:
        # Wait for the modal to be visible (with a timeout)
        try:
            visibility_of_element_by_testid(driver, data_testid="feature-announcement-modal")
            # Proceed with actions if the modal is visible
            print("Announcement modal is visible, performing actions...")
            # Add your actions here (e.g., close modal or interact with modal)
            modal_announcement_gotIt(driver)
        except:
            print("Announcement modal not visible, skipping...")
            return  # Skip if modal is not visible
    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                MODAL ANNOUNCEMENT GOT IT BUTTON
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def modal_announcement_gotIt(driver):
    try:
        # Continuously check for "Got It" buttons until none are found
        while True:
            try:
                got_it_button = find_element_by_testid(driver, data_testid="feature-announcement-modal-got-it-button")
                
                # Click on the "Got It" button
                click_element(element=got_it_button)
                
                print("Clicked 'Got It' button. Continuing to the next announcement...")
                
            except NoSuchElementException:
                # If no more "Got It" buttons are found, exit the loop
                print("No more 'Got It' buttons found.")
                break
            except Exception as e:
                # Handle any unexpected errors that may arise during the click
                take_screenshot(driver, "Exception Screenshot")
                assert False, f"Error while interacting with modal: {str(e)}\n{traceback.format_exc()}"
                
    except Exception as e:
        handle_exception(driver, e)



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                MODAL ANNOUNCEMENT ARROW
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def modal_announcement_arrow(driver, directional_arrows):
    try:
        # Click on the left or right arrow button
        arrow_button = find_element_by_testid(driver, data_testid=f"feature-announcement-modal-media-{directional_arrows}-button")
        click_element(element=arrow_button)
        
    except Exception as e:
        handle_exception(driver, e)


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                MODAL ANNOUNCEMENT TRY IT NOW BUTTON
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def modal_announcement_tryItNow(driver):
    try:
        # Click on the Try It Now button
        try_it_button = find_element_by_testid(driver, data_testid=f"feature-announcement-modal-try-it-now-button")
        click_element(element=try_it_button)
        
    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""