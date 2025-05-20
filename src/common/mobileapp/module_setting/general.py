from enums.main import Menu, Setting
from constants.element_ids import DataTestID

from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception
from constants.helper.element_android_app import find_visible_element_by_xpath, find_element_by_xpath_with_wait, click_element

from common.mobileapp.module_sub_menu.sub_menu import menu_button

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SETTING DROPDOWN OPTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_setting(driver, setting_option: Setting, menu: bool = True):
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
        
        if menu:
            menu_button(driver, menu=Menu.ASSETS)
        
            # Click on the settings button to open the dropdown
            btn_setting = find_element_by_xpath_with_wait(driver, DataTestID.APP_SETTING_BUTTON)
            click_element(element=btn_setting)
        
        button_testids = {
            Setting.SWITCH_TO_LIVE: DataTestID.SETTING_OPTION_SWITCH_TO_LIVE,
            Setting.SWITCH_TO_DEMO: DataTestID.SETTING_OPTION_SWITCH_TO_DEMO,
            Setting.OPEN_DEMO_ACCOUNT: DataTestID.SETTING_OPTION_OPEN_DEMO_ACCOUNT,
            Setting.PAYMENT_METHOD: DataTestID.SETTING_OPTION_PAYMENT_METHOD,
            Setting.ONE_CLICK_TRADING: DataTestID.SETTING_OPTION_OCT,
            Setting.LANGUAGE: DataTestID.SETTING_OPTION_LANGUGAGE,
            Setting.APPEARANCE: DataTestID.SETTING_OPTION_APPEARANCE,
            Setting.NOTIFICATION_SETTING: DataTestID.SETTING_OPTION_NOTIFICATION_SETTING,
            Setting.CHANGE_PASSWORD: DataTestID.APP_SETTING_OPTION_CHANGE_PASSWORD,
            Setting.LINKED_DEVICE: DataTestID.SETTING_OPTION_LINKED_DEVICE,
            Setting.BIOMETRICS_SETTING: DataTestID.SETTING_OPTION_BIOMETRICS_SETTING,
            Setting.REQUEST_CANCEL_ACCOUNT: DataTestID.SETTING_OPTION_REQUEST_CANCEL_ACCOUNT,
            Setting.HELP_SUPPORT: DataTestID.SETTING_OPTION_HELP_SUPPORT,
            Setting.LOGOUT: DataTestID.APP_SETTING_OPTION_LOGOUT
        }
        
        button_testid = button_testids.get(setting_option)
        if not button_testid:
            raise ValueError(f"Invalid button type: {setting_option}")
        
        # Click on the specified setting option
        dropdown_option = find_element_by_xpath_with_wait(driver, button_testid)
        delay(0.5)
        click_element(dropdown_option)

        if setting_option == Setting.LOGOUT:
            assert find_visible_element_by_xpath(driver, DataTestID.APP_LOGIN_LOGO)
        
    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""