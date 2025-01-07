
from constants.helper.driver import delay
from constants.helper.element import click_element, find_element_by_testid, find_list_of_elements_by_testid, spinner_element
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
        chart_symbol_name = find_list_of_elements_by_testid(driver, data_testid="symbol-overview-id")
        
        # Extract the symbol name from the first element if it exists
        chart_symbolName = chart_symbol_name[0].text.split()[0] if chart_symbol_name else None
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
        
        # Find the fullscreen button element using the provided data-testid
        expand_collapse_screen  = find_element_by_testid(driver, data_testid=f"chart-{chart_fullscreen}-fullscreen")
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
        button_trade = find_element_by_testid(driver, data_testid="chart-trade-button-close")
        click_element(element=button_trade)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
