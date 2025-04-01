import random

from enums.main import Setting, SettingLanguageMap
from constants.element_ids import DataTestID
from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, find_element_by_testid, find_list_of_elements_by_xpath, get_label_of_element

from common.desktop.module_setting.setting_general import button_setting


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SETTING CHANGE LANGUAGE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def configure_language_setting333(driver):
    try:
        # Loop to change language 3 times
        for _ in range(3):
            
            # Step 1: Click on the setting > language
            button_setting(driver, setting_option=Setting.LANGUAGE)

            # Step 2: Find the list of available languages
            languages_options = find_list_of_elements_by_xpath(driver, DataTestID.SETTING_OPTION_LANGUGAGE_ITEMS)

            # Step 3: Randomly select a language
            random_language = random.choice(languages_options)
            selected_language = get_label_of_element(random_language)

            print(f"Selected language: {selected_language}")

            # Step 4: Click on the selected language
            click_element(element=random_language)

            # Language map to match the selected language with the expected button text
            language_map = {
                "English": "Trade",
                "简体中文": "交易",
                "繁体中文": "交易",
                "ภาษาไทย": "เทรด",
                "Tiếng Việt": "Giao dịch",
                "Melayu": "Perdagangan",
                "Bahasa Indonesia": "Berdagang",
                "Japanese": "取引",
                "Korean": "거래",
                "Arabic": "التداول."
            }

            # Get the expected value from the language map
            expected_text = language_map.get(selected_language)

            # Step 5: Verify if the change is reflected
            submit_button = find_element_by_testid(driver, data_testid=DataTestID.SIDE_BAR_OPTION_TRADE)
            button_text = submit_button.text.strip()

            # Compare the button text with the expected text
            if button_text == expected_text:
                print(f"Language '{selected_language}' matches the expected text {expected_text}\n")
            else:
                assert False, f"Verification failed for language '{selected_language}', Expected: '{expected_text}', Found: '{button_text}'"

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



def configure_language_setting(driver):
    """
    Selects and verifies different languages in the settings.

    Args:
        driver (webdriver): Selenium WebDriver instance.
    """
    try:
        for _ in range(3):  # Repeat 3 times
            
            # Step 1: Open language settings
            button_setting(driver, setting_option=Setting.LANGUAGE)

            # Step 2: Get all available language options
            languages_options = find_list_of_elements_by_xpath(driver, DataTestID.SETTING_OPTION_LANGUGAGE_ITEMS)

            # Step 3: Randomly select a language
            random_language = random.choice(languages_options)
            selected_language = get_label_of_element(random_language)

            print(f"Selected language: {selected_language}")

            # Step 4: Click on the selected language
            click_element(element=random_language)

            # Get the expected button text using the optimized LanguageMap lookup
            expected_text = SettingLanguageMap.get_expected_text(selected_language)

            # Step 5: Verify if the change is reflected
            submit_button = find_element_by_testid(driver, data_testid=DataTestID.SIDE_BAR_OPTION_TRADE)
            button_text = submit_button.text.strip()

            # Compare the button text with the expected text
            assert button_text == expected_text, (
                f"Verification failed for language '{selected_language}', "
                f"Expected: '{expected_text}', Found: '{button_text}'"
            )
            print(f"Language '{selected_language}' matches the expected text '{expected_text}'\n")

    except Exception as e:
        handle_exception(driver, e)