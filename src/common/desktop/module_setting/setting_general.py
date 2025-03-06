from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception

from constants.helper.color_element import get_body_color
from constants.helper.element import click_element, find_element_by_testid, javascript_click, visibility_of_element_by_xpath, visibility_of_element_by_testid, wait_for_text_to_be_present_in_element_by_xpath





"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SETTING ACCOUNT INFORMATION TAB
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def accountInformation(driver):
    # To open the account linkage profile
    accountInfo = find_element_by_testid(driver, data_testid="account-selector")
    javascript_click(driver, element=accountInfo)
    
    delay(2)
    
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SETTING DROPDOWN OPTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
        
def button_setting(driver, setting_option: str):
    """
    Navigates to a specific setting option and performs actions based on the selected setting.

    Arguments:
    - driver: Selenium WebDriver instance.
    - setting_option: The setting option to be selected (e.g., "change-password", "open-demo-account", "notification-setting").

    Raises:
    - AssertionError: If the expected modal is not displayed.
    - ValueError: If the "Notification Settings" text is not found.
    """
    try:
        # Click on the settings button to open the dropdown
        click_element(find_element_by_testid(driver, data_testid="setting-button"))
        
        # Click on the specified setting option
        dropdown_option = visibility_of_element_by_testid(driver, data_testid=f"setting-option-{setting_option}")
        click_element(dropdown_option)

        # Mapping setting options to expected text
        expected_text_map = {
            "change-password": "Change Password",
            "open-demo-account": "Open a Demo Account",
            "notification-setting": "Notification Settings",
            "linked-device": "Linked Devices",
            "contact-information": "Contact Information"
        }
        
        delay(1)
        # demo-account-completion-modal-title
        # change-password-modal-title
        # demo-account-creation-modal-title
        
        if setting_option in expected_text_map:
            expected_text = expected_text_map[setting_option]
            match = wait_for_text_to_be_present_in_element_by_xpath(driver, f"//div[contains(normalize-space(text()), '{expected_text}')]", text=expected_text),
            if not match:
                raise AssertionError(f"Expected to display '{expected_text}' modal")

    except Exception as e:
        handle_exception(driver, e)

        

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SETTING - THEME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_theme(driver, theme_option=None):
    """
    To test the theme change (Light, Dark, System) in the application.

    Arguments:
    - theme_option: Optional parameter to specify a specific theme to select. If None, the function will iterate over all theme options.
    
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    
    # List of all theme options
    themes = ["Light", "Dark", "System"] if theme_option is None else [theme_option]

    try:
        # Iterate through the theme options (either all or the specified one)
        for option in themes:
            
            # Click on the theme switch button to open the theme dropdown
            setting = find_element_by_testid(driver, data_testid="switch-theme-button")
            click_element(setting)
            
            # Wait for and click the dropdown option for the current theme (Light, Dark, or System)
            dropdown_option = visibility_of_element_by_xpath(driver, f"//div[@class='sc-13nyl38-4 eQA-dBj' and text()='{option}']")
            click_element(dropdown_option)
            
            # Verify the page color after selecting each theme option
            if option == "Light":
                color = get_body_color(driver)
                assert color == "rgb(0, 9, 9)", "Light theme color mismatch, Expected rgb(0, 9, 9)"
            elif option == "Dark":
                color = get_body_color(driver)
                assert color == "rgb(234, 236, 239)", "Dark theme color mismatch, Expected rgb(234, 236, 239)"
            elif option == "System":
                color = get_body_color(driver)
                # Check the detected color for the System theme setting
                if color == "rgb(0, 9, 9)":
                    print("Light theme detected in System settings")
                elif color == "rgb(234, 236, 239)":
                    print("Dark theme detected in System settings")
                else:
                    assert False, f"Unexpected color for System theme {color}"

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""