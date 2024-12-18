import os
import json
import traceback

from data_config.encrypt_decrypt import decrypt_and_print
from constants.helper.element_android_app import find_element_by_xpath, click_element, click_element_with_wait, populate_element_with_wait, visibility_of_element_by_testid
from constants.helper.screenshot import take_screenshot



def check_symbol_element_present(driver):
    """Check if the user is already logged in by searching for an element that only appears after login """
    try:
        
        search_input = visibility_of_element_by_testid(driver, data_testid="symbol-search-selector")
        
        # element = driver.find_element_by_xpath("//*[@resource-id='logout-button']")
        return search_input.is_displayed()
    
    except:
        return False


def login_wt(driver, account_type, platform: str, testcaseID: str) -> None:
    
    try:
        
        splash_screen = visibility_of_element_by_testid(driver, data_testid="ads-skip-button")
        click_element(splash_screen)
        
        # Check if user is already logged in by looking for an element that is only present in login screen
        if check_symbol_element_present(driver):
            print("User is already logged in, skipping login steps.")
            return
        
        file_path = os.path.join("src/data_config/credential.json")
        
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
        
        select_account_type(driver, account_type)

        # Retrieve username and password from JSON data based on testcaseID
        if platform in data:
            for testcase in data[platform]:
                if testcase["TestcaseID"] == testcaseID:
                    login_username_encrypted = testcase["Username"]
                    login_password_encrypted = testcase["Password"]
                    break
            else:
                raise ValueError(f"Testcase ID '{testcaseID}' not found for platform '{platform}'")
        else:
            raise ValueError(f"Platform '{platform}' not found in credential data")
                    
        # Decrypt the credentials
        login_username = decrypt_and_print(login_username_encrypted)
        login_password = decrypt_and_print(login_password_encrypted)

        # Assuming these functions exist in your automation framework
        username_input = visibility_of_element_by_testid(driver, data_testid="login-user-id")
        populate_element_with_wait(driver, element=username_input, text=login_username)

        password_input = visibility_of_element_by_testid(driver, data_testid="login-password")
        populate_element_with_wait(driver, element=password_input, text=login_password)

        # Submit login
        # submit_button = find_element_by_testid(driver, "//*[@resource-id='login-submit']")
        submit_button = find_element_by_xpath(driver, "//android.widget.TextView[@text='Sign in']")
        # click_element(submit_button)
        click_element_with_wait(driver, element=submit_button)

    except Exception as e:
        take_screenshot(driver, "login_wt - Exception Screenshot")
        assert False, f"{str(e)}\n{traceback.format_exc()}"
        

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ACCOUNT TYPE SELECTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def select_account_type(driver, account_type):
    try:
        
        acct_type_selector = visibility_of_element_by_testid(driver, data_testid=f"tab-login-account-type-{account_type}")
        
        click_element(acct_type_selector)
        
        # Capture network logs
        # network_logs = capture_network_logs(driver)
        # attach_network_logs_to_allure(network_logs, log_name="Network Logs - Select Account Type")
        
        return acct_type_selector
    
    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "select_account_type - Exception Screenshot")
        # Log the full exception message and stacktrace
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


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
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "menu_button - Exception Screenshot")
        # Log the full exception message and stacktrace
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""