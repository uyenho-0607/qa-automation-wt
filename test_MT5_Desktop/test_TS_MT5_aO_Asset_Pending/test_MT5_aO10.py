import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_subMenu.utils import menu_button
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton, trade_stop_order, close_delete_order, trade_ordersConfirmationDetails, get_trade_snackbar_banner, extract_order_info
from data_config.utils import compare_dataframes, process_and_print_data

@allure.parent_suite("MT5 Membersite - Desktop - Asset - Modify / Delete Pending Order")

@allure.epic("MT5 Desktop ts_ao - Asset - Modify / Delete Pending Order")

# Member Portal
class TC_mt5_ao10():

    @allure.title("tc_mt5_ao10")

    @allure.description(
        """
        Sell Order
        
        Member able to place a Stop Order
        - Volume
        - Take Profit By Price
        - Expiry: Good Till Cancelled
        
        Member able to delete a Stop order
        """
        )

    def test_tc10(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server="MT5", client_name="Transactcloudmt5")

            with allure.step("Disable OCT"):
                toggle_radioButton(driver=main_driver, category="OCT", desired_state="unchecked")

            """ Place Stop Order """

            with allure.step("Place Stop Order"):
                trade_stop_order(driver=main_driver, trade_type="trade", option="sell", expiryType="good-till-cancelled", set_stopLoss=False, tp_type="price")

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_tradeConfirmation_df = trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")

            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Retrieve the Newly Created Pending Order"):
                original_orderID, trade_order_df = extract_order_info(driver=main_driver, tab_order_type="pending-orders", section_name="Trade Pending Order", row_number=[1])

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, trade_tradeConfirmation_df, trade_snackbar_banner_df)
                
            """ End of Place Order """

            with allure.step("Redirect to Asset page"):
                menu_button(driver=main_driver, menu="assets")

            with allure.step("Verify if it is the same orderIDs"):
                asset_orderID, pending_order_df = extract_order_info(driver=main_driver, tab_order_type="pending-orders", section_name="Pending Order", row_number=[1])
                if original_orderID == asset_orderID:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Trade orderID - {original_orderID} and Asset orderID - {asset_orderID} not matched"

            """ Delete Pending Order """

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
