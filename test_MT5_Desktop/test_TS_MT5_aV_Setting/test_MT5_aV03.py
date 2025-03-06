import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import switch_account_type

@allure.parent_suite("MT5 Membersite - Desktop - Setting")

@allure.epic("MT5 Desktop TS_aV - Setting")

# Member Portal
class TC_MT5_aV03():

    @allure.title("TC_MT5_aV03")

    @allure.description(
        """
        Member able to switch account (Live)
        """
        )
    
    def test_TC03(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5", account_type="demo")
                
            with allure.step("Click on the 'Switch to Live Account' tab"):
                switch_account_type(driver=main_driver, account_type="live")
                
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
