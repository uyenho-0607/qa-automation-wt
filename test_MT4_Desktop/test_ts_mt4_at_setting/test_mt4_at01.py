import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.setting_accountDetails import sum_by_currency

@allure.parent_suite("MT4 Membersite - Desktop - Setting")

@allure.epic("MT4 Desktop ts_at - Setting")

# Member Portal
class TC_mt4_at01():

    @allure.title("tc_mt4_at01")

    @allure.description(
        """
        Ensure the total balance display correctly
        """
        )
    
    def test_tc01(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")
                
            with allure.step("Verify the total balance label account is correct"):
                sum_by_currency(driver=main_driver)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
