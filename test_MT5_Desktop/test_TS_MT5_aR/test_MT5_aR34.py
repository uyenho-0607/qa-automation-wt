import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton_OCT, trade_stopLimit_order, neg_modify_stopLimit_order, get_neg_snackbar_banner, get_trade_snackbar_banner, extract_order_info



@allure.epic("MT5 Desktop TS_aR")

# Member Portal
class TC_MT5_aR34():

    @allure.title("TC_MT5_aR34")

    @allure.description(
        """
        Pending Order (Modify Stop Limit Buy Order) - OCT

        Negative Scenario: Pending Order - Invalid Price submitted
        Error message: Invalid Price Submitted
        """
        )
    
    def test_TC34(self, chromeDriver):
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
                
            with allure.step("Enable OCT"):
                toggle_radioButton_OCT(driver=main_driver, desired_state="checked")
                
            with allure.step("Place Stop Limit Order"):
                trade_stopLimit_order(driver=main_driver, trade_type="trade", option="buy", set_stopLoss=False, set_takeProfit=False, expiryType="good-till-day")

            with allure.step("Retrieve the snackbar message"):
                get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Retrieve the Newly Created Pending Order"):
                extract_order_info(driver=main_driver, tab_order_type="pending-orders", section_name="Pending Order", row_number=[1])

            """ Start of modifying Pending Order """
            
            with allure.step("Modify on Stop Limit Order"):
                neg_modify_stopLimit_order(driver=main_driver, trade_type="edit", row_number=[1], set_stopLoss=False, set_takeProfit=False, stopLimitPrice_flag=False)
                
            with allure.step("Retrieve the snackbar message"):
                get_neg_snackbar_banner(driver=main_driver)
                
        finally:
            stop_screen_recording(ffmpeg_process)
                        
            shutdown(main_driver)

            attach_video_to_allure(screen_recording_file, class_name)
