import random
from constants.element_ids import DataTestID

from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, click_element_with_wait, find_element_by_testid, find_list_of_elements_by_testid, find_visible_element_by_testid, get_label_of_element
from enums.main import LoginLanguageMap


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                LANGUAGE SELECTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def select_and_verify_language222(driver):
    """
    Randomly selects three different languages from the dropdown,
    verifies if the change is reflected on the login button, and repeats for each language.

    Args:
        driver (webdriver): Selenium WebDriver instance.
    """
    try:
        
        # Language map for verification values
        language_map = {
            "English": "Sign in",
            "简体中文": "登录",
            "繁体中文": "登錄",
            "ภาษาไทย": "เปิดบัญชีซื้อขายจริง",
            "Tiếng Việt": "Đăng nhập",
            "Melayu": "Log masuk",
            "Bahasa Indonesia": "Masuk",
            "Japanese": "ログイン",
            "Korean": "로그인"
        }

        # Step 1: Locate the language dropdown
        language_dropdown = find_visible_element_by_testid(driver, data_testid=DataTestID.LANGUAGE_DROPDOWN)

        # Step 2: Get all available language options
        click_element_with_wait(driver, element=language_dropdown)
        languages_options = find_list_of_elements_by_testid(driver, data_testid=DataTestID.LANGUAGE_OPTION)

        # Keep track of selected languages to avoid repetition
        selected_languages = []

        # Step 3: Select and verify languages
        for i in range(3):  # Repeat for 3 different random languages
            # Filter out languages already selected
            remaining_languages = [lang for lang in languages_options if lang.text not in selected_languages]

            if not remaining_languages:
                print("No more languages left to select.")
                break
            
            # Select random language from the choice
            random_language = random.choice(remaining_languages)
            
            # Get the language text
            selected_language = get_label_of_element(random_language)

            # Step 4: Click on the selected language
            click_element(element=random_language)
            
            # Delay to allow system to update
            delay(0.5)

            # Step 5: Verify if the change is reflected
            submit_button = find_element_by_testid(driver, data_testid=DataTestID.LOGIN_SUBMIT)
            button_text = get_label_of_element(element=submit_button)

            # Get the expected value from the language map
            expected_text = language_map.get(selected_language)
            
            # Compare the button text with the expected text
            assert button_text == expected_text, f"Verification failed for language '{selected_language}', Expected: '{expected_text}', Found: '{button_text}''"

            # Add the selected language to the list to avoid re-selection
            selected_languages.append(selected_language)
            
            # Only click dropdown again if it's **not the last iteration**
            if i < 2:  # Since range(3) means last index is 2
                click_element_with_wait(driver, element=language_dropdown)
                languages_options = find_list_of_elements_by_testid(driver, data_testid=DataTestID.LANGUAGE_OPTION)

        # Return the last successfully verified language
        return selected_language
    
    except Exception as e:
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                DEFAULT TO ENGLISH LANGUAGE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def select_english_language(driver):
    """
    Ensures that the application language is set to English.
    """
    # Step 1: Locate the language dropdown
    language_dropdown = find_visible_element_by_testid(driver, data_testid=DataTestID.LANGUAGE_DROPDOWN)
    language_label = get_label_of_element(language_dropdown).strip()
    
    # If the language is not English, to update the language to English
    if language_label != "English":
        click_element(element=language_dropdown)
        delay(0.5)

        # Step 4: Locate the language dropdown options
        languages_options = find_list_of_elements_by_testid(driver, data_testid=DataTestID.LANGUAGE_OPTION)

        # Step 5: Click on 'English' from the available options
        for option in languages_options:
            if get_label_of_element(option) == "English":
                click_element(element=option)
                break  # Stop once 'English' is clicked
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def select_and_verify_language(driver):
    """
    Randomly selects three different languages from the dropdown,
    verifies if the change is reflected on the login button, and repeats for each language.

    Args:
        driver (webdriver): Selenium WebDriver instance.
    """
    try:
        # Step 1: Locate the language dropdown
        language_dropdown = find_visible_element_by_testid(driver, data_testid=DataTestID.LANGUAGE_DROPDOWN)

        # Step 2: Get all available language options
        click_element_with_wait(driver, element=language_dropdown)
        languages_options = find_list_of_elements_by_testid(driver, data_testid=DataTestID.LANGUAGE_OPTION)

        # Keep track of selected languages to avoid repetition
        selected_languages = []

        # Step 3: Select and verify languages
        for i in range(3):  # Repeat for 3 different random languages
            # Filter out languages already selected
            remaining_languages = [lang for lang in languages_options if lang.text not in selected_languages]

            if not remaining_languages:
                print("No more languages left to select.")
                break
            
            # Select random language from the choice
            random_language = random.choice(remaining_languages)
            
            # Get the language text
            selected_language = get_label_of_element(random_language)

            # Step 4: Click on the selected language
            click_element(element=random_language)
            
            # Delay to allow system to update
            delay(0.5)

            # Step 5: Verify if the change is reflected
            submit_button = find_element_by_testid(driver, data_testid=DataTestID.LOGIN_SUBMIT)
            button_text = get_label_of_element(element=submit_button)

            # Get the expected value from the Enum
            expected_text = LoginLanguageMap.get_expected_text(selected_language)
            
            # Compare the button text with the expected text
            assert button_text == expected_text, f"Verification failed for language '{selected_language}', Expected: '{expected_text}', Found: '{button_text}''"

            # Add the selected language to the list to avoid re-selection
            selected_languages.append(selected_language)
            
            # Only click dropdown again if it's **not the last iteration**
            if i < 2:  # Since range(3) means last index is 2
                click_element_with_wait(driver, element=language_dropdown)
                languages_options = find_list_of_elements_by_testid(driver, data_testid="language-option")

        # Return the last successfully verified language
        return selected_language
    
    except Exception as e:
        handle_exception(driver, e)