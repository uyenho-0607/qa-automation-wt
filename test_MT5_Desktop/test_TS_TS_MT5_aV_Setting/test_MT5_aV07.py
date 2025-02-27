import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import switch_or_delete_account

@allure.parent_suite("MT5 Membersite - Desktop - Setting")

@allure.epic("MT5 Desktop TS_aV - Setting")

# Member Portal
class TC_MT5_aV07():

    @allure.title("TC_MT5_aV07")

    @allure.description(
        """
        Member able to delete account (Trading Account)
        """
        )
    
    def test_TC07(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                params_wt_url, _, _  = login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5")
            
            with allure.step("Delete account"):
                switch_or_delete_account(driver=main_driver, option="delete", login_password="Asdf!234", params_wt_url=params_wt_url)
                
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
