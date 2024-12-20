import allure

from datetime import datetime
from constants.helper.driver import delay, shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_session_video_to_allure
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile
from common.mobileweb.module_login.utils import login_wt
from common.mobileweb.module_symbol.utils import input_symbol
from common.mobileweb.module_subMenu.utils import menu_button, myTrade_button
from common.mobileweb.module_trade.utils import type_orderPanel, OH_closeDate, calendar_datePicker, button_viewAllTransaction


@allure.epic("MT4 Mobile TS_aP")

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

        # Get the class name dynamically
        class_name = self.__class__.__name__
        # start_recording_mobile(driver=main_driver)
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT4", client_name="Lirunex", account_type="live")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, platform="MT4", client_name="Lirunex")
                
            # with allure.step("Redirect to Asset page"):
            #     menu_button(driver=main_driver, menu_option="assets")

            # with allure.step("Click on My Trade to redirect to View All Transaction"): 
            #     myTrade_button(driver=main_driver)


            with allure.step("Redirect to View All Transaction page"):
                button_viewAllTransaction(driver=main_driver)

            with allure.step("Select the Order Panel: Order History"):
                type_orderPanel(driver=main_driver, tab_order_type="history")

            with allure.step("Retrieve the Order Panel data"):
                # calendar_datePicker(driver=main_driver, startDate = (10, "September", 2024), endDate = (12, "October", 2024))
                calendar_datePicker(driver=main_driver)

                delay(10)

        finally:
            # video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            # attach_video_to_allure_mobile(video_data, class_name)