import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_trade.utils import toggle_radioButton_OCT, trade_ordersConfirmationDetails, get_trade_snackbar_banner
from common.desktop.module_signal.utils import button_copyTrade
from data_config.utils import compare_dataframes, process_and_print_data


@allure.epic("MT4 Desktop TS_aX")

# Member Portal
class TC_MT4_aX01():

    @allure.title("TC_MT4_aX02")

    @allure.description(
        """
        Market Buy Order
        
        Swap to Units
        """
        )
    
    def test_TC01(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        # Get the class name dynamically
        start_screen_recording()
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT4", client_name="Lirunex", account_type="live") 
                
            with allure.step("Enable OCT"):
                toggle_radioButton_OCT(driver=main_driver, desired_state="checked")
            
            with allure.step("Copy To Trade Order"):
                copyTrade_df = button_copyTrade(driver=main_driver)
                
            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Compare against the Copy Trade and Snackbar message"):
                compare_dataframes(df1=copyTrade_df, name1="Copy Trade Details",
                                   df2=trade_snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Stop Loss", "Take Profit"])
            
            with allure.step("Print Modify Order Table Result"):
                process_and_print_data(copyTrade_df, trade_snackbar_banner_df)
                  
        finally:
            stop_screen_recording()
                        
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)