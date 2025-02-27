import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton, trade_oct_market_order, get_trade_snackbar_banner
from common.desktop.module_markets.utils import myTrade_order


@allure.parent_suite("MT5 Membersite - Desktop - Markets")

@allure.epic("MT5 Desktop TS_aT - Markets")

# Member Portal
class TC_MT5_aT04():

    @allure.title("TC_MT5_aT04")

    @allure.description(
        """
        "My Trade" displays the symbol of the most recently placed order.
        """
        )
    
    def test_TC04(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5")

            with allure.step("Search symbol"):
                symbolName = input_symbol(driver=main_driver, server="MT5", client_name="Transactcloudmt5")

            with allure.step("Enable OCT"):
                toggle_radioButton(driver=main_driver, category="OCT", desired_state="checked")

            with allure.step("Place Market Order"):
                direction = trade_oct_market_order(driver=main_driver, indicator_type="buy")

            with allure.step("Retrieve the snackbar message"):
                get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Verify My Trade Order"):
                myTrade_order(driver=main_driver, symbol_name=symbolName, order_type=direction)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
