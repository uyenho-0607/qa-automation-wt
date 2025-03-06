import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.search_symbol import symbol_search_feature


@allure.parent_suite("MT4 Membersite - Desktop - Markets")

@allure.epic("MT4 Desktop ts_ar - Markets")

# Member Portal
class TC_mt4_ar01():

    @allure.title("tc_mt4_ar01")

    @allure.description(
        """
        Member able to search for symbols
        - Wildcard search
        - Exact match
        """
        )
    
    def test_tc01(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("Check the pre-selected tab is correct"):
                symbol_search_feature(driver=main_driver, server="MT4", client_name="Lirunex")

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
