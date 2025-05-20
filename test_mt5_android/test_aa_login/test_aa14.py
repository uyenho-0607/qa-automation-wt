import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import forgot_password


@allure.parent_suite("Membersite - Android - Login")

@allure.epic("MT5 Android TS_aA - Login")

# Member Portal
class TC_MT5_aA14():

    @allure.title("TC_MT5_aA14")

    @allure.description(
        """
        Forgot Password via Live
        """
    )
    
    def test_tc14(self, android_driver):
        self.driver = android_driver
        main_driver = self.driver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        start_recording_mobile(driver=main_driver)
        
        try:

            with allure.step("Launch Web Trader Membersite and click on Forgot Password button"):
                forgot_password(driver=main_driver, email="test@test.com", accountID="188183338")
                
        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)