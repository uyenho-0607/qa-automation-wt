import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_education.education import education_video


@allure.parent_suite("MT5 Membersite - Desktop - Education Video")

@allure.epic("MT5 Desktop ts_aw - Education Video")

# Member Portal
class TC_mt5_aw01():

    @allure.title("tc_mt5_aw01")

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
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5")
                
            with allure.step("Verify the video is playing"):
                education_video(driver=main_driver)

        finally:          
            shutdown(main_driver)

            attach_session_video_to_allure(session_id)
