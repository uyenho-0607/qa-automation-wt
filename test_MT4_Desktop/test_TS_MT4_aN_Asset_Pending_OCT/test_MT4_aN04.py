import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_subMenu.utils import menu_button
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton, trade_stop_order, modify_stop_order, get_trade_snackbar_banner, extract_order_info
from data_config.utils import compare_dataframes, process_and_print_data

@allure.parent_suite("MT4 Membersite - Desktop - Asset - Modify / Delete Pending Order")

@allure.epic("MT4 Desktop ts_an - Asset - Modify / Delete Pending Order OCT")

# Member Portal
class TC_mt4_an04():
 
    @allure.title("tc_mt4_an04")

    @allure.description(
        """
        Sell Order
        
        Member able to place a Stop order with
        - Size
        - Price
        - Stop Loss by Points
        - Expiry: Good Till Cancelled

        Member able to modify a Stop order with
        - Price
        - Stop Loss by Price
        - Take Profit by Points
        - Expiry: Good Till Day
        """
    )
    
    def test_tc04(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("Enable OCT"):
                toggle_radioButton(driver=main_driver, category="OCT", desired_state="checked")

            """ Place Stop Order """

            with allure.step("Place Stop Order"):
                trade_stop_order(driver=main_driver, trade_type="trade", option="sell", sl_type="points", set_takeProfit=False, expiryType="good-till-cancelled")
                
            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Retrieve the Newly Created Pending Order"):
                original_orderID, trade_order_df = extract_order_info(driver=main_driver, tab_order_type="pending-orders", section_name="Trade Pending Order", row_number=[1])

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, trade_snackbar_banner_df)
                
            """ End of Place Stop Order """

            with allure.step("Redirect to Asset page"):
                menu_button(driver=main_driver, menu="assets")

            with allure.step("Verify if it is the same orderIDs"):
                asset_orderID, _ = extract_order_info(driver=main_driver, tab_order_type="pending-orders", section_name="Asset Pending Order", row_number=[1])
                if original_orderID == asset_orderID:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Trade orderID - {original_orderID} and Asset orderID - {asset_orderID} not matched"
                
            """ Start of modifying Pending Order """

            with allure.step("Modify Stop Order"):
                modify_stop_order(driver=main_driver, trade_type="edit", row_number=[1], sl_type="price", tp_type="points", expiryType="good-till-day")

            with allure.step("Retrieve the modified snackbar message"):
                edit_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the updated Pending Order"):
                updated_orderID, updated_order_df = extract_order_info(driver=main_driver, tab_order_type="pending-orders", section_name="Updated Pending Order", row_number=[1])
                
                if updated_orderID == asset_orderID:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Trade orderID - {updated_orderID} and Asset orderID - {asset_orderID} not matched"
                    
            with allure.step("Retrieve and compare the Updated Pending Order and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=updated_order_df, name1="Updated Pending Order", df2=edit_snackbar_banner_df, name2="Snackbar Banner Message")

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, edit_snackbar_banner_df, updated_order_df)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
