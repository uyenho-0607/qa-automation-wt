import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton, trade_market_order, trade_ordersConfirmationDetails, get_trade_snackbar_banner, close_delete_order

@allure.parent_suite("MT4 Membersite - Desktop - Others")

@allure.epic("MT4 Desktop TS_aP - Others")

# Member Portal
class TC_MT4_aP03():

    @allure.title("TC_MT4_aP03")

    @allure.description(
        """
        (Close) - Market Order
        
        - Min/Max button
        - Increase/Decrease by button
        - Validation check
        """
        )
    
    def test_TC03(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server="MT4", client_name="Lirunex")
                
            with allure.step("Disable OCT"):
                toggle_radioButton(driver=main_driver, category="OCT", desired_state="unchecked")
                
            with allure.step("Place Market Order"):
                trade_market_order(driver=main_driver, trade_type="trade", option="buy", set_stopLoss=False, set_takeProfit=False)

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")
                
            with allure.step("Retrieve the snackbar message"):
                get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Order Panel: Open Position - Click on Close to Partial close an order"):
                close_delete_order(driver=main_driver, row_number=[1], order_action="close", actions=[("increase", 3), ("decrease", 2)], trade_type="close-order", set_negMarket=True)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
