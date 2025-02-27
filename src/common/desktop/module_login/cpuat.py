import os
import json
import traceback

from constants.helper.screenshot import take_screenshot
from constants.helper.driver import access_url, wait, switch_to_new_window
from constants.helper.element import click_element, find_element_by_xpath, populate_element, find_element_by_xpath_with_wait, click_element_with_wait, populate_element_with_wait

from data_config.encrypt_decrypt import decrypt_and_print

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                LAUNCH CPUAT WEBSITE 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def launch_cpuat(self, platform: str = None, env_type: str = None, sub_type: str = None) -> None:
    try:
        
        # Read URLs from the JSON file
        file_path = os.path.join("src/data_config/urls.json")
        with open(file_path, 'r') as file:
            urls = json.load(file)

        # Handle the special case for "CPUAT"
        if platform == "CPUAT":
            params_wt_url = urls["CPUAT"]
        else:
            # Check for the platform, env_type, and sub_type in the JSON
            if platform not in urls or env_type not in urls[platform] or sub_type not in urls[platform][env_type]:
                raise ValueError(f"Unsupported environment type: {platform} {env_type} {sub_type}")

            params_wt_url = urls[platform][env_type][sub_type]

        # Access the URL with optimized loading techniques
        access_url(self.driver, params_wt_url)

        wait(self.driver)

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(self.driver, "Launch_wt - Exception Screenshot")
        # Log the full exception message and stacktrace
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CPUAT USER LOGIN
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def cpuat_user_login(self, platform: str, testcaseID: str) -> None:
    try:
        
        file_path = os.path.join("src/data_config/credential.json")
        
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
        
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
        
        user_input_element = find_element_by_xpath(self.driver, "//input[@id='username']")
        
        populate_element_with_wait(self.driver, user_input_element, str(login_username))
        
        password_input_element = find_element_by_xpath(self.driver, "//input[@id='password']")
        
        populate_element(password_input_element, str(login_password))
        
        take_screenshot(self.driver, "input_credential")
        
        submit_button_element = find_element_by_xpath(self.driver, "//button[@id='btnCustomerLogin']")
        
        click_element(submit_button_element)
        
        take_screenshot(self.driver, "success_login")

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(self.driver, "login_cpuat - Exception Screenshot")
        # Log the full exception message and stacktrace
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                REDIRECT TO WT WEBSITE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def btn_webTrader(self):
    try: 
        cpuat_webTrader = find_element_by_xpath_with_wait(self.driver, "//span[contains(text(),'Web Trader')]")
        
        click_element_with_wait(self.driver, element=cpuat_webTrader)

        switch_to_new_window(self.driver)

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(self.driver, "btn_webTrader - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                LOGIN STEP
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Login to CPUAT Website
def login_cpuat(self, platform: str, testcaseID: str, env_type: str = None, sub_type: str = None) -> None:
    try:
            
        launch_cpuat(self, platform, env_type, sub_type)

        cpuat_user_login(self, platform, testcaseID)

        btn_webTrader(self)
        
        # login_cpuat(self, platform="CPUAT", testcaseID="TC01")
        
    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(self.driver, "login_cpuat - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""