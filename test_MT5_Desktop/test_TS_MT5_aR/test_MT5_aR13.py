import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton_OCT, neg_trade_limit_order, get_neg_snackbar_banner, trade_ordersConfirmationDetails



@allure.epic("MT5 Desktop TS_aR")

# Member Portal
class TC_MT5_aR13():

    @allure.title("TC_MT5_aR13")

    @allure.description(
        """
        Pending Order (Place Limit Buy Order)

        Negative Scenario: Invalid Stop Loss
        Error message: Invalid Stop Loss Or Take Profit Hit
        """
        )
    
    def test_TC13(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        ffmpeg_process, screen_recording_file = start_screen_recording(class_name)
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT5", client_name="Transactcloudmt5", account_type="live")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, platform="MT5", client_name="Transactcloudmt5")
                
            with allure.step("Disable OCT"):
                toggle_radioButton_OCT(driver=main_driver)
                
            with allure.step("Place Limit Order"):
                neg_trade_limit_order(driver=main_driver, trade_type="trade", option="buy", set_takeProfit=False, entryPrice_flag=False)
                
            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")
                
            with allure.step("Retrieve the snackbar message"):
                get_neg_snackbar_banner(driver=main_driver)

        finally:
            stop_screen_recording(ffmpeg_process)
                        
            shutdown(main_driver)

            attach_video_to_allure(screen_recording_file, class_name)
