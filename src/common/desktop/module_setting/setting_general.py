from constants.helper.color_element import get_body_color
from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, find_element_by_testid, visibility_of_element_by_xpath


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SETTING DROPDOWN OPTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_setting(driver, setting_option):
    """
    To navigate to a specific setting option and perform actions based on the setting selected.

    Arguments:
    - setting_option: The setting option to be selected, such as "change-password" or "open-demo-account".

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Find and click on the setting button to open the settings dropdown
        setting = find_element_by_testid(driver, data_testid="setting-button")
        click_element(setting)
        
        # Find and click on the specific setting option based on the provided setting_option parameter
        dropdown_option = find_element_by_testid(driver, data_testid=f"setting-option-{setting_option}")
        click_element(dropdown_option)
        
        # Additional steps based on the selected setting option
        if setting_option == "change-password":
            # Wait for the "change-password" section to become visible (indicating it's loaded)
            visibility_of_element_by_xpath(driver, "//div[@class='sc-ur24yu-1 bDuvIg']")

        if setting_option == "open-demo-account":
            # Wait for the "open-demo-account" section to become visible (indicating it's loaded)
            visibility_of_element_by_xpath(driver, "//div[@class='sc-ur24yu-1 eqxJBS']")

    except Exception as e:
        # Handle any exceptions that occur during the execution
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
                    print("Unexpected color for System theme", color)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""