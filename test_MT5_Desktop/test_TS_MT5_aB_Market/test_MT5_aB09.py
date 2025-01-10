import allure
import pandas as pd

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton_OCT, trade_market_order, modify_market_order, trade_ordersConfirmationDetails, get_trade_snackbar_banner, extract_order_info
from common.desktop.module_notification.utils import process_order_notifications
from data_config.utils import compare_dataframes, process_and_print_data


@allure.epic("MT5 Desktop TS_aB - Market")

# Member Portal 
class TC_MT5_aB09():

    @allure.title("TC_MT5_aB09")
        
    @allure.description(
        """
        Sell Order
        
        Member able to place a Market order with
        - Volume
        
        Member able to modify a Market order with
        - Stop Loss by Price
        """
    )
    
    def test_TC09(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5", account_type="live")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server="MT5", client_name="Transactcloudmt5")

            with allure.step("Disable OCT"):
                toggle_radioButton_OCT(driver=main_driver)

            """ Place Market Order """

            with allure.step("Place Market Order"):
                trade_market_order(driver=main_driver, trade_type="trade", option="sell", set_fillPolicy=True, set_stopLoss=False, set_takeProfit=False)

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_tradeConfirmation_df = trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")
                
            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Compare against the Trade Confirmation and Snackbar message"):
                compare_dataframes(driver=main_driver, df1=trade_tradeConfirmation_df, name1="Trade Confirmation Details",
                                   df2=trade_snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Volume", "Units", "Stop Loss", "Take Profit"])
                
            with allure.step("Retrieve the Newly Created Open Position Order"):
                original_orderID, trade_order_df = extract_order_info(driver=main_driver, tab_order_type="open-positions", section_name="Trade Open Position", row_number=[1])

            with allure.step("Retrieve and compare Open Position and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=trade_order_df, name1="Trade Open Position",
                                   df2=trade_snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Volume", "Units", "Stop Loss", "Take Profit"])

            with allure.step("Retrieve and compare Open Position and Notification Order Message / Details"):
                # Call the method to get the lists of dataframes
                noti_message, noti_order_details = process_order_notifications(driver=main_driver, orderIDs=original_orderID)

                # Concatenate all dataframes in the notification_msgs list into a single dataframe

                if noti_message:  # Check if noti_message is not empty
                    noti_msg_df = pd.concat(noti_message, ignore_index=True)

                compare_dataframes(driver=main_driver, df1=trade_order_df, name1="Trade Open Position",
                                   df2=noti_msg_df, name2="Notification Order Message",
                                   required_columns=["Symbol", "Order No.", "Volume", "Units"])

                # Compare against Open Position and Notification Order Details
                if noti_order_details:  # Check if noti_order_details is not empty
                    noti_order_df = pd.concat(noti_order_details, ignore_index=True)

                compare_dataframes(driver=main_driver, df1=trade_order_df, name1="Trade Open Position",
                                   df2=noti_order_df, name2="Notification Order Details",
                                   required_columns=["Open Date", "Symbol", "Order No.", "Type", "Volume", "Units", "Take Profit", "Stop Loss", "Swap", "Commission"])
                
            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, trade_tradeConfirmation_df, trade_snackbar_banner_df, noti_msg_df, noti_order_df)
                
            """ End of Place Order """
            
            """ Start of Modify Order """

            with allure.step("Modify on Market Order"):
                modify_market_order(driver=main_driver, trade_type="edit", row_number=[1], sl_type="price", set_takeProfit=False)

            with allure.step("Click on the Trade Confirmation button to place the order"):
                edit_tradeConfirmation_df = trade_ordersConfirmationDetails(driver=main_driver, trade_type="edit")
                
            with allure.step("Retrieve the modified snackbar message"):
                edit_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Compare against the Trade Confirmation and Snackbar message"):
                compare_dataframes(driver=main_driver, df1=edit_tradeConfirmation_df, name1="Trade Confirmation Details",
                                   df2=edit_snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Volume", "Units", "Stop Loss", "Take Profit"])

            with allure.step("Retrieve the Order Panel data"):
                updated_orderID, updated_order_df = extract_order_info(driver=main_driver, tab_order_type="open-positions", section_name="Updated Open Position", row_number=[1])

            with allure.step("Retrieve and compare Open Position and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=updated_order_df, name1="Updated Open Position",
                                   df2=edit_snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Volume", "Units", "Stop Loss", "Take Profit"])

            with allure.step("Print Modify Order Table Result"):
                process_and_print_data(trade_order_df, edit_tradeConfirmation_df, edit_snackbar_banner_df, updated_order_df)
            
            with allure.step("Verify if it is the same orderIDs"):
                if original_orderID == updated_orderID:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Place orderID - {original_orderID} and Modified orderID - {updated_orderID} not matched"
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
