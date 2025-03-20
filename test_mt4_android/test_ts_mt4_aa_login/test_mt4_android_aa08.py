import allure
from enums.main import Server, LoginResultState

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import select_account_type, splash_screen, login_wt, toggle_remember_me_checkbox, verify_login_fields


@allure.parent_suite("Membersite - Android - Login")

@allure.epic("MT4 Android TS_aA - Login")

# Member Portal
class TC_MT4_aA08():

    @allure.title("TC_MT4_aA08")

    @allure.description(
        """
        Verify that the system saves the last successful login credentials when [Remember Me] is checked and does not remember incorrect credentials.
        """
    )
    
    def test_tc08(self, android_driver):
        self.driver = android_driver
        main_driver = self.driver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        start_recording_mobile(driver=main_driver)
        
        try:
            with allure.step("Check the 'Rmb me' checkbox > Login to Web Trader Membersite > logout"):
                username, password = toggle_remember_me_checkbox(driver=main_driver, server=Server.MT4)
                
            with allure.step("Input incorrect credential"):
                login_wt(driver=main_driver, server=Server.MT4, testcase_id="TC02", expectation=LoginResultState.FAILURE) 

            with allure.step("Terminate and relaunch the current active app package"):
                current_app_package = main_driver.current_package  # Get the active app package
                print(f"APP packaing: {current_app_package}")
                
                main_driver.terminate_app(current_app_package)  # Terminate the app
                main_driver.activate_app(current_app_package)  # Relaunch the app
                
            with allure.step("Skip splash screen"):
                # Skip the splash screen
                splash_screen(driver=main_driver)

            with allure.step("Click on the 'LIVE' Account tab"):
                # Step 2: Select the desired account type (either CRM / Live or Demo) for login.
                select_account_type(driver=main_driver)
                
            with allure.step("Validate the system does not rmb incorrect credential entered previously"):
                verify_login_fields(driver=main_driver, expected_username=username, expected_password=password)
                
        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)