import allure

from datetime import datetime
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_subMenu.utils import menu_button
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import type_orderPanel, OH_closeDate


@allure.epic("MT4 Desktop TS_aP")

# Member Portal
class TC_MT4_aP07():

    @allure.title("TC_MT4_aP07")

    @allure.description(
        """
        Member able to select a date range from order history with the table content updated
        """
        )
    
    def test_TC07(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        # Get the class name dynamically
        start_screen_recording()
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT4", client_name="Lirunex", account_type="live")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, platform="MT4", client_name="Lirunex")

            with allure.step("Select the Order Panel: Order History"):
                type_orderPanel(driver=main_driver, tab_order_type="history")

            with allure.step("Retrieve the Order Panel data"):        
                OH_closeDate(driver=main_driver, startDate="3", endDate="4",
                                    target_startMonth=datetime.strptime("October 2024", "%B %Y"),
                                    target_endMonth=datetime.strptime("October 2024", "%B %Y"))

            with allure.step("Redirect to Asset page"):
                menu_button(driver=main_driver, menu="assets")
                
            with allure.step("Select the Order Panel: Order History"):
                type_orderPanel(driver=main_driver, tab_order_type="history")

            with allure.step("Retrieve the Order Panel data"):        
                OH_closeDate(driver=main_driver, startDate="3", endDate="4",
                                    target_startMonth=datetime.strptime("October 2024", "%B %Y"),
                                    target_endMonth=datetime.strptime("October 2024", "%B %Y"))
            
        finally:
            stop_screen_recording()
                        
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)