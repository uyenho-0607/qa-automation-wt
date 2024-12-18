import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_video_to_allure

from common.backoffice.login.utils import login_bo


@allure.epic("MT4 Admin Portal - Login")

# Admin Portal - Login to backoffice account
class TC_MT4_aA01():

    @allure.title("TC_MT4_aA01")

    @allure.description(
        """
        Member able login to Admin Portal
        """
        )
    
    def test_TC01(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        
        # Get the class name dynamically
        class_name = self.__class__.__name__
        ffmpeg_process, screen_recording_file = start_screen_recording(class_name)
        
        try:
            
            with allure.step("Login to Web Trader Admin Portal"):
                # login_bo(driver=main_driver, platform="MT4", client_name="Lirunex", testcaseID="TC01", expect_failure=True)
                login_bo(driver=main_driver, platform="MT4", client_name="Lirunex")

        finally:
            stop_screen_recording(ffmpeg_process)
            
            shutdown(main_driver)

            attach_video_to_allure(screen_recording_file, class_name)