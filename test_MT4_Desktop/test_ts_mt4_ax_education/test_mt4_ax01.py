import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_education.education import education_video


@allure.parent_suite("MT4 Membersite - Desktop - Education Video")

@allure.epic("MT4 Desktop ts_ax - Education Video")

# Member Portal
class TC_mt4_ax01():

    @allure.title("tc_mt4_ax01")

    @allure.description(
        """
        Ensure the video can be played
        """
        )
    
    def test_tc01(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")
                
            with allure.step("Verify the video is playing"):
                education_video(driver=main_driver)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
