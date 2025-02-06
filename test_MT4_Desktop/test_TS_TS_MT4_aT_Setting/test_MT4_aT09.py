import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import open_demo_account


@allure.epic("MT4 Desktop TS_aT - Setting")

# Member Portal
class TC_MT4_aT09():

    @allure.title("TC_MT4_aT09")

    @allure.description(
        """
        Member able to open a demo account via setting
        """
        )
    
    def test_TC09(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live") 
                # sss

            with allure.step("Open demo account"):
                # System click on the "X" button
                open_demo_account(driver=main_driver, setting=True,  set_close_modal=True)
                
                # System click on the "Sign In" button
                open_demo_account(driver=main_driver, setting=True, new_password="Asdf!23456789", confirm_password="Asdf!23456789")


        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)