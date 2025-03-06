import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import button_setting

@allure.parent_suite("MT5 Membersite - Desktop - Login")

@allure.epic("MT5 Desktop ts_aa - Login")

# Member Portal- Login via CRM account
class TC_mt5_aa01():

    @allure.title("tc_mt5_aa01")

    @allure.description(
        """
        Member able login to Web Trader via CRM Live Account tab
        """
        )
    
    def test_tc01(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5", account_type="crm", use_crm_cred=True)
            
            with allure.step("Successfully Logout"):
                button_setting(driver=main_driver, setting_option="logout")

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
