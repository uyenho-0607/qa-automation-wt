import traceback

from constants.helper.driver import delay
from constants.helper.element import click_element_with_wait, find_element_by_testid, find_list_of_elements_by_testid, spinner_element
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import take_screenshot



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CHART SYMBOL NAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_chart_symbol_name(driver):
    try:
        
        chart_symbol_name = find_list_of_elements_by_testid(driver, data_testid="symbol-overview-id")
        chart_symbolName = chart_symbol_name[0].text.split()[0] if chart_symbol_name else None
        return chart_symbolName
    
    except Exception as e:
        handle_exception(driver, e)
        # # Attach a screenshot in case of an exception
        # take_screenshot(driver, "get_chart_symbol_name - Exception Screenshot")
        # # Log the full exception message and stacktrace
        # # Raise an assertion error with the error message
        # assert False, f"{str(e)}\n{traceback.format_exc()}"

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
def chart_minMax(driver, chart_fullscreen):
    try:
        spinner_element(driver)
        
        delay(0.5)
        
        # Find all elements matching the attribute selector
        expand_collapse_screen  = find_element_by_testid(driver, data_testid=chart_fullscreen)
        click_element_with_wait(driver, element=expand_collapse_screen)
        
    except Exception as e:
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
    try:
        # Find all elements matching the attribute selector
        button_trade = find_element_by_testid(driver, data_testid="chart-trade-button-close")
        # button_trade = find_element_by_xpath(driver, "//div[@class='sc-crulu1-3 guyQQb']")
        click_element_with_wait(driver, element=button_trade)

    except Exception as e:
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
