import allure
from enums.main import AccountType

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import click_splash_screen, select_account_type, toggle_remember_me_checkbox, verify_login_fields



@allure.parent_suite("Membersite - Android - Login")

@allure.epic("MT5 Android TS_aA - Login")

# Member Portal
class TC_MT5_aA10():

    @allure.title("TC_MT5_aA10")

    @allure.description(
        """
        Verify that the [Remember Me] feature does not apply to Demo tab
        """
    )
    
    def test_tc10(self, android_driver):
        self.driver = android_driver
        main_driver = self.driver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        start_recording_mobile(driver=main_driver)
        
        try:

            with allure.step("Launch WT and Click on the 'Demo' Account tab"):
                # Skip the splash screen
                click_splash_screen(driver=main_driver)

                # Step 2: Select the desired account type (either CRM / Live or Demo) for login.
                select_account_type(driver=main_driver, account_type=AccountType.DEMO)
                
            with allure.step("Validate the fields is empty"):
                verify_login_fields(driver=main_driver, expected_username="", expected_password="")
                
        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)