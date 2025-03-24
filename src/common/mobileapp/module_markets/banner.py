from constants.element_ids import DataTestID

from constants.helper.error_handler import handle_exception
from constants.helper.element_android_app import find_element_by_xpath_with_wait



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                MESTHEAD BANNER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def  verify_mesthead_banner(driver):
    try:

        image_element = find_element_by_xpath_with_wait(driver, DataTestID.MESTHEAD_BANNER)
        
        # Get the 'src' attribute
        image_src = image_element.get_attribute("src")
        print(image_src)
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""