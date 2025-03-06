import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_signal.signal import signal_search_feature


@allure.parent_suite("MT4 Membersite - Desktop - Signal")

@allure.epic("MT4 Desktop TS_aS - Signal")

# Member Portal
class TC_MT4_aS01():

    @allure.title("TC_MT4_aS01")

    @allure.description(
        """
        Signal - Search function
        - Wildcard Search
        - Exact Search
        """
        )
    
    def test_TC01(self, chromeDriver):

        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", testcaseID="TC01")
            
            with allure.step("Signal - Search function"):
                signal_search_feature(driver=main_driver)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
