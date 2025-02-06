import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import link_account, switch_or_delete_account


@allure.epic("MT4 Desktop TS_aT - Setting")

# Member Portal
class TC_MT4_aT05():

    @allure.title("TC_MT4_aT05")

    @allure.description(
        """
        Member able to link account (Trading Account)
        """
        )
    
    def test_TC05(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live") 
            
            with allure.step("Link account"):
                link_account(driver=main_driver, account_id="188188888", accountPassword="Asd123")
                # link_account(driver=main_driver, account_id="188188888", accountPassword="Asd123", expect_failure=True) # expected to fail
                
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
