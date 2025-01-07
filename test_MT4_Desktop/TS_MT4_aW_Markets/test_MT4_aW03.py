import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton_OCT, trade_oct_market_order
from common.desktop.module_markets.utils import myTrade_order



@allure.epic("MT4 Desktop TS_aW - Markets")

# Member Portal
class TC_MT4_aX01():

    @allure.title("TC_MT4_aX01")

    @allure.description(
        """
        Verify that the specified symbol appears in the 'My Trade' section at the top row.
        """
        )
    
    def test_TC01(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live")

            with allure.step("Search symbol"):
                symbolName = input_symbol(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("Enable OCT"):
                toggle_radioButton_OCT(driver=main_driver, desired_state="checked")

            with allure.step("Place Market Order"):
                trade_oct_market_order(driver=main_driver, option="buy")

            with allure.step("Verify My Trade Order"):
                myTrade_order(driver=main_driver, symbol_name=symbolName)


                        
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
