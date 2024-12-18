import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import button_setting


@allure.epic("MT4 Desktop TS_aA - Login")

# Member Portal - Login via Demo CMS account
class TC_MT4_aA04():
            
    @allure.title("TC_MT4_aA04")

    @allure.description(
        """
        Member able login to Web Trader via Demo Account tab
        """
        )
    
    def test_TC04(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        ffmpeg_process, screen_recording_file = start_screen_recording(class_name)
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT4", client_name="Lirunex", account_type="demo")
             
            with allure.step("Successfully Logout"):
                button_setting(driver=main_driver, setting_option="logout")

        finally:
            stop_screen_recording(ffmpeg_process)
                        
            shutdown(main_driver)

            attach_video_to_allure(screen_recording_file, class_name)
