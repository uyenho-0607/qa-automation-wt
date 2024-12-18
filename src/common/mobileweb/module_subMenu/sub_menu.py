from constants.helper.element import click_element, click_element_with_wait, visibility_of_element_by_testid, visibility_of_element_by_xpath
from constants.helper.error_handler import handle_exception



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                MENU SELECTION (TRADE / MARKET / ASSET / SIGNAL / CALENDAR / NEWS)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# menu button (Trade / Market / Asset / Signal / Calendar / News
def menu_button(driver, menu_option):
    try:
       
        menu_selection = visibility_of_element_by_testid(driver, data_testid=f"side-bar-option-{menu_option}")
        click_element_with_wait(driver, element=menu_selection)
        
    except Exception as e:
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ASSET - MY TRADE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def myTrade_button(driver):
    try:
       
        menu_selection = visibility_of_element_by_xpath(driver, "//div[contains(@class, 'r-1otgn73 r-18u37iz r-1wtj0ep')]")
        click_element(element=menu_selection)
        
    except Exception as e:
        handle_exception(driver, e)
        