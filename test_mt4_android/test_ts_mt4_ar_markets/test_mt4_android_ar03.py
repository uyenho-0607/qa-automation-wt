import allure

from enums.main import Server
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import login_wt
from common.mobileapp.module_symbol.search_symbol import search_symbol_variations


@allure.parent_suite("MT4 Membersite - Android - Markets")

@allure.epic("MT4 Android ts_ar - Markets")

# Member Portal
class TC_MT4_aR03():

    @allure.title("TC_MT4_aR03")

    @allure.description(
        """
        Member able to search for symbols
        - Wildcard search
        - Exact match
        """
    )
    
    def test_tc03(self, android_driver):
        self.driver = android_driver
        main_driver = self.driver
        session_id = main_driver.session_id

        # Get the class name dynamically
        class_name = self.__class__.__name__
        start_recording_mobile(driver=main_driver)
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT4)

            with allure.step("Perform exact and wildcard search"):
                search_symbol_variations(driver=main_driver, server=Server.MT4)

        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)