import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_markets.trade_watchlist import toggle_symbol_favorite_status


@allure.parent_suite("MT4 Membersite - Desktop - Markets")

@allure.epic("MT4 Desktop ts_ar - Markets")

# Member Portal
class TC_mt4_ar03():

    @allure.title("tc_mt4_ar03")

    @allure.description(
        """
        Member able to fav or unfav symbol for each of the section
        """
        )
    
    def test_tc03(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")
                
            with allure.step("Toggle to Fav/Unfav the star"):
                toggle_symbol_favorite_status(driver=main_driver)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
