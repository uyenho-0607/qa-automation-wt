import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import switch_or_delete_account, handle_password_prompt_on_account_switch

@allure.parent_suite("MT4 Membersite - Desktop - Setting")

@allure.epic("MT4 Desktop ts_at - Setting")

# Member Portal
class TC_mt4_at06():

    @allure.title("tc_mt4_at06")

    @allure.description(
        """
        Member able to switch account (Trading Account) or Switch account with if (Re-enter password prompt)
        """
        )
    
    def test_tc06(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live", testcaseID="TC01")

            with allure.step("Switch account"):
                switch_or_delete_account(driver=main_driver, option="switch")

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)