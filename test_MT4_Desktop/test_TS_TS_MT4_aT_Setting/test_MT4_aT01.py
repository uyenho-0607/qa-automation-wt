import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.setting_accountDetails import sum_by_currency


@allure.epic("MT4 Desktop TS_aT - Setting")

# Member Portal
class TC_MT4_aT01():

    @allure.title("TC_MT4_aT01")

    @allure.description(
        """
        Ensure the total balance display correctly
        """
        )
    
    def test_TC01(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live")
                
            with allure.step("Verify the total balance label account is correct"):
                sum_by_currency(driver=main_driver)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
