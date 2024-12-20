import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton_OCT, neg_trade_stopLimit_order, get_neg_snackbar_banner, trade_ordersConfirmationDetails



@allure.epic("MT5 Desktop TS_aR")

# Member Portal
class TC_MT5_aR29():

    @allure.title("TC_MT5_aR29")

    @allure.description(
        """
        Pending Order (Place Stop Limit Buy Order)

        Negative Scenario: Pending Order - Invalid Stop Limit Price submitted
        Error message: Invalid Price Submitted
        """
        )
    
    def test_TC29(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        # Get the class name dynamically
        start_screen_recording()
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT5", client_name="Transactcloudmt5", account_type="live")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, platform="MT5", client_name="Transactcloudmt5")
                
            with allure.step("Disable OCT"):
                toggle_radioButton_OCT(driver=main_driver)
                      
            with allure.step("Place Stop Limit Order"):
                neg_trade_stopLimit_order(driver=main_driver, trade_type="trade", option="buy", set_stopLoss=False, set_takeProfit=False, entryPrice_flag=False)
                
            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")
                
            with allure.step("Retrieve the snackbar message"):
                get_neg_snackbar_banner(driver=main_driver)
                
        finally:
            stop_screen_recording()
                        
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)