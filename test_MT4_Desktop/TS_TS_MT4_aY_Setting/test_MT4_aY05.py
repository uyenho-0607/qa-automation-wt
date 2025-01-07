import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import open_demo_account


@allure.epic("MT4 Desktop TS_aY - Setting")

# Member Portal
class TC_MT4_aY05():

    @allure.title("TC_MT4_aY05")

    @allure.description(
        """
        Open a demo account
        """
        )
    
    def test_TC05(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live")

            with allure.step("Open demo account"):
                # System click on the "Sign In" button
                open_demo_account(driver=main_driver, setting=True)
                
                # System click on the "X" button
                # open_demo_account(driver=main_driver, set_close=True)


                        
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)