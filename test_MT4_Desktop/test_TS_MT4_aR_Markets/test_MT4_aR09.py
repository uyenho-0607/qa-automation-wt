import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import clear_search_history


@allure.parent_suite("MT4 Membersite - Desktop - Markets")

@allure.epic("MT4 Desktop ts_ar - Markets")

# Member Portal
class TC_mt4_ar09():

    @allure.title("tc_mt4_ar09")

    @allure.description(
        """
        Members can clear the search result history
        """
        )
    
    def test_tc09(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("Clear Search History"):
                clear_search_history(driver=main_driver)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
