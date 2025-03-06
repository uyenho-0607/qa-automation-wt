import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_markets.utils import market_select_symbols, market_watchlist


@allure.parent_suite("MT4 Membersite - Desktop - Markets")

@allure.epic("MT4 Desktop ts_ar - Markets")

# Member Portal
class TC_mt4_ar07():

    @allure.title("tc_mt4_ar07")

    @allure.description(
        """
        Member able to redirect to the correct page upon clicking on [Symbols]
        - My Trade
        - Top Picks
        - Top Gainer / Top Loser
        - Symbols
        - Market - Watchlist section
        """
        )
    
    def test_tc07(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("My Trade - Click on [Symbols] and redirect to Trade screen"):
                market_select_symbols(driver=main_driver, option_name="My Trade")
                
            with allure.step("Top Picks - Click on [Symbols] and redirect to Trade screen - Top Picks tab pre-selected"):
                market_select_symbols(driver=main_driver, option_name="Top Picks")

            with allure.step("Top Gainer - Click on [Symbols] and redirect to Trade screen - Top Gainer tab pre-selected"):
                market_select_symbols(driver=main_driver, option_name="Top Gainer")
            
            with allure.step("Top Loser - Click on [Symbols] and redirect to Trade screen - Top Loser tab pre-selected"):
                market_select_symbols(driver=main_driver, option_name="Top Loser")

            with allure.step("Signal - Click on [Symbols] and redirect to Signal screen - Fav Signal / Signal List tab pre-selected"):
                market_select_symbols(driver=main_driver, option_name="Signal")
                
            with allure.step("Market Watchlist"):
                market_watchlist(driver=main_driver)
                
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
