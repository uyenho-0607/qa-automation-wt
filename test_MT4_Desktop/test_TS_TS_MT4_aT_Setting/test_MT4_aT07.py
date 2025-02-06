import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import switch_or_delete_account


@allure.epic("MT4 Desktop TS_aT - Setting")

# Member Portal
class TC_MT4_aT07():

    @allure.title("TC_MT4_aT07")

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
                params_wt_url, _, _  = login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live") 
            
            with allure.step("Delete account"):
                switch_or_delete_account(driver=main_driver, option="delete", login_password="Asd123", params_wt_url=params_wt_url)
                
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
