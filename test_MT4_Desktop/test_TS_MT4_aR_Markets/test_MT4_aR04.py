import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_markets.utils import market_redirect_arrow, market_watchlist


@allure.epic("MT4 Desktop TS_aR - Markets")

# Member Portal
class TC_MT4_aR04():

    @allure.title("TC_MT4_aR04")

    @allure.description(
        """
        Member able to redirect to the correct page upon clicking on [>]
        - My Trade
        - Top Picks
        - Top Gainer / Top Loser
        - Signal
        - News
        """
        )
    
    def test_TC04(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live", testcaseID="TC01")

            with allure.step("Markets -  arrows"):
                market_redirect_arrow(driver=main_driver, option_name="My Trade")
                market_redirect_arrow(driver=main_driver, option_name="Top Picks")
                market_redirect_arrow(driver=main_driver, option_name="Top Gainer")
                market_redirect_arrow(driver=main_driver, option_name="Top Loser")
                market_redirect_arrow(driver=main_driver, option_name="Signal")
                market_redirect_arrow(driver=main_driver, option_name="News")

            with allure.step("Market Watchlist"):
                market_watchlist(driver=main_driver)
                
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
