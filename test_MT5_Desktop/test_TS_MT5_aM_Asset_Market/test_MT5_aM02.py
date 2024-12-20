import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_subMenu.utils import menu_button
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton_OCT, trade_market_order, modify_market_order, trade_ordersConfirmationDetails, get_trade_snackbar_banner, extract_order_info
from data_config.utils import compare_dataframes, process_and_print_data


@allure.epic("MT5 Desktop TS_aM - Asset - Modify / Close Market Order")

# Member Portal
class TC_MT5_aM02():

    @allure.title("TC_MT5_aM02")

    @allure.description(
        """
        Sell Order
        
        Member able to place a Market order with
        - Volume
        - Stop Loss by Price
        
        Member able to modify a Market order with
        - Take Profit by Price
        """
    )

    def test_TC02(self, chromeDriver):
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

            with allure.step("Disable OCT"):
                toggle_radioButton_OCT(driver=main_driver)
                
            with allure.step("Place Market Order"):
                trade_market_order(driver=main_driver, trade_type="trade", option="sell", set_fillPolicy=True, sl_type="price", set_takeProfit=False)

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")
                
            with allure.step("Retrieve the snackbar message"):
                get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Retrieve the Newly Created Open Position Order"):
                original_orderID, trade_order_df = extract_order_info(driver=main_driver, tab_order_type="open-positions", section_name="Trade Open Position", row_number=[1])

            """ End of Place Order """
            
            with allure.step("Redirect to Asset page"):
                menu_button(driver=main_driver, menu="assets")
            
            with allure.step("Verify if it is the same orderIDs"):
                asset_orderID, _ = extract_order_info(driver=main_driver, tab_order_type="open-positions", section_name="Asset Open Position", row_number=[1])
                if original_orderID == asset_orderID:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Trade orderID - {original_orderID} and Asset orderID - {asset_orderID} not matched"
                   
            """ Start of Modify Order """
            
            with allure.step("Modify on Market Order"):
                modify_market_order(driver=main_driver, trade_type="edit", row_number=[1], set_stopLoss=False, tp_type="price")

            with allure.step("Click on the Trade Confirmation button to update the order"):
                edit_tradeConfirmation_df = trade_ordersConfirmationDetails(driver=main_driver, trade_type="edit")

            with allure.step("Retrieve the updated order snackbar message "):
                edit_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Compare against the Trade Confirmation and Snackbar message"):
                compare_dataframes(df1=edit_tradeConfirmation_df, name1="Trade Confirmation Details",
                                   df2=edit_snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Volume", "Units", "Stop Loss", "Take Profit"])
                
            with allure.step("Retrieve the updated Open Position Order"):
                updated_orderID, updated_order_df = extract_order_info(driver=main_driver, tab_order_type="open-positions", section_name="Updated Open Position", row_number=[1])
                
                if updated_orderID == asset_orderID:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Trade orderID - {updated_orderID} and Asset orderID - {asset_orderID} not matched"
                    
            with allure.step("Retrieve and compare Open Position and Snackbar banner message"):
                compare_dataframes(df1=updated_order_df, name1="Updated Open Position",
                                   df2=edit_snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Volume", "Units", "Stop Loss", "Take Profit"])

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, edit_tradeConfirmation_df, edit_snackbar_banner_df, updated_order_df)

        finally:
            stop_screen_recording()
                        
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)