import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import switch_account_type

@allure.parent_suite("MT4 Membersite - Desktop - Setting")

@allure.epic("MT4 Desktop ts_at - Setting")

# Member Portal
class TC_mt4_at02():

    @allure.title("tc_mt4_at02")

    @allure.description(
        """
        Member able to switch account (Demo)
        """
        )
    
    def test_tc02(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")
                
            with allure.step("Click on the 'Switch to Demo Account' tab"):
                switch_account_type(driver=main_driver, account_type="demo")
                
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
