import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt


@allure.epic("MT5 Desktop TS_aA - Login")

# Member Portal - Login via Demo CMS account
class TC_MT5_aA03():

    @allure.title("TC_MT5_aA03")
    
    @allure.description(
        """
        Member unable login with wrong credentials in Live tab
        - correct accountID with wrong password
        """
        )
    
    def test_TC03(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        

        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5", account_type="live", testcaseID="TC01", expect_failure=True)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
