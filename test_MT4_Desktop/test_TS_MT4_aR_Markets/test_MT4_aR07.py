import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_markets.utils import market_watchlist_filter


@allure.epic("MT4 Desktop TS_aR - Markets")

# Member Portal
class TC_MT4_aR07():

    @allure.title("TC_MT4_aR07")

    @allure.description(
        """
        Members can filter the symbols to display or hide them
        """
        )
    
    def test_TC07(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live")

            with allure.step("Market Watchlist"):
                market_watchlist_filter(driver=main_driver)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
