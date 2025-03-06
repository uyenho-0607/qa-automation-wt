import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_markets.utils import select_trade_symbol_from_watchlist


@allure.parent_suite("MT4 Membersite - Desktop - Markets")

@allure.epic("MT4 Desktop ts_ar - Markets")

# Member Portal
class TC_mt4_ar04():

    @allure.title("tc_mt4_ar04")

    @allure.description(
        """
        Member can select any symbol via the Trade - Watchlist page
        """
        )
    
    def test_tc04(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("Search symbol on trade watchlist"):
                select_trade_symbol_from_watchlist(driver=main_driver)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
