import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_markets.utils import market_redirect_arrow

@allure.parent_suite("MT5 Membersite - Desktop - Markets")

@allure.epic("MT5 Desktop ts_at - Markets")

# Member Portal
class TC_mt5_at06():

    @allure.title("tc_mt5_at06")

    @allure.description(
        """
        Member able to redirect to the correct page upon clicking on [>]
        - My Trade
        - Top Picks
        - Top Gainer / Top Loser
        - Signal
        """
        )
    
    def test_tc06(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5")

            with allure.step("My Trade - Click on [>] and redirect to Asset screen"):
                market_redirect_arrow(driver=main_driver, option_name="My Trade")
                
            with allure.step("Top Picks - Click on [>] and redirect to Trade screen - Top Picks tab pre-selected"):
                market_redirect_arrow(driver=main_driver, option_name="Top Picks")
                
            with allure.step("Top Gainer - Click on [>] and redirect to Trade screen - Top Gainer tab pre-selected"):
                market_redirect_arrow(driver=main_driver, option_name="Top Gainer")
                
            with allure.step("Top Loser - Click on [>] and redirect to Trade screen - Top Loser tab pre-selected"):
                market_redirect_arrow(driver=main_driver, option_name="Top Loser")
                
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
