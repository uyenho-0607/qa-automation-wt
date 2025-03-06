import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_markets.utils import market_redirect_arrow, market_watchlist


@allure.parent_suite("MT4 Membersite - Desktop - Markets")

@allure.epic("MT4 Desktop TS_aR - Markets")

# Member Portal
class TC_MT4_aR06():

    @allure.title("TC_MT4_aR06")

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
    
    def test_TC06(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("My Trade - Click on [>] and redirect to Asset screen"):
                market_redirect_arrow(driver=main_driver, option_name="My Trade")
                
            with allure.step("Top Picks - Click on [>] and redirect to Trade screen - Top Picks tab pre-selected"):
                market_redirect_arrow(driver=main_driver, option_name="Top Picks")
                
            with allure.step("Top Gainer - Click on [>] and redirect to Trade screen - Top Gainer tab pre-selected"):
                market_redirect_arrow(driver=main_driver, option_name="Top Gainer")
                
            with allure.step("Top Loser - Click on [>] and redirect to Trade screen - Top Loser tab pre-selected"):
                market_redirect_arrow(driver=main_driver, option_name="Top Loser")
                
            with allure.step("Signal - Click on [>] and redirect to Signal screen - Fav Signal / Signal List tab pre-selected"):
                market_redirect_arrow(driver=main_driver, option_name="Signald")
                
            with allure.step("News - Click on [>] and redirect to News screen"):
                market_redirect_arrow(driver=main_driver, option_name="News")
                
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
