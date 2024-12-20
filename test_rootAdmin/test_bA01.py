import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_session_video_to_allure

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
        session_id = main_driver.session_id
        
        # Get the class name dynamically
        start_screen_recording()
        
        try:
            
            with allure.step("Login to Web Trader Root Admin"):
                login_RA(driver=main_driver)

        finally:
            stop_screen_recording()
                        
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)