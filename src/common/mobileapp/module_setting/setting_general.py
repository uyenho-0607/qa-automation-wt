from constants.element_ids import DataTestID

from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception
from constants.helper.element_android_app import visibility_of_element_by_xpath, wait_for_element_clickable_xpath, click_element

from common.mobileapp.module_subMenu.sub_menu import menu_button

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SETTING DROPDOWN OPTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_setting(driver, setting_option: str, menu: bool = True):
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
            menu_button(driver, menu="assets")
        
            # Click on the settings button to open the dropdown
            btn_setting = wait_for_element_clickable_xpath(driver, DataTestID.APP_SETTING_BUTTON.value)
            click_element(element=btn_setting)
            
        
        button_testids = {
            "switch-to-live": DataTestID.SETTING_OPTION_SWITCH_TO_LIVE.value,
            "switch-to-demo": DataTestID.SETTING_OPTION_SWITCH_TO_DEMO.value,
            "open-demo-account": DataTestID.SETTING_OPTION_OPEN_DEMO_ACCOUNT.value,
            "payment-method": DataTestID.SETTING_OPTION_PAYMENT_METHOD.value,
            'one-click-trading': DataTestID.SETTING_OPTION_OCT.value,
            "language": DataTestID.SETTING_OPTION_LANGUGAGE.value,
            "appearance": DataTestID.SETTING_OPTION_APPEARANCE.value,
            "notification-setting": DataTestID.SETTING_OPTION_NOTIFICATION_SETTING.value,
            "change-password": DataTestID.APP_SETTING_OPTION_CHANGE_PASSWORD.value,
            "linked-device": DataTestID.SETTING_OPTION_LINKED_DEVICE.value,
            "biometrics-setting": DataTestID.SETTING_OPTION_BIOMETRICS_SETTING.value,
            "request-cancel-account": DataTestID.SETTING_OPTION_REQUEST_CANCEL_ACCOUNT.value,
            "help-support": DataTestID.SETTING_OPTION_HELP_SUPPORT.value,
            "logout": DataTestID.APP_SETTING_OPTION_LOGOUT.value
        }
        
        button_testid = button_testids.get(setting_option)
        if not button_testid:
            raise ValueError(f"Invalid button type: {setting_option}")
        
        # Click on the specified setting option
        dropdown_option = wait_for_element_clickable_xpath(driver, button_testid)
        delay(0.5)
        click_element(dropdown_option)

        # # Mapping setting options to expected text
        # expected_text_map = {
        #     "change-password": "Change Password",
        #     "open-demo-account": "Open a Demo Account",
        #     "notification-setting": "Notification Settings",
        #     "linked-device": "Linked Devices",
        #     "contact-information": "Contact Information"
        # }
        
        # delay(1)
        
        # if setting_option in expected_text_map:
        #     expected_text = expected_text_map[setting_option]
        #     match = wait_for_text_to_be_present_in_element_by_xpath(driver, f"//div[contains(normalize-space(text()), '{expected_text}')]", text=expected_text),
        #     if not match:
        #         raise AssertionError(f"Expected to display '{expected_text}' modal")
        
        if setting_option == "logout":
            assert visibility_of_element_by_xpath(driver, DataTestID.APP_LOGIN_LOGO.value)
        
    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""