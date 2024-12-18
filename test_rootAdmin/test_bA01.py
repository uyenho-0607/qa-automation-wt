import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_video_to_allure

from common.rootadmin.login import login_RA


@allure.epic("Root Admin - Login")

# Root Admin - Login to Root Admin
class TC_MT4_aA01():

    @allure.title("TC_MT4_aA01")

    @allure.description(
        """
        Member able login to Root Admin
        """
        )
    
    def test_TC01(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        
        # Get the class name dynamically
        class_name = self.__class__.__name__
        ffmpeg_process, screen_recording_file = start_screen_recording(class_name)
        
        try:
            
            with allure.step("Login to Web Trader Root Admin"):
                login_RA(driver=main_driver)

        finally:
            stop_screen_recording(ffmpeg_process)
            
            shutdown(main_driver)

            attach_video_to_allure(screen_recording_file, class_name)