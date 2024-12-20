import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton_OCT, neg_trade_stop_order, get_neg_snackbar_banner



@allure.epic("MT4 Desktop TS_aP")

# Member Portal
class TC_MT4_aP23():

    @allure.title("TC_MT4_aP23")

    @allure.description(
        """
        Pending Order (Place Stop Sell Order) - OCT

        Negative Scenario: Invalid Take Profit
        Error message: Invalid Stop Loss Or Take Profit Hit
        """
        )
    
    def test_TC23(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        # Get the class name dynamically
        start_screen_recording()
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT4", client_name="Lirunex", account_type="live")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, platform="MT4", client_name="Lirunex")
                
            with allure.step("Enable OCT"):
                toggle_radioButton_OCT(driver=main_driver, desired_state="checked")

            with allure.step("Place Stop Order"):
                neg_trade_stop_order(driver=main_driver, trade_type="trade", option="sell", set_stopLoss=False, entryPrice_flag=False)
                
            with allure.step("Retrieve the snackbar message"):
                get_neg_snackbar_banner(driver=main_driver)
                
        finally:
            stop_screen_recording()
                        
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)