import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton_OCT, trade_stop_order, modify_stop_order, get_trade_snackbar_banner, extract_order_info
from data_config.utils import compare_dataframes, process_and_print_data, append_orderIDs_to_csv


@allure.epic("MT4 Desktop TS_aG - Stop OCT")

# Member Portal 
class TC_MT4_aG08():
 
    @allure.title("TC_MT4_aG08")

    @allure.description(
        """
        Buy Order
        
        Member able to place a Stop order with
        - Size
        - Price
        - Stop Loss by Points
        - Take Profit by Price
        - Expiry: Good Till Day

        Member able to modify a Stop order with
        - Price
        - Stop Loss by Price
        - Take Profit by Points
        - Expiry: Good Till Cancelled
        """
    )
    
    def test_TC08(self, chromeDriver):
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

            """ Place Stop Order """

            with allure.step("Place Stop Order"):
                trade_stop_order(driver=main_driver, trade_type="trade", option="buy", sl_type="points", tp_type="price", expiryType="good-till-day")
                
            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Retrieve the Newly Created Pending Order"):
                original_orderID, trade_order_df = extract_order_info(driver=main_driver, tab_order_type="pending-orders", section_name="Trade Pending Order", row_number=[1])

            with allure.step("Retrieve and compare Pending Order and Snackbar banner message"):
                compare_dataframes(df1=trade_order_df, name1="Trade Pending Order",
                                   df2=trade_snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Size", "Units", "Stop Loss", "Take Profit"])

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, trade_snackbar_banner_df)
                
            """ End of Place Stop Order """

            """ Start of modifying Pending Order """

            with allure.step("Modify Stop Order"):
                modify_stop_order(driver=main_driver, trade_type="edit", row_number=[1], sl_type="price", tp_type="points", expiryType="good-till-cancelled")

            with allure.step("Retrieve the modified snackbar message"):
                edit_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the Updated Order Panel data"):
                updated_orderID, updated_order_df = extract_order_info(driver=main_driver, tab_order_type="pending-orders", section_name="Updated Pending Order", row_number=[1])
                append_orderIDs_to_csv(order_ids=updated_orderID, filename="MT4_Desktop_Stop_OCT.csv")

            with allure.step("Retrieve and compare the Updated Pending Order and Snackbar banner message"):
                compare_dataframes(df1=updated_order_df, name1="Updated Pending Order",
                                   df2=edit_snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Size", "Units", "Stop Loss", "Take Profit"])

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, edit_snackbar_banner_df, updated_order_df)
                    
            with allure.step("Verify if it is the same orderIDs"):
                if original_orderID == updated_orderID:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Place orderID - {original_orderID} and Modified orderID - {updated_orderID} not matched"

        finally:
            stop_screen_recording(ffmpeg_process)
                        
            shutdown(main_driver)

            attach_video_to_allure(screen_recording_file, class_name)
