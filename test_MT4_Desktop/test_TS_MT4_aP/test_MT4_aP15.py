import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton_OCT, neg_trade_limit_order, get_neg_snackbar_banner



@allure.epic("MT4 Desktop TS_aP")

# Member Portal
class TC_MT4_aP15():

    @allure.title("TC_MT4_aP15")

    @allure.description(
        """
        Pending Order (Place Limit Sell Order) - OCT

        Negative Scenario: Invalid Take Profit
        Error message: Invalid Stop Loss Or Take Profit Hit
        """
        )
    
    def test_TC15(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        ffmpeg_process, screen_recording_file = start_screen_recording(class_name)
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT4", client_name="Lirunex", account_type="live")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, platform="MT4", client_name="Lirunex")
                
            with allure.step("Enable OCT"):
                toggle_radioButton_OCT(driver=main_driver, desired_state="checked")

            with allure.step("Place Limit Order"):
                neg_trade_limit_order(driver=main_driver, trade_type="trade", option="sell", set_stopLoss=False, entryPrice_flag=False)
                
            with allure.step("Retrieve the snackbar message"):
                get_neg_snackbar_banner(driver=main_driver)
                
        finally:
            stop_screen_recording(ffmpeg_process)
                        
            shutdown(main_driver)

            attach_video_to_allure(screen_recording_file, class_name)
