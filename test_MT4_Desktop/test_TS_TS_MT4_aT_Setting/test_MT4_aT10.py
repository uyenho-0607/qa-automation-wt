import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import open_demo_account_error_msg

@allure.parent_suite("MT4 Membersite - Desktop - Setting")

@allure.epic("MT4 Desktop TS_aT - Setting")

# Member Portal
class TC_MT4_aT10():

    @allure.title("TC_MT4_aT10")

    @allure.description(
        """
        Error message checking for demo account creation
        """
        )
    
    def test_TC10(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="demo", set_username=False)

            with allure.step("Open demo account"):
                open_demo_account_error_msg(driver=main_driver)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)