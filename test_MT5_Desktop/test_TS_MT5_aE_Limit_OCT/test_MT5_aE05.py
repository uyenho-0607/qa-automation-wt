import allure

from datetime import datetime
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton_OCT, trade_limit_order, modify_limit_order, get_trade_snackbar_banner, extract_order_info
from data_config.utils import compare_dataframes, process_and_print_data, append_orderIDs_to_csv


@allure.epic("MT5 Desktop TS_aE - Limit OCT")

# Member Portal 
class TC_MT5_aE05():

    @allure.title("TC_MT5_aE05")
    
    @allure.description(
        """
        Buy Order
        
        Member able to place a Limit order with
        - Volume
        - Price
        - Take Profit by Points
        - Expiry: Good Till Cancelled

        Member able to modify a Limit order with
        - Price
        - Take Profit by Points
        - Expiry: Specified Date and Time
        """
    )
        
    def test_TC05(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        # Get the class name dynamically
        start_screen_recording()
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT5", client_name="Transactcloudmt5", account_type="live")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, platform="MT5", client_name="Transactcloudmt5")

            with allure.step("Enable OCT"):
                toggle_radioButton_OCT(driver=main_driver, desired_state="checked")

            """ Place Limit Order """

            with allure.step("Place Limit Order"):
                trade_limit_order(driver=main_driver, trade_type="trade", option="buy", set_stopLoss=False, tp_type="points",expiryType="good-till-cancelled")

            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Retrieve the Newly Created Pending Order"):
                original_orderID, trade_order_df = extract_order_info(driver=main_driver, tab_order_type="pending-orders", section_name="Trade Pending Order", row_number=[1])

            with allure.step("Retrieve and compare Pending Order and Snackbar banner message"):
                compare_dataframes(df1=trade_order_df, name1="Trade Pending Order",
                                   df2=trade_snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Units", "Stop Loss", "Take Profit"])

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, trade_snackbar_banner_df)
                
            """ End of Place Limit Order """

            """ Start of modifying Pending Order """

            with allure.step("Modify Limit Order"):
                modify_limit_order(driver=main_driver, trade_type="edit", row_number=[1], set_stopLoss=False, tp_type="points", expiryType="specified-date-and-time", expiryDate="19", targetMonth=datetime.strptime("Nov 2024", "%b %Y"), hour_option="11", min_option="35", specifiedDate=True)

            with allure.step("Retrieve the modified snackbar message"):
                edit_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the Updated Order Panel data"):
                updated_orderID, updated_order_df = extract_order_info(driver=main_driver, tab_order_type="pending-orders", section_name="Updated Pending Order", row_number=[1])
                append_orderIDs_to_csv(order_ids=updated_orderID, filename="MT5_Desktop_Limit_OCT.csv")
                
            with allure.step("Retrieve and compare the Updated Pending Order and Snackbar banner message"):
                compare_dataframes(df1=updated_order_df, name1="Updated Pending Order",
                                   df2=edit_snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Units", "Stop Loss", "Take Profit"])

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, edit_snackbar_banner_df, updated_order_df)
                    
            with allure.step("Verify if it is the same orderIDs"):
                if original_orderID == updated_orderID:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Place orderID - {original_orderID} and Modified orderID - {updated_orderID} not matched"

        finally:
            stop_screen_recording()
                        
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)