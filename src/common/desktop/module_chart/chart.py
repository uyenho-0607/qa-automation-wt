from constants.element_ids import DataTestID
from constants.helper.driver import delay
from constants.helper.element import spinner_element, click_element, find_element_by_testid, is_element_present_by_testid, get_label_of_element, visibility_of_element_by_testid
from constants.helper.error_handler import handle_exception


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CHART SYMBOL NAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_chart_symbol_name(driver):
    """
    This function attempts to find the symbol name from the chart overview section. 
    It retrieves the text of the first element with the test ID "symbol-overview-id" and splits it to extract the symbol part.
    
    Returns:
    - str or None: The chart symbol name if found, otherwise None.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Find the elements that contain the symbol name        
        if is_element_present_by_testid(driver, data_testid=DataTestID.SYMBOL_OVERVIEW_ID.value):
            chart_symbol_name = visibility_of_element_by_testid(driver, data_testid=DataTestID.SYMBOL_OVERVIEW_ID.value)
            # # Extract the symbol name from the first element if it exists
            chart_symbolName = get_label_of_element(element=chart_symbol_name).split()[0]
            return chart_symbolName
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CHART - MIN / MAX FULLSCREEN CHART
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Min / Max the Chart
def chart_minMax(driver, chart_fullscreen: str):
    """ 
    This function will wait for the page to load, ensure that the spinner element is not visible,
    and then click the fullscreen button to either expand or collapse the chart window.
    
    Arguments:
    - chart_fullscreen: The 'data-testid' value for the fullscreen button on the chart.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Wait for any loading spinner to disappear before proceeding
        spinner_element(driver)

        # Introduce a slight delay to ensure that the chart is ready for interaction
        delay(0.5)
        
        # Determine the data-testid based on the button type
        button_testids = {
            "toggle": DataTestID.CHART_TOGGLE_FULLSCREEN.value,
            "exit": DataTestID.CHART_EXIT_FULLSCREEN.value
        }
        
        button_testid = button_testids.get(chart_fullscreen)
        if not button_testid:
            raise ValueError(f"Invalid button type: {chart_fullscreen}")
        
        # Attempt to locate the button
        expand_collapse_screen = find_element_by_testid(driver, data_testid=button_testid)
        # Click the fullscreen button to toggle the fullscreen state
        click_element(element=expand_collapse_screen)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CHART - CLOSE THE OPW MODAL
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def chart_trade_modal_close(driver):
    """
    This function finds the close button of the trade modal using the `data-testid` attribute,
    and then clicks it to close the modal. If an issue is encountered, it will be logged and handled.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Find all elements matching the attribute selector
        button_trade = find_element_by_testid(driver, data_testid=DataTestID.CHART_TRADE_BUTTON_CLOSE.value)
        click_element(element=button_trade)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""