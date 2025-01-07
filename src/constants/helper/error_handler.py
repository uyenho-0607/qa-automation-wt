import inspect
import logging
import traceback

from constants.helper.screenshot import take_screenshot


# Configure logging
# Log everything at DEBUG level and above
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


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
    logger.error(f"Error occurred in {function_name}: {e}", exc_info=True)
    assert False, f"{str(e)}\n{traceback.format_exc()}"