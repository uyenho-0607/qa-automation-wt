import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.webTrader_login import forgot_password

@allure.parent_suite("MT4 Membersite - Desktop - Login")

@allure.epic("MT4 Desktop ts_aa - Login")

# Member Portal
class TC_mt4_aa09():

    @allure.title("tc_mt4_aa09")

    @allure.description(
        """
        Forgot Password via Live
        """
        )
    
    def test_tc09(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:

            with allure.step("Launch Web Trader Membersite and click on Forgot Password button"):
                forgot_password(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live", email="test11@test.com", accountID="18818888")

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
