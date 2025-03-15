import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import toggle_remember_me_checkbox


@allure.parent_suite("Membersite - Android - Login")

@allure.epic("MT4 Android TS_aA - Login")

# Member Portal
class TC_MT4_aA08():

    @allure.title("TC_MT4_aA08")

    @allure.description(
        """
        Verify that the [Remember Me] feature does not apply to Demo tab
        """
    )
    
    def test_tc08(self, android_driver):
        self.driver = android_driver
        main_driver = self.driver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        start_recording_mobile(driver=main_driver)
        
        try:
            with allure.step("Login to Web Trader Membersite"):
                toggle_remember_me_checkbox(driver=main_driver, server="MT4", client_name="Lirunex", testcaseID="TC01", kick_user=False)

        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)