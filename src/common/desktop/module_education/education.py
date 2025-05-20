
import random

from enums.main import Menu
from constants.helper.driver import delay, get_current_url, switch_to_new_window
from constants.helper.element import spinner_element, javascript_click, click_element, find_list_of_elements_by_xpath, find_visible_element_by_xpath, is_element_present_by_xpath
from constants.helper.error_handler import handle_exception

from common.desktop.module_sub_menu.sub_menu import menu_button


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                LAUNCH CPUAT WEBSITE 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def education_video(driver):
    try:
        
        # Redirect to the Markets page
        menu_button(driver, menu=Menu.EDUCATION)

        spinner_element(driver)
        
        # Delay to allow elements to load
        delay(2)
        
        # find the list of the education list
        education_lists = find_list_of_elements_by_xpath(driver, "//div[contains(@class, 'sc-10lehzk-0 fVYmwG')]")
        if not education_lists:
            assert False, "Page is empy"
        
        # Select a random deposit option from the dropdown
        random_deposit_option = random.choice(education_lists)
        
        # Click the randomly selected deposit option
        click_element(element=random_deposit_option)
        
        delay(2)
        
        if is_element_present_by_xpath(driver, "//iframe[@id='widget2']"):
            # Switch to iframe - video
            iframe = find_visible_element_by_xpath(driver, "//iframe[@id='widget2']")
            driver.switch_to.frame(iframe)
            
            # Click on the play button
            btn_video_play = find_visible_element_by_xpath(driver, "//button[@class='ytp-large-play-button ytp-button ytp-large-play-button-red-bg']")
            javascript_click(driver, element=btn_video_play)
            
            # Check if the video is playing
            is_playing = driver.execute_script("return arguments[0].paused;", btn_video_play)

            if not is_playing:
                print("Video is playing")
            else:
                assert False, "Video is NOT playing"
        else:
            assert False, "No video is displayed"
            
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                VIDEO REDIRECTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def video_redirection(driver):
    try:
        
        # Redirect to the Markets page
        menu_button(driver, menu=Menu.EDUCATION)

        spinner_element(driver)
        
        # Delay to allow elements to load
        delay(2)
        
        # find the list of the education list
        education_lists = find_list_of_elements_by_xpath(driver, "//div[contains(@class, 'sc-10lehzk-0 fVYmwG')]")
        if not education_lists:
            assert False, "Page is empy"
        
        # Select a random deposit option from the dropdown
        random_deposit_option = random.choice(education_lists)
        
        # Click the randomly selected deposit option
        click_element(element=random_deposit_option)
        
        delay(2)
        
        if is_element_present_by_xpath(driver, "//iframe[@id='widget2']"):
            # Switch to iframe - video
            iframe = find_visible_element_by_xpath(driver, "//iframe[@id='widget2']")
            driver.switch_to.frame(iframe)
            
            # Click on the play button
            btn_video_redirection = find_visible_element_by_xpath(driver, "//a[@class='ytp-impression-link']")
            javascript_click(driver, element=btn_video_redirection)
            
            switch_to_new_window(driver)
            
            # Get the current URL after logout
            current_url = get_current_url(driver)
            
            # Assert that the URL should change to the login page
            if "youtube.com" in current_url:
                print("Redirect to youtube website: ", current_url)
            else:
                # Raise an assertion error
                assert False, "Expected to redirect to youtube website"
        else:
            assert False, "No video is displayed"
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
