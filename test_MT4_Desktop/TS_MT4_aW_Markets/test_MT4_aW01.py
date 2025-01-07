import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_markets.utils import market_select_symbols, market_redirect_arrow, news_section, market_watchlist


@allure.epic("MT4 Desktop TS_aW - Markets")

# Member Portal
class TC_MT4_aX01():

    @allure.title("TC_MT4_aX01")

    @allure.description(
        """
        Markets - My Trade
        """
        )
    
    def test_TC01(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live")

            with allure.step("Markets - symbols"):
                market_select_symbols(driver=main_driver, option_name="My Trade")
                market_select_symbols(driver=main_driver, option_name="Top Picks")
                market_select_symbols(driver=main_driver, option_name="Top Gainer")
                market_select_symbols(driver=main_driver, option_name="Top Loser")
                market_select_symbols(driver=main_driver, option_name="Signal")
                
            with allure.step("Markets -  arrows"):
                market_redirect_arrow(driver=main_driver, option_name="My Trade")
                market_redirect_arrow(driver=main_driver, option_name="Top Picks")
                market_redirect_arrow(driver=main_driver, option_name="Top Gainer")
                market_redirect_arrow(driver=main_driver, option_name="Top Loser")
                market_redirect_arrow(driver=main_driver, option_name="Signal")
                market_redirect_arrow(driver=main_driver, option_name="News")
                
            with allure.step("Market Watchlist"):
                market_watchlist(driver=main_driver)
                
            with allure.step("News"):
                news_section(driver=main_driver)


                        
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
