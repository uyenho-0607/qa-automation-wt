import allure
from datetime import datetime

# from dateutil.parser import parse
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_subMenu.utils import menu_button
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import type_orderPanel, OH_closeDate

@allure.parent_suite("MT5 Membersite - Desktop - Others")

@allure.epic("MT5 Desktop TS_aR - Others")

# Member Portal
class TC_MT4_aR09():

    @allure.title("TC_MT5_aR09")

    @allure.description(
        """
        Member able to select a date range from order history with the table content updated
        """
        )
    
    def test_TC09(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server="MT5", client_name="Transactcloudmt5")

            with allure.step("Select the Order Panel: Order History"):
                type_orderPanel(driver=main_driver, tab_order_type="history", sub_tab="positions-history", position=True)
                
            with allure.step("Retrieve the Order Panel data"):
                OH_closeDate(driver=main_driver, startDate="3", endDate="4",
                             target_startMonth=datetime.strptime("October 2025", "%B %Y"),
                             target_endMonth=datetime.strptime("October 2025", "%B %Y"))

            with allure.step("Redirect to Asset page"):
                menu_button(driver=main_driver, menu="assets")
                
            with allure.step("Retrieve the Order Panel data"):
                OH_closeDate(driver=main_driver, startDate="3", endDate="4",
                             target_startMonth=datetime.strptime("October 2025", "%B %Y"),
                             target_endMonth=datetime.strptime("October 2025", "%B %Y"))
                
        finally:
            stop_screen_recording(ffmpeg_process)
            
            shutdown(main_driver)

            attach_video_to_allure(screen_recording_file, class_name)
