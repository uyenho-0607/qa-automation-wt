import allure


from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_trade.order_panel.utils import update_column_visibility

@allure.parent_suite("MT4 Membersite - Desktop - Others")

@allure.epic("MT4 Desktop TS_aP - Others")

# Member Portal
class TC_MT4_aP11():

    @allure.title("TC_MT4_aP11")

    @allure.description(
        """
        Member able to update the column visibility with the table header updated
        """
        )
    
    def test_TC11(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live", testcaseID="TC01")

            with allure.step("Validate Column Visibility from Trade to Asset"):
                update_column_visibility(driver=main_driver, tab_order_type="open-positions")
                update_column_visibility(driver=main_driver, tab_order_type="pending-orders")
                update_column_visibility(driver=main_driver, tab_order_type="history")
                
            with allure.step("Validate Column Visibility from Asset to Trade"):
                update_column_visibility(driver=main_driver, tab_order_type="open-positions", set_menu=True)
                update_column_visibility(driver=main_driver, tab_order_type="pending-orders", set_menu=True)
                update_column_visibility(driver=main_driver, tab_order_type="history", set_menu=True)

        finally:
            stop_screen_recording(ffmpeg_process)
            
            shutdown(main_driver)

            attach_video_to_allure(screen_recording_file, class_name)
