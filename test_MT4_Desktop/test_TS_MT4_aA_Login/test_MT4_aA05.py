import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_video_to_allure
from common.desktop.module_login.utils import login_wt


@allure.epic("MT4 Desktop TS_aA - Login")

# Member Portal - Login via Demo CMS account
class TC_MT4_aA05():
               
    @allure.title("TC_MT4_aA05")

    @allure.description(
        """
        Member unable login with wrong credentials in CRM Live tab
        - correct accountID with wrong password
        """
        )
    
    def test_TC05(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        ffmpeg_process, screen_recording_file = start_screen_recording(class_name)
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT4", client_name="Lirunex", account_type="crm", testcaseID="TC01", expect_failure=True) 

        finally:
            stop_screen_recording(ffmpeg_process)
                        
            shutdown(main_driver)

            attach_video_to_allure(screen_recording_file, class_name)
