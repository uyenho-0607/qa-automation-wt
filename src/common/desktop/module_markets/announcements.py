from constants.helper.error_handler import handle_exception
from constants.helper.element import get_label_of_element, spinner_element, find_element_by_xpath



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                WATCHLIST - FILTER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def announcement_validation(driver):
    try:
        spinner_element(driver)
        
        announcement = find_element_by_xpath(driver, "//span[@class='sc-e1w4ks-4 gmeSyq']")
        label_announcement = get_label_of_element(element=announcement)
        
        if label_announcement == "#" or label_announcement == " ":
            raise AssertionError("System should not reflect #")
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""