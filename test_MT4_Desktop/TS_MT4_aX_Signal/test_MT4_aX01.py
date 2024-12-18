import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_trade.utils import toggle_radioButton_OCT, trade_ordersConfirmationDetails, get_trade_snackbar_banner
from common.desktop.module_signal.utils import button_copyTrade
from data_config.utils import compare_dataframes, process_and_print_data


@allure.epic("MT4 Desktop TS_aP")

# Member Portal
class TC_MT4_aP01():

    @allure.title("TC_MT4_aP01")

    @allure.description(
        """
        Market Buy Order
        
        Swap to Units
        """
        )
    
    def test_TC01(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        ffmpeg_process, screen_recording_file = start_screen_recording(class_name)
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT4", client_name="Lirunex", account_type="live") 
                
            with allure.step("Disable OCT"):
                toggle_radioButton_OCT(driver=main_driver)
            
            with allure.step("Copy To Trade Order"):
                copyTrade_df = button_copyTrade(driver=main_driver)


            # with allure.step("Click on the Trade Confirmation button to place the order"):
            #     trade_tradeConfirmation_df = trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")

            # with allure.step("Compare against the Trade Confirmation and Snackbar message"):
            #     compare_dataframes(df1=copyTrade_df, name1="Copy Trade Details",
            #                        df2=trade_tradeConfirmation_df, name2="Trade Confirmation Details",
            #                        required_columns=["Symbol", "Type", "Size", "Units", "Stop Loss", "Take Profit"])
                
            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            # with allure.step("Compare against the Trade Confirmation and Snackbar message"):
            #     compare_dataframes(df1=trade_tradeConfirmation_df, name1="Trade Confirmation Details",
            #                        df2=trade_snackbar_banner_df, name2="Snackbar Banner Message",
            #                        required_columns=["Symbol", "Type", "Size", "Units", "Stop Loss", "Take Profit"])


            with allure.step("Compare against the Trade Confirmation and Snackbar message"):
                compare_dataframes(df1=copyTrade_df, name1="Copy Trade Details",
                                   df2=trade_snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Size", "Stop Loss", "Take Profit"])
            
            with allure.step("Print Modify Order Table Result"):
                # process_and_print_data(trade_tradeConfirmation_df, trade_snackbar_banner_df)
                process_and_print_data(copyTrade_df, trade_snackbar_banner_df)
                  
        finally:
            stop_screen_recording(ffmpeg_process)
                        
            shutdown(main_driver)

            attach_video_to_allure(screen_recording_file, class_name)
