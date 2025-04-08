import random

from enums.main import Menu
from constants.element_ids import DataTestID
from appium.webdriver.common.appiumby import AppiumBy

from constants.helper.driver import delay
from constants.helper.element_android_app import swipe_left, click_element, find_element_by_xpath_with_wait, find_element_by_testid_with_wait, find_list_of_elements_by_xpath, get_label_of_element
from constants.helper.error_handler import handle_exception

from common.mobileapp.module_sub_menu.utils import menu_button
from common.mobileapp.module_symbol.search_symbol import input_symbol


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TOGGLE SYMBOL TO FAV / UNFAVOURITE STAR
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def toggle_symbol_favorite_status(driver):
    try:
        
        # Redirect to the Markets page
        menu_button(driver, menu=Menu.TRADE)
        
        star_icon = find_element_by_testid_with_wait(driver, data_testid=DataTestID.APP_CHART_STAR_SYMBOL)
        click_element(element=star_icon)
        
    except Exception as e:
        handle_exception(driver, e)
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                REMOVE FAVOURITE SYMBOL
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def remove_favorite_symbol(driver, server=None):
    try:
        
        # Search for symbol
        input_symbol(driver, server)
        
        # Click on the 'Star' icon to favourite
        star_icon = find_element_by_testid_with_wait(driver, data_testid=DataTestID.APP_CHART_STAR_SYMBOL)
        click_element(element=star_icon)
                
        # Redirect to the Markets page
        menu_button(driver, menu=Menu.MARKET)
        
        # Click on Fav tab        
        btn_fav = find_element_by_xpath_with_wait(driver, DataTestID.APP_TAB_TOP_FAVOURITES)
        click_element(element=btn_fav)
        
        delay(1)
        
        # Find the first matching element from the list and perform a left swipe
        rows = find_list_of_elements_by_xpath(driver, DataTestID.APP_MARKET_SYMBOL_ROW_ITEMS)
        print(f"Number of elements found: {len(rows)}")
        
        if not rows:
            msg = find_element_by_xpath_with_wait(driver, DataTestID.APP_MSG_NO_ITEMS_AVAILABLE)
            label_msg = get_label_of_element(element=msg)
            assert False, f"Retrieved: {label_msg}"
        
        # Randomly select one row from the list
        row = random.choice(rows)
        
        # Find the symbol name within the selected row
        label_symbolName = row.find_element(AppiumBy.XPATH, DataTestID.APP_MARKET_WATCHLIST_FAV_SYMBOL_NAME)
        label_symbol_name = get_label_of_element(element=label_symbolName)
        print("Symbol Name", label_symbol_name)
        swipe_left(driver, element=row)
        
        # Click on the 'Remove' button
        btn_remove = find_element_by_xpath_with_wait(driver, DataTestID.APP_MARKET_SYMBOL_ROW_REMOVE)
        click_element(btn_remove)
        
        delay(1)
        
        updated_rows = find_list_of_elements_by_xpath(driver, DataTestID.APP_MARKET_SYMBOL_ROW_ITEMS)

        # Extract all symbol names after removal
        updated_symbol_names = []
        for updated_row in updated_rows:
            symbol_label = updated_row.find_element(AppiumBy.XPATH, DataTestID.APP_MARKET_WATCHLIST_FAV_SYMBOL_NAME)
            updated_symbol_names.append(get_label_of_element(symbol_label))


            # Assert that the symbol is no longer in the list
            assert label_symbol_name not in updated_symbol_names, f"❌ Symbol '{label_symbol_name}' was not removed"

            print(f"Symbol '{label_symbol_name}' successfully removed.")
            break  # Exit loop once assertion passes
                
    except Exception as e:
        handle_exception(driver, e)
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""