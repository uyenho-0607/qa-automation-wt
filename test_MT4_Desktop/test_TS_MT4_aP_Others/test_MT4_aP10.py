import allure

# from datetime import datetime

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.order_panel.utils import toggle_order_panel_sort


@allure.epic("MT4 Desktop TS_aP - Others")

# Member Portal
class TC_MT4_aP10():

    @allure.title("TC_MT4_aP10")

    @allure.description(
        """
        Member able to sort/hide columns with the table content updated
        """
        )
    
    def test_TC10(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("Disable OCT"):
                toggle_order_panel_sort(driver=main_driver)

                # toggle_order_panel_sort(driver=main_driver, startDate="3", endDate="4",
                #                         target_startMonth=datetime.strptime("October 2024", "%B %Y"),
                #                         target_endMonth=datetime.strptime("October 2024", "%B %Y"))
                                        
        finally:
            stop_screen_recording(ffmpeg_process)
            
            shutdown(main_driver)

            attach_video_to_allure(screen_recording_file, class_name)
