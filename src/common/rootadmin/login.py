import os
import json
import base64
import random
import pytesseract
from io import BytesIO

# Adjusting preprocessing steps again for better accuracy
from PIL import Image

from constants.helper.error_handler import handle_exception
from data_config.encrypt_decrypt import decrypt_and_print
from constants.helper.driver import access_url, delay
from constants.helper.screenshot import attach_text
from constants.helper.element import clear_input_field, find_element_by_xpath, get_label_of_element, populate_element_with_wait, visibility_of_element_by_xpath, wait_for_text_to_be_present_in_element_by_xpath
from data_config.file_handler import get_credentials



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                LAUNCH WT WEBSITE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# platform: The platform type (MT4, MT5, RootAdmin).
# client_name: The client name (Lirunex / Transactcloudmt5)
# device_type: The environment type (Desktop, Mobile, Backoffice).
# env_type: The specific sub-environment (SIT, Release_SIT, UAT).


def launch_RA(driver, platform: str, env_type: str) -> None:
    try:
        # Read URLs from the JSON file
        file_path = os.path.join("src/data_config/urls.json")
        with open(file_path, 'r') as file:
            urls = json.load(file)
        
        if platform == "RootAdmin":
            if env_type not in urls["RootAdmin"]:
                raise ValueError(f"Unsupported environment type for RootAdmin: {env_type}")
            params_wt_url = urls["RootAdmin"][env_type]

        # Access the URL with optimized loading techniques
        access_url(driver, params_wt_url)
        
    except Exception as e:
        handle_exception(driver, e)



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""




"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                WT BO LOGIN PAGE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def ra_user_login(driver, platform: str, testcaseID: str, expect_failure: bool = False, max_retries: int = 10) -> None:
    try:
        
        # Load credentials from the JSON file
        data = get_credentials()
        
        # Check if the platform exists in the data
        if platform in data:
            # If expect_failure is True, use Invalid_Credential and require testcaseID
            if expect_failure:
                if testcaseID is None:
                    raise ValueError("testcaseID must be provided for Invalid_Credential.")
                
                credential_type = "Invalid_Credential"
                valid_testcases = [testcase for testcase in data[platform].get(credential_type, [])
                                   if testcase["TestcaseID"] == testcaseID]
                if not valid_testcases:
                    raise ValueError(f"Testcase ID '{testcaseID}' not found in {credential_type} for platform '{platform}'")
                testcase = valid_testcases[0]
            else:
                # If expect_failure is False, decide between CRM_Credential or Credential without testcaseID
                credential_type = "Credential"
                
                if not data[platform].get(credential_type):
                    raise ValueError(f"No {credential_type} data available for platform '{platform}'")
                
                # Randomly pick a testcase from the selected credential list
                testcase = random.choice(data[platform][credential_type])
        
        # Retrieve the username and password from the selected testcase
        login_username_encrypted = testcase["Username"]
        login_password_encrypted = testcase["Password"]

        # Decrypt the credentials
        login_username = decrypt_and_print(login_username_encrypted)
        login_password = decrypt_and_print(login_password_encrypted)

        # Fill in the username and password fields
        username_input = visibility_of_element_by_xpath(driver, "(//input[contains(@class,'mantine-4eck0i')])[1]")
        populate_element_with_wait(driver, element=username_input, text=login_username)

        password_input = find_element_by_xpath(driver, "//input[@type='password']")
        populate_element_with_wait(driver, element=password_input, text=login_password)
        
        # Retry logic for login attempts
        for attempt in range(max_retries):
            read_captcha(driver)
            
            match = wait_for_text_to_be_present_in_element_by_xpath(driver, "//div[normalize-space(text())='Dashboard']", text="Dashboard")
            if match:
            # success_url = get_success_urls(platform, env_type)
            # if wait_for_url(driver, [success_url]):
                # Check if we expected failure but logged in successfully
                if expect_failure:
                    attach_text("Expected failure, but login succeeded without error. Test failed as expected failure condition not met.", name="Unexpected Success")
                    assert False, "Expected failure, but login succeeded without error. Test failed."
                else:
                    attach_text("Redirection to the correct website verified", name="Success")
                    assert True
                return
            
            # Handle error messages
            error_message = handle_login_error(driver)
            print(f"Attempt {attempt + 1} Error Message: ", error_message)

            if "Invalid credentials, please try again" in error_message:
                if expect_failure:
                    attach_text("Expected failure condition met.", name="Test passed as expected.")
                    assert True  # Pass the test if expected failure
                else:
                    assert False, "Invalid credentials error encountered. Test failed."
                return
            
            elif "Verification code invalid" in error_message:
                if attempt < max_retries - 1:
                    attach_text(error_message, name=f"Attempt {attempt + 1} failed: verification code invalid. Retrying...")
                    delay(0.5)
                    captcha_input = visibility_of_element_by_xpath(driver, "(//div[@class='mantine-Input-wrapper mantine-12sbrde']/input)[3]")
                    clear_input_field(captcha_input)
                else:
                    assert False, "Verification code invalid after maximum attempts. Test failed."
        
    except Exception as e:
        handle_exception(driver, e)


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                READ CAPTCHA
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def read_captcha(driver):
    # Thresholds and blurring sigma
    th1 = 140
    th2 = 140  
    sig = 1.5  


    # Find the CAPTCHA image element
    captcha_image_element = visibility_of_element_by_xpath(driver, "(//img)[2]")
    
    # Get the CAPTCHA image src (base64 string)
    captcha_image_src = captcha_image_element.get_attribute("src")
    
    # Extract base64 part from the src
    base64_image = captcha_image_src.split(",")[1]

    # Decode the base64 string to bytes
    image_bytes = base64.b64decode(base64_image)
    if not image_bytes:
        raise Exception("Failed to decode CAPTCHA image from base64.")
    
    # Decode the CAPTCHA
    image = Image.open(BytesIO(image_bytes))
    
    # Convert to black and white
    black_and_white = image.convert("L")
    black_and_white.save("black_and_white.png")

    # Apply the first threshold
    first_threshold = black_and_white.point(lambda p: p > th1 and 255)
    first_threshold.save("first_threshold.png")

    # Perform OCR using Tesseract
    result = pytesseract.image_to_string(first_threshold, lang='eng', config='--psm 7')

    # Print the result
    print(f"Captured CAPTCHA: {result}")

    # Find the input field for CAPTCHA entry
    captcha_input = find_element_by_xpath(driver, "(//input[contains(@class,'mantine-8va6cp')])[1]")
    
    # Populate the CAPTCHA input field with the best extracted numeric text
    populate_element_with_wait(driver, element=captcha_input, text=result)

    return result

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                RETRIEVE THE ERROR MESSAGE CONTENT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def handle_login_error(driver):
    try:
        # Handle the expected failure scenario
        error_message_notification = visibility_of_element_by_xpath(driver, "//div[@class='mantine-Text-root mantine-Notification-description mantine-1y9keh2']")
        error_message = get_label_of_element(error_message_notification)
        attach_text(error_message, name="Expected login failure. Error message found: ")
        return error_message
    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                LOGIN STEP
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Login to WebTrader Website Release_SIT
def login_RA(driver, platform: str = "RootAdmin", testcaseID: str = None, env_type: str = "Release_SIT", expect_failure: bool = False, max_retries: int = 10) -> None:
    try:

        launch_RA(driver, platform, env_type)
        
        ra_user_login(driver, platform, testcaseID, expect_failure, max_retries)

    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""