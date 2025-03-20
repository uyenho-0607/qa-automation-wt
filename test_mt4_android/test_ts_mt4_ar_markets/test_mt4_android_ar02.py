import allure
import pytest

from enums.main import Server
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import login_wt
from common.mobileapp.module_symbol.utils import input_symbol

# from common.mobileapp.module_markets.trade_watchlist import handle_pre_selected_tab


@allure.parent_suite("MT4 Membersite - Android - Markets")

@allure.epic("MT4 Android TS_AR - Markets")

# Member Portal
class TC_MT4_aR02():

    @allure.title("TC_MT4_aR02")

    @allure.description(
        """
        Member able to verify the login pre-selected tab
        """
    )
    
    def test_tc02(self, android_driver):
        self.driver = android_driver
        main_driver = self.driver
        session_id = main_driver.session_id

        # Get the class name dynamically
        class_name = self.__class__.__name__
        start_recording_mobile(driver=main_driver)
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT4)
                
            with allure.step("Search Symbols"):
                input_symbol(driver=main_driver, server=Server.MT4, desired_symbol_name="UKOIL.std")

            # with allure.step("Check the pre-selected tab is correct"):
            #     handle_pre_selected_tab(driver=main_driver)

        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)