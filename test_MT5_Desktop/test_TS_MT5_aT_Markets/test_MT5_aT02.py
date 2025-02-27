import allure

from common.desktop.module_markets.trade_watchlist import toggle_symbol_favorite_status
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt


@allure.parent_suite("MT5 Membersite - Desktop - Markets")

@allure.epic("MT5 Desktop TS_aT - Markets")

# Member Portal
class TC_MT5_aT02():

    @allure.title("TC_MT5_aT02")

    @allure.description(
        """
        Member able to 
        - verify the login pre-selected tab
        - fav or unfav symbol for each of the section
        """
        )
    
    def test_TC02(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5")
                
            with allure.step("Toggle to Fav/Unfav the star"):
                toggle_symbol_favorite_status(driver=main_driver)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
