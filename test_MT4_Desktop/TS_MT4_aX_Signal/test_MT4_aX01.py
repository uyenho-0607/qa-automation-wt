import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_trade.utils import toggle_radioButton_OCT, trade_ordersConfirmationDetails, get_trade_snackbar_banner, extract_order_info
from common.desktop.module_signal.utils import button_copyTrade, handle_order_type
from data_config.utils import compare_dataframes, process_and_print_data


@allure.epic("MT4 Desktop TS_aX - Signal")

# Member Portal
class TC_MT4_aX01():

    @allure.title("TC_MT4_aX01")

    @allure.description(
        """
        Signal - Copy To Trade Order
        """
        )
    
    def test_TC01(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live") 
                
            with allure.step("Disable OCT"):
                toggle_radioButton_OCT(driver=main_driver)
            
            with allure.step("Copy To Trade Order"):
                copyTrade_df, label_OrderStatus = button_copyTrade(driver=main_driver)

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_tradeConfirmation_df = trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")

            with allure.step("Compare against the Copy Trade Details and Trade Confirmation Details"):
                compare_dataframes(driver=main_driver, df1=copyTrade_df, name1="Copy Trade Details",
                                   df2=trade_tradeConfirmation_df, name2="Trade Confirmation Details",
                                   required_columns=["Symbol", "Type", "Stop Loss", "Take Profit"])
                
            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Compare against the Trade Confirmation and Snackbar message"):
                compare_dataframes(driver=main_driver, df1=trade_tradeConfirmation_df, name1="Trade Confirmation Details",
                                   df2=trade_snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Size", "Units", "Stop Loss", "Take Profit"])

            with allure.step("Redirect to Asset Page"):
                orderPanel_type, orderPanel_name = handle_order_type(driver=main_driver, order_type=label_OrderStatus)

            with allure.step("Retrieve the Newly Created Order"):
                _, trade_order_df = extract_order_info(driver=main_driver, tab_order_type=orderPanel_type, section_name=orderPanel_name, row_number=[1])
            
            with allure.step("Compare against the Snackbar message and Order Panel details"):
                compare_dataframes(driver=main_driver, df1=trade_snackbar_banner_df, name1="Snackbar Banner Message",
                                   df2=trade_order_df, name2=orderPanel_name,
                                   required_columns=["Symbol", "Type", "Stop Loss", "Take Profit"])
            
            with allure.step("Print the Order Table Result"):
                process_and_print_data(copyTrade_df, trade_tradeConfirmation_df, trade_snackbar_banner_df, trade_order_df)
                

                        
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
