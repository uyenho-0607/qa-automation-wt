import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import button_setting

@allure.parent_suite("MT4 Membersite - Desktop - Login")

@allure.epic("MT4 Desktop ts_aa - Login")

# Member Portal
class TC_mt4_aa02():

    @allure.title("tc_mt4_aa02")

    @allure.description(
        """
        Member able login to Web Trader via Live Account tab
        """
        )
    
    def test_tc02(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")
                
            with allure.step("Successfully Logout"):
                button_setting(driver=main_driver, setting_option="logout") 

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
