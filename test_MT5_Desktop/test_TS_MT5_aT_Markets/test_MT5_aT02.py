import allure

from common.desktop.module_markets.trade_watchlist import handle_pre_selected_tab
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt


@allure.parent_suite("MT5 Membersite - Desktop - Markets")

@allure.epic("MT5 Desktop ts_at - Markets")

# Member Portal
class TC_mt5_at02():

    @allure.title("tc_mt5_at02")

    @allure.description(
        """
        Member able to verify the login pre-selected tab
        """
        )
    
    def test_tc02(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5")

            with allure.step("Check the pre-selected tab is correct"):
                handle_pre_selected_tab(driver=main_driver)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
