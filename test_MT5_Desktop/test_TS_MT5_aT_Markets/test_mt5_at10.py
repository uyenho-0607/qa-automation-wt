import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_markets.announcements import announcement_validation


@allure.parent_suite("MT5 Membersite - Desktop - Markets")

@allure.epic("MT5 Desktop ts_at - Markets")

# Member Portal
class TC_mt5_at10():

    @allure.title("tc_mt5_at10")

    @allure.description(
        """
        Announcement Validation
        """
        )
    
    def test_tc10(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5")
                
            with allure.step("Announcement"):
                announcement_validation(driver=main_driver)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
