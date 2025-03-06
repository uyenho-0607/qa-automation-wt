import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import link_account

@allure.parent_suite("MT5 Membersite - Desktop - Setting")

@allure.epic("MT5 Desktop ts_av - Setting")

# Member Portal
class TC_mt5_av05():

    @allure.title("tc_mt5_av05")

    @allure.description(
        """
        Member able to link account (Trading Account)
        """
        )
    
    def test_tc05(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5")
            
            with allure.step("Link account"):
                link_account(driver=main_driver, account_id="18094", accountPassword="zf25R!$MzF$g")
                
            with allure.step("Link account with error message promot"):
                link_account(driver=main_driver, account_id="18094", accountPassword="zf25R!$MzF$g", expect_failure=True) # expected to fail
                
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
