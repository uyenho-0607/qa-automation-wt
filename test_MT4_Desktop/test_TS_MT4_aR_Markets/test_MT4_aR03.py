import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_markets.utils import select_trade_symbol_from_watchlist

@allure.parent_suite("MT4 Membersite - Desktop - Markets")

@allure.epic("MT4 Desktop TS_aR - Markets")

# Member Portal
class TC_MT4_aR03():

    @allure.title("TC_MT4_aR03")

    @allure.description(
        """
        Member can select any symbol via the Trade - Watchlist page
        """
        )
    
    def test_TC03(self, chromeDriver):
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
