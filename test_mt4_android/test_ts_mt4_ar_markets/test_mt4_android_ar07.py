import allure
import pytest

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import login_wt
from common.mobileapp.module_markets.utils import market_select_symbols, market_watchlist


@allure.parent_suite("MT4 Membersite - Android - Markets")

@allure.epic("MT4 Android ts_ar - Markets")

# Member Portal
class TC_MT4_aR07():

    @allure.title("TC_MT4_aR07")

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
    
    @pytest.mark.flaky(reruns=1, reruns_delay=2)  # Retry once if the test fails
    def test_tc07(self, chromeDriver, request):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Get the class name dynamically
        class_name = self.__class__.__name__
        start_recording_mobile(driver=main_driver)
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT4, client_name="Lirunex")

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
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)