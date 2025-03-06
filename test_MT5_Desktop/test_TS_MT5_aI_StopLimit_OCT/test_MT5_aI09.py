import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton, trade_stopLimit_order, modify_stopLimit_order, get_trade_snackbar_banner, extract_order_info
from data_config.utils import compare_dataframes, process_and_print_data

@allure.parent_suite("MT5 Membersite - Desktop - Trade - Stop Limit Order")

@allure.epic("MT5 Desktop ts_ai - Stop Limit OCT")

# Member Portal
class TC_mt5_ai09():

    @allure.title("tc_mt5_ai09")

    @allure.description(
        """
        Sell Order
        
        Member able to place a Stop Limit Order with
        - Volume
        - Price
        - Expiry: Good Till Cancelled

        Member able to modify a Stop Limit Order with
        - Price
        - Stop Loss by Points
        - Expiry: Good Till Day
        """
    )
    
    def test_tc09(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server="MT5", client_name="Transactcloudmt5")

            with allure.step("Enable OCT"):
                toggle_radioButton(driver=main_driver, category="OCT", desired_state="checked")
        
            """ Place Stop Limit Order """
            
            with allure.step("Place Stop Limit Order"):
                trade_stopLimit_order(driver=main_driver, trade_type="trade", option="sell", set_stopLoss=False, set_takeProfit=False, expiryType="good-till-cancelled")

            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Retrieve the Newly Created Pending Order"):
                original_orderID, trade_order_df = extract_order_info(driver=main_driver, tab_order_type="pending-orders", section_name="Trade Pending Order", row_number=[1])

            with allure.step("Retrieve and compare Pending Order and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=trade_order_df, name1="Trade Pending Order", df2=trade_snackbar_banner_df, name2="Snackbar Banner Message", compare_volume=False)

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, trade_snackbar_banner_df)
                
            """ End of Place Stop Limit Order """

            """ Start of modifying Pending Order """

            with allure.step("Modify Stop Limit Order"):
                modify_stopLimit_order(driver=main_driver, trade_type="edit", row_number=[1], sl_type="points", set_takeProfit=False, expiryType="good-till-day")

            with allure.step("Retrieve the modified snackbar message"):
                edit_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the Updated Order Panel data"):
                updated_orderID, updated_order_df = extract_order_info(driver=main_driver, tab_order_type="pending-orders", section_name="Updated Pending Order", row_number=[1])
                
            with allure.step("Retrieve and compare the Updated Pending Order and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=updated_order_df, name1="Updated Pending Order", df2=edit_snackbar_banner_df, name2="Snackbar Banner Message", compare_volume=False)

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, edit_snackbar_banner_df, updated_order_df)
                    
            with allure.step("Verify if it is the same orderIDs"):
                if original_orderID == updated_orderID:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Place orderID - {original_orderID} and Modified orderID - {updated_orderID} not matched"

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
