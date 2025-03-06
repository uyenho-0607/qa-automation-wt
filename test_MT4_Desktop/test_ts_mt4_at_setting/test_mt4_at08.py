import allure

from constants.helper.driver import delay, shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import open_demo_account_screen

@allure.parent_suite("MT4 Membersite - Desktop - Setting")

@allure.epic("MT4 Desktop ts_at - Setting")

# Member Portal
class TC_mt4_at08():

    @allure.title("tc_mt4_at08")

    @allure.description(
        """
        Member able to open a demo account via login screen
        """
        )
    
    def test_tc08(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Launch Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="demo", set_username=False)

            with allure.step("Open demo account by clicking the 'X' button"):
                # System click on the "X" button
                open_demo_account_screen(driver=main_driver, set_close_modal=True)
            
            with allure.step("Open demo account and login"):
                # System click on the "Sign In" button
                open_demo_account_screen(driver=main_driver, new_password="Asdf!23456789", confirm_password="Asdf!23456789")
                
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)