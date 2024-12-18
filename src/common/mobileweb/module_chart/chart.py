from constants.helper.driver import delay
from constants.helper.element import click_element_with_wait, find_element_by_testid, visibility_of_element_by_testid
from constants.helper.error_handler import handle_exception



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CHART SYMBOL NAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_chart_symbol_name(driver):
    try:
        
        chart_symbol_name = visibility_of_element_by_testid(driver, data_testid="symbol-overview-id")
        return chart_symbol_name

    except Exception as e:
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
def chart_minMax(driver, chart_fullscreen):
    try:
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
        
        # take_screenshot(driver, "Trade_Action")

    except Exception as e:
        handle_exception(driver, e)
