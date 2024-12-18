import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile
from common.mobileweb.module_login.utils import login_wt
from common.mobileweb.module_symbol.utils import input_symbol
from common.mobileweb.module_trade.utils import toggle_radioButton_OCT, neg_trade_market_order, get_neg_snackbar_banner


@allure.epic("MT4 Mobile TS_aP")

# Member Portal
class TC_MT4_aP09():

    @allure.title("TC_MT4_aP09")

    @allure.description(
        """
        Market Sell Order - OCT

        Negative Scenario: Invalid Take Profit
        Error message: Invalid Stop Loss Or Take Profit Hit
        """
        )
        
    def test_TC09(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        # start_recording_mobile(driver=main_driver)
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT4", client_name="Lirunex", account_type="live")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, platform="MT4", client_name="Lirunex")
                
            with allure.step("Enable OCT"):
                toggle_radioButton_OCT(driver=main_driver, desired_state="checked")
                
            with allure.step("Place Take Profit - Price"):
                neg_trade_market_order(driver=main_driver, trade_type="trade", option="sell", set_stopLoss=False, pre_trade=True)
                
            with allure.step("Retrieve the snackbar message"):
                get_neg_snackbar_banner(driver=main_driver)

        finally:
            # video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            # attach_video_to_allure_mobile(video_data, class_name)