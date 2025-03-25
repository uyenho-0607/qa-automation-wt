from selenium.webdriver.common.by import By

from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, get_label_of_element, is_element_disabled_by_cursor, spinner_element, find_visible_element_by_xpath, find_element_by_testid

from common.desktop.module_sub_menu.sub_menu import menu_button
from common.desktop.module_trade.order_panel.op_general import get_table_body
from common.desktop.module_trade.order_panel.order_panel_info import type_orderPanel

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SETTING ACCOUNT INFORMATION TAB
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def verify_order_panel_button_disabled(driver):
    """Verify that the Edit / Close / Delete action buttons are disabled in a given order panel tab."""
    table_body = get_table_body(driver)
    
    for row in table_body.find_elements(By.TAG_NAME, "tr"):
        for button_type in ["close", "edit"]:
            button = row.find_element(By.XPATH, f".//div[contains(@data-testid, 'button-{button_type}')]")
            is_disabled = is_element_disabled_by_cursor(driver, element=button)
            assert is_disabled, f"Expected '{button_type.capitalize()}' button to be disabled"
            

def verify_bulk_button_disabled(driver, tab_order_type, bulk_test_id):
    """Verify that the bulk action button is disabled in a given order panel tab."""
    type_orderPanel(driver, tab_order_type)
    spinner_element(driver)
    
    bulk_orderType = find_element_by_testid(driver, data_testid=bulk_test_id)
    bulk_is_disabled = is_element_disabled_by_cursor(driver, element=bulk_orderType)
    # print(f"\nTab: {tab_order_type}, Bulk Button Disabled: {bulk_is_disabled}")
    assert bulk_is_disabled, f"Expected '{bulk_test_id}' button to be disabled"
    verify_order_panel_button_disabled(driver)
    
    

def verify_read_only_access(driver, tab_order_type, bulk_test_id):
    
    """Verify read-only access restrictions by checking UI elements and bulk actions."""
    menu_button(driver, menu="assets")  # Navigate to "Assets"
    
    type_orderPanel(driver, tab_order_type)
    spinner_element(driver)
    
    table_body = get_table_body(driver)
    first_row = table_body.find_elements(By.TAG_NAME, "tr")[0]
    symbol_name = first_row.find_element(By.XPATH, ".//td[contains(@data-testid, 'column-symbol')]/span")
    click_element(element=symbol_name)
    spinner_element(driver)
    
    # Retrieve "This symbol is for view only" message
    message = find_visible_element_by_xpath(driver, "//div[@class='sc-xc0b2i-1 XQXKK']")
    attach_text(get_label_of_element(element=message), name=f"Trade - {tab_order_type}")

    verify_bulk_button_disabled(driver, tab_order_type, bulk_test_id)




def read_only_access(driver, set_menu: bool = False):
    """Run read-only access verification for various order panel tabs."""
    try:
        
        tab_actions = {
            "open-positions": "bulk-close",
            "pending-orders": "bulk-delete"
        }
        
        if set_menu:
            for tab, test_id in tab_actions.items():
                verify_read_only_access(driver, tab_order_type=tab, bulk_test_id=test_id)
        else:
            menu_button(driver, menu="assets")  # Navigate to "Assets"
            for tab, test_id in tab_actions.items():
                verify_bulk_button_disabled(driver, tab_order_type=tab, bulk_test_id=test_id)
    
    except Exception as e:
        handle_exception(driver, e)


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



