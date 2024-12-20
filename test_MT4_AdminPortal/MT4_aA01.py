import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_session_video_to_allure

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
        session_id = main_driver.session_id
        
        # Get the class name dynamically
        start_screen_recording()
        
        try:
            
            with allure.step("Login to Web Trader Admin Portal"):
                # login_bo(driver=main_driver, platform="MT4", client_name="Lirunex", testcaseID="TC01", expect_failure=True)
                login_bo(driver=main_driver, platform="MT4", client_name="Lirunex")

        finally:
            stop_screen_recording()
                        
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)