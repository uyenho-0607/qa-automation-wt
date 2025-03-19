from constants.element_ids import DataTestID
from constants.helper.element_android_app import click_element, find_element_by_xpath, populate_element, find_visible_element_by_xpath


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CHANGE ACCOUNT PASSWORD
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def change_password(driver, old_password, new_password, confirm_password):
    # Locate and populate the old password input field
    old_password_input = find_visible_element_by_xpath(driver, DataTestID.APP_CHANGE_PASSWORD_MODAL_OLD_PASSWORD)
    populate_element(element=old_password_input, text=old_password)

    # Locate and populate the new password input field
    new_password_input = find_element_by_xpath(driver, DataTestID.APP_CHANGE_PASSWORD_MODAL_NEW_PASSWORD)
    populate_element(element=new_password_input, text=new_password)

    # Locate and populate the confirm password input field
    confirm_password_input = find_element_by_xpath(driver, DataTestID.APP_CHANGE_PASSWORD_MODAL_CONFIRM_NEW_PASSWORD)
    populate_element(element=confirm_password_input, text=confirm_password)

    # Find the submit button and click it
    submit_button = find_element_by_xpath(driver, DataTestID.APP_CHANGE_PASSWORD_MODAL_CONFIRM)
    click_element(element=submit_button)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""