import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile
from common.mobileweb.module_login.utils import login_wt
from common.mobileweb.module_symbol.utils import input_symbol
from common.mobileweb.module_trade.utils import toggle_radioButton_OCT, trade_oct_market_order, modify_market_order, get_trade_snackbar_banner, extract_order_info, button_viewAllTransaction
from data_config.utils import compare_dataframes, process_and_print_data


@allure.epic("MT4 Mobile TS_aL - Asset OCT - Modify / Close Market Order")

# Member Portal
class TC_MT4_aL01():

    @allure.title("TC_MT4_aL01")
    
    @allure.description(
        """
        Buy Order
        
        Member able to place a Market order with
        - Size
        
        Member able to modify a Market order with
        - Stop Loss by Points
        - Take Profit by Price
        """
    )
    
    def test_TC01(self, chromeDriver):
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

            with allure.step("Enable OCT"):
                toggle_radioButton_OCT(driver=main_driver, desired_state="checked")
            
            with allure.step("Place Market Order"):
                trade_oct_market_order(driver=main_driver, option="buy")
                
            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the Newly Created Open Position Order"):
                original_orderID, trade_order_df = extract_order_info(driver=main_driver, tab_order_type="open-positions", section_name="Trade Open Position", row_number=1)

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, trade_snackbar_banner_df)
                
            """ Asset Page related """

            with allure.step("Redirect to View All Transaction page"):
                button_viewAllTransaction(driver=main_driver)

            with allure.step("Verify if it is the same orderIDs"):
                asset_orderID, _ = extract_order_info(driver=main_driver, tab_order_type="open-positions", section_name="Asset Open Position", row_number=1)
                if original_orderID == asset_orderID:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Trade orderID - {original_orderID} and Asset orderID - {asset_orderID} not matched"
                    
            """ Start of Modify Order """
            
            with allure.step("Modify on Market Order"):
                modify_market_order(driver=main_driver, trade_type="edit", row_number=1, sl_type="points", tp_type="price")

            with allure.step("Retrieve the modified snackbar message"):
                edit_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the Order Panel data"):
                updated_orderID, updated_order_df = extract_order_info(driver=main_driver, tab_order_type="open-positions", section_name="Updated Open Position", row_number=1)

                if updated_orderID == asset_orderID:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Trade orderID - {updated_orderID} and Asset orderID - {asset_orderID} not matched"

            with allure.step("Retrieve and compare Open Position and Snackbar banner message"):
                compare_dataframes(df1=updated_order_df, name1="Updated Open Position",
                                   df2=edit_snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Size", "Units", "Stop Loss", "Take Profit"])

            with allure.step("Print Modify Order Table Result"):
                process_and_print_data(trade_order_df, edit_snackbar_banner_df, updated_order_df)
                        
        finally:
            # video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            # attach_video_to_allure_mobile(video_data, class_name)