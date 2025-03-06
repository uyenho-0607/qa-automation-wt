import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_signal.signal import express_interest


@allure.parent_suite("MT5 Membersite - Desktop - Signal")

@allure.epic("MT5 Desktop ts_au - Signal")

# Member Portal
class TC_mt5_au03():

    @allure.title("tc_mt5_au03")

    @allure.description(
        """
        Signal - Express Interest
        """
        )
    
    def test_tc03(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5")
            
            with allure.step("Copy To Trade Order"):
                express_interest(driver=main_driver, click_submit=False)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
