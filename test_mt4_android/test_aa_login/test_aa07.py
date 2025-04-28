import allure

from enums.main import Server, Setting
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import login_wt
from common.mobileapp.module_setting.utils import button_setting


@allure.parent_suite("Membersite - Android - Login")

@allure.epic("MT4 Android TS_aA - Login")

# Member Portal
class TC_MT4_aA07():

    @allure.title("TC_MT4_aA07")

    @allure.description(
        """
        Members can select a language from the login page, and the selected language is applied upon login.
        """
    )
    
    def test_tc07(self, android_driver):
        self.driver = android_driver
        main_driver = self.driver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        start_recording_mobile(driver=main_driver)
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT4, set_language=True)
                
            with allure.step("Successfully Logout"):
                button_setting(driver=main_driver, setting_option=Setting.LOGOUT)
                
        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)