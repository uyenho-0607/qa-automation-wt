import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_education.education import video_redirection


@allure.parent_suite("MT5 Membersite - Desktop - Education Video")

@allure.epic("MT5 Desktop ts_aw - Education Video")

# Member Portal
class TC_mt5_aw02():

    @allure.title("tc_mt5_aw02")

    @allure.description(
        """
        Ensure the video is redirected to the correct website
        """
        )
    
    def test_tc02(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5")
                
            with allure.step("Verify the video is redirected to the correct website"):
                video_redirection(driver=main_driver)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
