import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile
from common.mobileweb.module_login.utils import login_wt
from common.mobileweb.module_symbol.utils import input_symbol
from common.mobileweb.module_trade.utils import toggle_radioButton_OCT, trade_limit_order, modify_limit_order, trade_ordersConfirmationDetails, get_trade_snackbar_banner, extract_order_info
from data_config.utils import compare_dataframes, process_and_print_data, append_orderIDs_to_csv


@allure.epic("MT4 Mobile TS_aD - Limit")

# Member Portal 
class TC_MT4_aB15():

    @allure.title("TC_MT4_aD15")
    
    @allure.description(
        """
        Sell Order
        
        Member able to place a Limit order with
        - Size
        - Price
        - Stop Loss by Price
        - Take Profit by Points
        - Expiry: Good Till Day

        Member able to modify a Limit order with
        - Price
        - Stop Loss by Points
        - Take Profit by Price
        - Expiry: Good Till Cancelled
        """
    )
    
    def test_TC15(self, chromeDriver):
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

            with allure.step("Disable OCT"):
                toggle_radioButton_OCT(driver=main_driver)

            """ Place Limit Order """

            with allure.step("Place Limit Order"):
                trade_limit_order(driver=main_driver, trade_type="trade", option="sell", sl_type="price", tp_type="points", expiryType="good-till-day")

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_tradeConfirmation_df = trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")
                
            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Compare against the Trade Confirmation and Snackbar message"):
                compare_dataframes(df1=trade_tradeConfirmation_df, name1="Trade Confirmation Details",
                                   df2=trade_snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Size", "Units", "Stop Loss", "Take Profit"])
                
            with allure.step("Retrieve the Newly Created Pending Order"):
                original_orderID, trade_order_df = extract_order_info(driver=main_driver, tab_order_type="pending-orders", section_name="Trade Pending Order", row_number=1)

            with allure.step("Retrieve and compare Pending Order and Snackbar banner message"):
                compare_dataframes(df1=trade_order_df, name1="Trade Pending Order",
                                   df2=trade_snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Size", "Units", "Stop Loss", "Take Profit"])

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, trade_tradeConfirmation_df, trade_snackbar_banner_df)
                
            """ End of Place Order """
            
            """ Start of Modify Order """

            with allure.step("Modify on Limit Order"):
                modify_limit_order(driver=main_driver, trade_type="edit", row_number=1, sl_type="points", tp_type="price", expiryType="good-till-cancelled")

            with allure.step("Click on the Trade Confirmation button to update the order"):
                edit_tradeConfirmation_df = trade_ordersConfirmationDetails(driver=main_driver, trade_type="edit")

            with allure.step("Retrieve the modified snackbar message"):
                edit_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Compare against the Trade Confirmation and Snackbar message"):
                compare_dataframes(df1=edit_tradeConfirmation_df, name1="Trade Confirmation Details",
                                   df2=edit_snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Size", "Units", "Stop Loss", "Take Profit"])

            with allure.step("Retrieve the Updated Order Panel data"):
                updated_orderID, updated_order_df = extract_order_info(driver=main_driver, tab_order_type="pending-orders", section_name="Updated Pending Order", row_number=1)
                append_orderIDs_to_csv(order_ids=updated_orderID, filename="MT4_Mobile_Limit.csv")

            with allure.step("Retrieve and compare the Updated Pending Order and Snackbar banner message"):
                compare_dataframes(df1=updated_order_df, name1="Updated Pending Order",
                                   df2=edit_snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Size", "Units", "Stop Loss", "Take Profit"])

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, edit_tradeConfirmation_df, edit_snackbar_banner_df, updated_order_df)

            with allure.step("Verify if it is the same orderIDs"):
                if original_orderID == updated_orderID:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Place orderID - {original_orderID} and Modified orderID - {updated_orderID} not matched"
                
        finally:
            # video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            # attach_video_to_allure_mobile(video_data, class_name)