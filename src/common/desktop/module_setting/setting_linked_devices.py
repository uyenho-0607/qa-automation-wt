import random

from enums.main import Setting

from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, find_element_by_xpath, find_list_of_elements_by_xpath

from common.desktop.module_setting.utils import button_setting
from common.desktop.module_markets.markets_watchlist import handle_alert_success


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                NOTIFICATION SETTING MODAL - LINKED DEVICES
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def linked_devices_modal(driver, set_terminate: bool = True):
    try:
        
        # Open the "Linked Devices" modal dialog
        button_setting(driver, setting_option=Setting.LINKED_DEVICE)
        
        if set_terminate:
            # Click on the terminate button
            btn_terminate = find_element_by_xpath(driver, "//div[@class='sc-1b49kuv-0 sc-5juhuq-0 eyDFgk bwVZIu']")
            click_element(btn_terminate)
            
            alert_msg = handle_alert_success(driver)
            if alert_msg != "Session terminated successfully":
                assert False, f"Receive {alert_msg} instead of the expected message"
        else:
            terminate_single = find_list_of_elements_by_xpath(driver, "(//div[@class='sc-6to9kt-4 dNMFZG'])[2]/div")
            initial_count = len(terminate_single)  # Store the initial count
            print(initial_count)
                        
            terminate_single_active_sessions = find_list_of_elements_by_xpath(driver, "//div[@class='sc-1b49kuv-4 fCLekE']")
            if terminate_single_active_sessions:
                random_symbol = random.choice(terminate_single_active_sessions) # Randomly choose one symbol from the list
                click_element(random_symbol)  # Click on the selected symbol
                    
                alert_msg = handle_alert_success(driver)
                if alert_msg != "Session terminated successfully":
                    assert False, f"Receive {alert_msg} instead of the expected message"
                
                # Get the updated count and verify
                updated_count = len(find_list_of_elements_by_xpath(driver, "(//div[@class='sc-6to9kt-4 dNMFZG'])[2]/div"))
                if updated_count != initial_count - 1:
                    assert False, f"Expected {initial_count - 1} active sessions, but found {updated_count}"

        # Click on the 'X' button
        btn_close = find_element_by_xpath(driver, "//div[@class='sc-ur24yu-4 jgnDww']//*[name()='svg']")
        click_element(btn_close)
    
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e) 
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""