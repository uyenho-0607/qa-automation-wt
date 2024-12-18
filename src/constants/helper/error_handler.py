import traceback
import inspect

from constants.helper.screenshot import take_screenshot


def handle_exception(driver, e):
    # Get the current function name
    function_name = inspect.stack()[1].function
    
    # capitalize() will capitalize the first letter of the function name (e.g., myFunction becomes MyFunction).
    # Capitalize the first letter of the function name
    # capitalized_function_name = function_name.capitalize()
    
    # upper() will capitalize all letters of the function name (e.g., myFunction becomes MYFUNCTION).
    # Capitalize all letters of the function name
    # uppercase_function_name = function_name.upper()

    # Attach a screenshot with the function name in the filename
    take_screenshot(driver, f"Exception_Screenshot - {function_name}")
    
    # Log the full exception message and stack trace
    assert False, f"{str(e)}\n{traceback.format_exc()}"