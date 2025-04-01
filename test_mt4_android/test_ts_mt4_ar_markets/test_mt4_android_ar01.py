import allure
import pytest

from enums.main import Server, OrderPanel
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import login_wt
from common.mobileapp.module_markets.utils import navigate_and_select_watchlist_symbol


@allure.parent_suite("MT4 Membersite - Android - Markets")

@allure.epic("MT4 Android ts_ar - Markets")

# Member Portal
class TC_MT4_aR01():

    @allure.title("TC_MT4_aR01")

    @allure.description(
        """
        Member can select any symbol via the Trade - Watchlist page
        """
    )
    
    def test_tc01(self, androidDriver):
        self.driver = androidDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Get the class name dynamically
        class_name = self.__class__.__name__
        start_recording_mobile(driver=main_driver)
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT4)
                
            with allure.step("Market Watchlist"):
                navigate_and_select_watchlist_symbol(driver=main_driver)
                
        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)