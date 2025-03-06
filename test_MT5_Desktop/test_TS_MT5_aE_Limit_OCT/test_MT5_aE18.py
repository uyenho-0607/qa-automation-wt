import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton, trade_limit_order, close_delete_order, get_trade_snackbar_banner, extract_order_info
from data_config.utils import compare_dataframes, process_and_print_data

@allure.parent_suite("MT5 Membersite - Desktop - Trade - Limit Order")

@allure.epic("MT5 Desktop ts_ae - Limit OCT")

# Member Portal
class TC_mt5_ae18():

        
    @allure.title("tc_mt5_ae18")

    @allure.description(
        """
        Sell Order
        
        Member able to place a Limit order with
        - Volume
        - Price
        - Take Profit by Price
        - Expiry: Good Till Day
        
        Member able to delete a Limit order
        """
        )


    def test_tc18(self, chromeDriver):
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
                
            """ Place Market Order """

            with allure.step("Place Limit Order"):
                trade_limit_order(driver=main_driver, trade_type="trade", option="sell", expiryType="good-till-day", set_stopLoss=False, tp_type="price")

            with allure.step("Retrieve the snackbar message"):
                get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the Newly Created Pending Order"):
                _, pending_order_df = extract_order_info(driver=main_driver, tab_order_type="pending-orders", section_name="Pending Order", row_number=[1])

            """ End of Place Order """
                
            with allure.step("Order Panel: Pending Order - Click on Delete button"):
                close_delete_order(driver=main_driver, row_number=[1], order_action="close")

            with allure.step("Retrieve the snackbar message"):
                snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Retrieve the Order History data"):
                _, order_history_df = extract_order_info(driver=main_driver, tab_order_type="history", section_name="Order History", row_number=[1], position=True, sub_tab="orders-and-deals")

                compare_dataframes(driver=main_driver, df1=pending_order_df, name1="Pending Order", df2=order_history_df, name2="Order History")

            with allure.step("Print Final Result"):
                process_and_print_data(pending_order_df, snackbar_banner_df, order_history_df)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
